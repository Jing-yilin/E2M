from flask import Blueprint, request, jsonify
from ....converters import file_to_markdown

bp = Blueprint("v1", __name__)


# return ”you have successfully connected to e2m api“
@bp.route("/ping", methods=["GET"])
def ping():
    """
    It is used to check if the API is running.
    e.g:
        curl http://127.0.0.1:8765/api/v1/ping

    """
    return jsonify({"message": "You have successfully connected to the e2m API!"})


@bp.route("/convert", methods=["POST"])
def convert_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    markdown = file_to_markdown(file)
    return jsonify({"markdown": markdown})
