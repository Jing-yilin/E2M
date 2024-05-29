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
            parse_mode=request.args.get("parse_mode", default="auto"),
            langs=request.args.get("langs", default="zh").split(","),
            extract_images=request.args.get("extract_images", default=False),
        )
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # 生成缓存键
    cache_key = hashlib.md5(
        f"{file_name}{data.parse_mode}{data.extract_images}".encode()
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
        logger.info("Cache hit")
        return jsonify({"result": cached_result.result})
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
        extract_images=data.extract_images,
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
