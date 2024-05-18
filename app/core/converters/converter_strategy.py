# get a converter by extension

from typing import Union

from ..parsers.base_parser import ParserMode
from .base_converter import BaseConverter
from .doc import (
    support_types as doc_support_types,
    DocConverter,
    DocxConverter,
    HtmlConverter,
    HtmConverter,
    EpubConverter,
    PdfConverter,
    RtfConverter,
)

# todo: more converters


ALL_SUPPORT_TYPES = doc_support_types


class ConverterStrategy:
    """This class is used to get a converter by extension."""

    @classmethod
    def get_converter(
        cls, file: str, parse_mode: Union[ParserMode, str] = "auto", *args, **kwargs
    ) -> BaseConverter:

        # identify parse mode
        if isinstance(parse_mode, str):
            if parse_mode == "auto":
                parse_mode = ParserMode.AUTO
            elif parse_mode == "general":
                parse_mode = ParserMode.GENERAL
            elif parse_mode == "book":
                parse_mode = ParserMode.BOOK
            elif parse_mode == "law":
                parse_mode = ParserMode.LAW
            elif parse_mode == "manual":
                parse_mode = ParserMode.MANUAL
            elif parse_mode == "paper":
                parse_mode = ParserMode.PAPER
            elif parse_mode == "resume":
                parse_mode = ParserMode.RESUME
            elif parse_mode == "qa":
                parse_mode = ParserMode.QA
            elif parse_mode == "table":
                parse_mode = ParserMode.TABLE
            else:
                raise ValueError(
                    f"Unsupported parse mode: {parse_mode}, your parse mode should be \
                          one of {ParserMode.__members__}"
                )

        # get a converter by extension
        if not file:
            raise ValueError("file is required")
        file_extension = file.split(".")[-1]
        if file_extension not in ALL_SUPPORT_TYPES:
            raise ValueError(
                f"Unsupported file type: {file_extension}, your file type should be \
                one of {ALL_SUPPORT_TYPES}"
            )
        if file_extension == "docx":
            return DocxConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "doc":
            return DocConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "html":
            return HtmlConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "htm":
            return HtmConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "epub":
            return EpubConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "pdf":
            return PdfConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        elif file_extension == "rtf":
            return RtfConverter(file=file, parse_mode=parse_mode, *args, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
