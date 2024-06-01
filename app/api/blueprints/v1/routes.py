from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.blueprints.v1.controllers import ping, file_to_markdown
from api.blueprints.v1.schemas import ConvertRequest
from pydantic import ValidationError
import hashlib
import os


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
        return jsonify({"error": "No file uploaded"}), 400
    file_name = file.filename

    try:
        data = ConvertRequest(
            parse_mode=request.form.get("parse_mode", default="auto"),
            langs=request.form.get("langs", default="zh").split(","),
            extract_images=request.form.get("extract_images", default=False),
            first_page=int(request.form.get("first_page", default=1)),
            last_page=request.form.get("last_page", default=None),
        )
        if data.last_page is not None:
            data.last_page = int(data.last_page)
        logger.debug(f"Request data: {data}")
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # 生成缓存键
    cache_key = hashlib.md5(
        f"{file_name}{data.parse_mode}{data.extract_images}{data.langs}{data.first_page}{data.last_page}".encode()
    ).hexdigest()

    # 检查缓存
    logger.info("Checking cache")
    cached_result = ConversionCache.query.filter_by(
        cache_key=cache_key,
        # file_name=file_name,
        parse_mode=data.parse_mode,
        langs=str(data.langs),
        extract_images=data.extract_images,
    ).first()
    if cached_result:
        logger.info(f"Cache hit: {cached_result}")
        return jsonify({"message": cached_result.result}), 200
    logger.info("Cache miss")

    # 保存文件到临时目录
    logger.info("Saving file to temp directory")
    file_path = f"./temp/{file_name}"
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    file.save(file_path)

    # 执行转换
    md_result, code = file_to_markdown(  # Response
        file_path=file_path,
        parse_mode=data.parse_mode,
        langs=data.langs,
        extract_images=data.extract_images,
        first_page=data.first_page,
        last_page=data.last_page,
    )

    # save to cache if successful
    if code == 200:
        logger.info("Storing result to cache")
        try:
            new_cache_entry = ConversionCache(
                cache_key=cache_key,
                file_name=file_name,
                parse_mode=data.parse_mode,
                langs=str(data.langs),
                extract_images=data.extract_images,
                first_page=data.first_page,
                last_page=data.last_page,
                result=md_result,
            )
            db.session.add(new_cache_entry)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error storing result to cache: {e}")
            return jsonify({"error": "Error storing result to cache"}), 500
        logger.info("Result stored to cache")
    else:
        logger.error("Error converting file to markdown")

    return jsonify({"message": md_result}), code
