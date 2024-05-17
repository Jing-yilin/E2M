from flask import jsonify


def ping():
    """This function is used to check if the API is running."""
    return jsonify({"message": "You have successfully connected to the e2m API!"}), 200


def file_to_markdown(*args, **kwargs):
    # todo: this is temp implementation
    return jsonify({"message": "This is a markdown file!"}), 200
