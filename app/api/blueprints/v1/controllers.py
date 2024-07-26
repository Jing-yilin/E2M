# app/api/blueprints/v1/controllers.py

from flask import jsonify
from api.core.converters.base_converter import BaseConverter
from api.core.converters.converter_strategy import ConverterStrategy
from typing import Tuple, Dict, Any
from api.blueprints.v1.schemas import ResponseData, FileInfo, RequestData

import logging

logger = logging.getLogger(__name__)


def ping() -> Tuple[Dict[str, str], int]:
    """
    Check if the API is running.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a dictionary with a message and an HTTP status code.
    """
    logger.info("Ping request received")
    return jsonify({"message": "You have successfully connected to the e2m API!"}), 200


def file_to_markdown(
    file_info: FileInfo, request_data: RequestData, **kwargs: Any
) -> Tuple[Dict[str, Any], int]:
    """
    Convert a file to markdown format.

    Args:
        file_info (FileInfo): Information about the file to be converted.
        request_data (RequestData): Additional request data for the conversion.
        **kwargs: Additional keyword arguments for the conversion process.

    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing the conversion result as a dictionary and an HTTP status code.

    Raises:
        ValueError: If the file type is not supported.
    """
    logger.info(f"Starting conversion for file: {file_info.file_name}")

    try:
        converter: BaseConverter = ConverterStrategy.get_converter(
            file=file_info.file_path
        )
    except ValueError as e:
        logger.error(f"Unsupported file type: {e}")
        return ResponseData(status="error", error=str(e)).to_dict(), 400

    try:
        converter.set_file_info(file_info=file_info)
        converter.set_request_data(request_data=request_data)

        resp: ResponseData = converter.convert(**kwargs)

        if resp.error:
            logger.error(f"Error converting file to markdown: {resp.error}")
            return resp.to_dict(), 400

        logger.info(f"Successfully converted file to markdown: {file_info.file_name}")
        return resp.to_dict(), 200

    except Exception as e:
        logger.exception(f"Unexpected error during file conversion: {e}")
        return (
            ResponseData(
                status="error", error=f"An unexpected error occurred: {str(e)}"
            ).to_dict(),
            500,
        )
