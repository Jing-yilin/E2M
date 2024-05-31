from flask import jsonify
from api.core.converters.base_converter import BaseConverter
from api.core.converters.converter_strategy import ConverterStrategy
from typing import Tuple, Optional
from pathlib import Path


# logging
import logging

logger = logging.getLogger(__name__)


def ping():
    """This function is used to check if the API is running."""
    return jsonify({"message": "You have successfully connected to the e2m API!"}), 200


def file_to_markdown(
    file_path: Optional[str | Path], parse_mode: str, **kwargs
) -> Tuple[str, int]:
    # try:
    converter: BaseConverter = ConverterStrategy.get_converter(
        file=file_path, parse_mode=parse_mode
    )

    md_result = converter.convert(**kwargs)

    logger.info(f"Converted file to markdown: {md_result}")

    return (md_result, 200)
    # except Exception as e:
    #     logger.error(f"Error converting file to markdown: {e}")
    #     return (f"Error converting file to markdown: {e}", 500)
