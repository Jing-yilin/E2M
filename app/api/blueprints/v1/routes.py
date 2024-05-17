from flask import Blueprint, request, jsonify
from flasgger import swag_from
from .controllers import ping, file_to_markdown

bp = Blueprint("v1", __name__)


@bp.route("/ping", methods=["GET"])
@swag_from("./swagger/ping.yml")
def ping_route():
    """It is used to check if the API is running.
    ---
    """
    return ping()


@bp.route("/convert", methods=["POST"])
@swag_from("./swagger/convert.yml")
def convert_route():
    """This endpoint is used to convert a file to markdown.
    ---
    """
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    return file_to_markdown(file)
