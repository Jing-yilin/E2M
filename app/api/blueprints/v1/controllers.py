from flask import jsonify
from api.core.converters.base_converter import BaseConverter
from api.core.converters.converter_strategy import ConverterStrategy
from typing import Tuple
from api.blueprints.v1.schemas import ResponseData, FileInfo, RequestData

# logging
import logging

logger = logging.getLogger(__name__)


def ping():
    """This function is used to check if the API is running."""
    return jsonify({"message": "You have successfully connected to the e2m API!"}), 200


def file_to_markdown(
    file_info: FileInfo, request_data: RequestData, **kwargs
) -> Tuple[dict, int]:

    converter: BaseConverter = ConverterStrategy.get_converter(file=file_info.file_path)

    converter.set_file_info(file_info=file_info)
    converter.set_request_data(request_data=request_data)

    resp: ResponseData = converter.convert(**kwargs)

    logger.info(f"Converted file to markdown: {resp}")

    return (resp.to_dict(), 200)
