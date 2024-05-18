from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.blueprints.v1.controllers import ping, file_to_markdown
import os

# logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

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
    # File Type: <class 'werkzeug.datastructures.file_storage.FileStorage'>
    logger.debug(f"File Type: {type(file)}")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file_name = file.filename
    logger.info(f"Received file: {file_name}")
    # todo: use database to store the file
    # save the file "./temp/file_name.docx"
    file_path = f"./temp/{file_name}"
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    file.save(file_path)
    logger.info(f"File saved to: ./temp/{file_name}")
    parse_mode = request.args.get("parse_mode", default="auto")
    logger.info(f"parse_mode: {parse_mode}")

    return file_to_markdown(file_path=file_path, parse_mode=parse_mode)
