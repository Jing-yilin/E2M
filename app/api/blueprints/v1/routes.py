from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.blueprints.v1.controllers import ping, file_to_markdown
from api.blueprints.v1.schemas import ConvertRequest
from pydantic import ValidationError
import os

# logging
import logging

logger = logging.getLogger(__name__)

bp = Blueprint("v1", __name__)


@bp.route("/ping", methods=["GET"])
@swag_from("./swagger/ping.yml")
def ping_route():
    """It is used to check if the API is running.

    e.g:
        curl -X GET "http://localhost:8765/api/v1/ping" \
        -H "accept: application/json"
    ---
    """
    return ping()


@bp.route("/convert", methods=["POST"])
@swag_from("./swagger/convert.yml")
def convert_route():
    """This endpoint is used to convert a file to markdown.

    parameters:
        - name: file
            in: formData
            type: file
            required: true
            description: The file to be converted to markdown.
        - name: parse_mode
            in: query
            type: string
            required: false
            description: The parse mode to use. The default is "auto".
        - name: start_page
            in: query
            type: integer
            required: false
            description: The start page to convert from.
        - name: end_page
            in: query
            type: integer
            required: false
            description: The end page to convert to.
        - name: extract_images
            in: query
            type: boolean
            required: false
            description: Whether to extract images from the file.

    # use utf-8

    e.g: curl -X POST "http://localhost:8765/api/v1/convert" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data; charset=utf-8" \
        -H "Accept-Charset: utf-8" \
        -F "file=@/path/to/file.docx" \
        -F "parse_mode=auto"

    ---
    """
    file = request.files.get("file")
    logger.debug(f"File Type: {type(file)}")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file_name = file.filename
    logger.info(f"Received file: {file_name}")

    file_path = f"./temp/{file_name}"
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    file.save(file_path)
    logger.info(f"File saved to: ./temp/{file_name}")

    try:
        data = ConvertRequest(
            parse_mode=request.args.get("parse_mode", default="auto"),
            start_page=request.args.get("start_page", default=0),
            end_page=request.args.get("end_page", default=None),
            extract_images=request.args.get("extract_images", default=False),
        )
        logger.info(f"Received data: {data}")
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    return file_to_markdown(
        file_path=file_path,
        parse_mode=data.parse_mode,
        start_page=data.start_page,
        end_page=data.end_page,
        extract_images=data.extract_images,
    )
