from flask import jsonify
from ....core.converters.base_converter import BaseConverter
from ....core.converters.converter_strategy import ConverterStrategy


# logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def ping():
    """This function is used to check if the API is running."""
    return jsonify({"message": "You have successfully connected to the e2m API!"}), 200


def file_to_markdown(file_path: str, parse_mode: str, *args, **kwargs):

    converter: BaseConverter = ConverterStrategy.get_converter(
        file=file_path, parse_mode=parse_mode
    )
    md_result = converter.convert()

    logger.info(f"Converted file to markdown: {md_result}")

    return jsonify({"message": md_result}), 200
