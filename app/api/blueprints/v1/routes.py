from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.blueprints.v1.controllers import ping, file_to_markdown
from api.blueprints.v1.schemas import RequestData, FileInfo, ResponseData
from api.config import Config
from api.core.utils.file_utils import get_file_hash
import os
import json


# logging
import logging

logger = logging.getLogger(__name__)

bp = Blueprint("v1", __name__)


@bp.route("/", methods=["GET"])
@swag_from("./swagger/index.yml")
def index_route():
    return (
        jsonify({"message": "You have successfully reached the API, congratulations!"}),
        200,
    )


@bp.route("/ping", methods=["GET"])
@swag_from("./swagger/ping.yml")
def ping_route():
    return ping()


@bp.route("/convert", methods=["POST"])
@swag_from("./swagger/convert.yml")
def convert_route():
    from api.blueprints.v1.models import ConversionCache, db

    file = request.files.get("file")

    if not file:
        return (
            jsonify(ResponseData(status="error", error="No file uploaded").to_dict()),
            400,
        )

    file_name = file.filename

    # save to temp directory
    logger.debug("Saving file to temp directory")
    file_path = f"./temp/{file_name}"
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    file.save(file_path)
    logger.debug(f"File saved to {file_path}")

    # get file info
    file_info: FileInfo = FileInfo(
        file_path=file_path,
        file_name=file_name,
        file_size=os.path.getsize(file_path),
        file_type=file_name.split(".")[-1],
        file_hash=get_file_hash(file_path),
    )

    # get request info
    data = RequestData(
        file_hash=file_info.file_hash,
        parse_mode=request.form.get("parse_mode", default="auto"),
        langs=request.form.get("langs", default="zh").split(","),
        extract_images=request.form.get("extract_images", default=False),
        first_page=int(request.form.get("first_page", default=1)),
        last_page=request.form.get("last_page", default=None),
        use_llm=request.form.get("use_llm", default=False),
        model_source=request.form.get("model_source", default="openai"),
        model=request.form.get("model", default="gpt-3.5-turbo"),
        return_type=request.form.get("return_type", default="md"),  # md, json
        enforced_json_format=request.form.get("enforced_json_format", default=None),
        save_to_cache=request.form.get("save_to_cache", default=True),
        use_cache=request.form.get("use_cache", default=True),
    )
    if data.last_page is not None:
        data.last_page = int(data.last_page)
    logger.info(f"Request data: {data}")

    # get cache key
    cache_key = data.get_hash_key()

    if Config.USE_DB and data.use_cache:

        # check cache
        logger.info("Checking cache")
        cached_result = ConversionCache.query.filter_by(
            cache_key=cache_key,
            parse_mode=data.parse_mode,
            langs=str(data.langs),
            extract_images=data.extract_images,
            first_page=data.first_page,
            last_page=data.last_page,
            use_llm=data.use_llm,
            model_source=data.model_source,
            model=data.model,
            return_type=data.return_type,
            enforced_json_format=data.enforced_json_format,
        ).first()
        if cached_result:
            logger.info(f"Cache hit: {cached_result}")
            logger.info(f"Cached result: {cached_result.result}")
            resp_dict = json.loads(cached_result.result)
            code = 200
            os.remove(file_path)
            return jsonify(resp_dict), code

        logger.info("Cache miss")

    # execute conversion
    resp_dict, code = file_to_markdown(  # Response
        file_info=file_info,
        request_data=data,
    )

    if Config.USE_DB and data.save_to_cache:
        # save to cache if successful
        logger.info("Storing result to cache")
        try:

            new_cache_entry = ConversionCache(
                cache_key=cache_key,
                file_name=file_info.file_name,
                parse_mode=data.parse_mode,
                langs=str(data.langs),
                extract_images=data.extract_images,
                first_page=data.first_page,
                last_page=data.last_page,
                use_llm=data.use_llm,
                model_source=data.model_source,
                model=data.model,
                return_type=data.return_type,
                enforced_json_format=data.enforced_json_format,
                result=json.dumps(resp_dict),
            )
            db.session.add(new_cache_entry)
            db.session.commit()
            logger.info("Result stored to cache")
        except Exception as e:
            logger.error(f"Error storing result to cache: {e}")
            resp_dict = ResponseData(
                status="error", error=f"Error storing result to cache: {e}"
            ).to_dict()
            code = 500

    return jsonify(resp_dict), code
