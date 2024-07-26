from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.blueprints.v1.controllers import ping, file_to_markdown
from api.blueprints.v1.schemas import RequestData, FileInfo, ResponseData
from api.blueprints.v1.models import ConversionCache, db
from api.config import Config
from api.core.utils.file_utils import get_file_hash, save_file_to_temp
import os
import json
import logging
from werkzeug.utils import secure_filename
from functools import wraps

logger = logging.getLogger(__name__)

bp = Blueprint("v1", __name__)


def validate_file(func):
    """
    Decorator to validate the uploaded file.

    This decorator checks if a file is present in the request and if its type is allowed.
    If validation fails, it returns an appropriate error response.

    Args:
        func (callable): The route function to be decorated.

    Returns:
        callable: The wrapped function that includes file validation.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        file = request.files.get("file")
        if not file:
            return (
                jsonify(
                    ResponseData(status="error", error="No file uploaded").to_dict()
                ),
                400,
            )
        if not allowed_file(file.filename):
            return (
                jsonify(
                    ResponseData(
                        status="error", error="File type not allowed"
                    ).to_dict()
                ),
                400,
            )
        return func(*args, **kwargs)

    return wrapper


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str): The name of the uploaded file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "ppt", "pptx", "html", "htm"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/", methods=["GET"])
@swag_from("./swagger/index.yml")
def index_route():
    """
    Handle the index route of the API.

    Returns:
        tuple: A JSON response with a welcome message and HTTP status code 200.
    """
    return (
        jsonify({"message": "You have successfully reached the API, congratulations!"}),
        200,
    )


@bp.route("/ping", methods=["GET"])
@swag_from("./swagger/ping.yml")
def ping_route():
    """
    Handle the ping route of the API.

    Returns:
        Response: The result of the ping() function from controllers.
    """
    return ping()


@bp.route("/convert", methods=["POST"])
@swag_from("./swagger/convert.yml")
@validate_file
def convert_route():
    """
    Handle the file conversion route.

    This function processes the uploaded file, checks the cache for existing results,
    performs the conversion if necessary, and stores the result in the cache.

    Returns:
        tuple: A JSON response with the conversion result and an HTTP status code.
    """
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = save_file_to_temp(file)

    file_info = get_file_info(file_path, filename)
    request_data = get_request_data(request, file_info.file_hash)
    cache_key = request_data.get_hash_key()

    if Config.USE_DB and request_data.use_cache:
        cached_result = check_cache(cache_key, request_data)
        if cached_result:
            return jsonify(json.loads(cached_result.result)), 200

    response, code = file_to_markdown(file_info=file_info, request_data=request_data)

    if Config.USE_DB and request_data.save_to_cache and code == 200:
        store_result_to_cache(cache_key, file_info, request_data, response)

    return jsonify(response), code


def get_file_info(file_path, file_name):
    """
    Get information about the uploaded file.

    Args:
        file_path (str): The path to the uploaded file.
        file_name (str): The name of the uploaded file.

    Returns:
        FileInfo: An object containing information about the file.
    """
    return FileInfo(
        file_path=file_path,
        file_name=file_name,
        file_size=os.path.getsize(file_path),
        file_type=file_name.rsplit(".", 1)[-1].lower(),
        file_hash=get_file_hash(file_path),
    )


def get_request_data(request, file_hash):
    """
    Extract and process request data from the incoming request.

    Args:
        request (Request): The Flask request object.
        file_hash (str): The hash of the uploaded file.

    Returns:
        RequestData: An object containing the processed request data.
    """
    data = RequestData(
        file_hash=file_hash,
        parse_mode=request.form.get("parse_mode", "auto"),
        langs=request.form.get("langs", "zh").split(","),
        extract_images=request.form.get("extract_images", "false").lower() == "true",
        first_page=int(request.form.get("first_page", 1)),
        last_page=(
            int(request.form.get("last_page"))
            if request.form.get("last_page")
            else None
        ),
        use_llm=request.form.get("use_llm", "false").lower() == "true",
        model_source=request.form.get("model_source", "openai"),
        model=request.form.get("model", "gpt-3.5-turbo"),
        max_tokens=int(request.form.get("max_tokens", 4096)),
        return_type=request.form.get("return_type", "md"),
        enforced_json_format=request.form.get("enforced_json_format"),
        comment=request.form.get("comment"),
        save_to_cache=request.form.get("save_to_cache", "true").lower() == "true",
        use_cache=request.form.get("use_cache", "true").lower() == "true",
    )
    logger.info(f"Request data: {data}")
    return data


def check_cache(cache_key, data):
    """
    Check if a cached result exists for the given cache key and request data.

    Args:
        cache_key (str): The cache key to check.
        data (RequestData): The request data object.

    Returns:
        ConversionCache or None: The cached result if found, None otherwise.
    """
    logger.info("Checking cache")
    cached_result = ConversionCache.query.filter_by(
        cache_key=cache_key,
        parse_mode=data.parse_mode,
        langs=",".join(data.langs),
        extract_images=data.extract_images,
        first_page=data.first_page,
        last_page=data.last_page,
        use_llm=data.use_llm,
        model_source=data.model_source,
        model=data.model,
        max_tokens=data.max_tokens,
        return_type=data.return_type,
        enforced_json_format=data.enforced_json_format,
        comment=data.comment,
    ).first()
    logger.info("Cache hit" if cached_result else "Cache miss")
    return cached_result


def store_result_to_cache(cache_key, file_info, request_data, response):
    """
    Store the conversion result in the cache.

    Args:
        cache_key (str): The cache key for storing the result.
        file_info (FileInfo): Information about the processed file.
        request_data (RequestData): The request data used for the conversion.
        response (dict): The conversion result to be stored.

    Raises:
        Exception: If there's an error while storing the result in the cache.
    """
    logger.info("Storing result to cache")
    try:
        new_cache_entry = ConversionCache(
            cache_key=cache_key,
            file_name=file_info.file_name,
            parse_mode=request_data.parse_mode,
            langs=",".join(request_data.langs),
            extract_images=request_data.extract_images,
            first_page=request_data.first_page,
            last_page=request_data.last_page,
            use_llm=request_data.use_llm,
            model_source=request_data.model_source,
            model=request_data.model,
            return_type=request_data.return_type,
            enforced_json_format=request_data.enforced_json_format,
            comment=request_data.comment,
            result=json.dumps(response),
        )
        db.session.add(new_cache_entry)
        db.session.commit()
        logger.info("Result stored to cache")
    except Exception as e:
        logger.error(f"Error storing result to cache: {e}")
        db.session.rollback()
