# get a converter by extension

from typing import Union

from api.core.parsers.base_parser import ParserMode
from api.core.converters.base_converter import BaseConverter
from api.core.converters.doc import (
    support_types as doc_support_types,
    TxtConverter,
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
        cls, file: str, parse_mode: Union[ParserMode, str] = "auto", **kwargs
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
        if file_extension in ["txt", "md", "py", "json", "yaml", "yml"]:
            return TxtConverter(file=file, parse_mode=parse_mode, **kwargs)
        if file_extension == "docx":
            return DocxConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "doc":
            return DocConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "html":
            return HtmlConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "htm":
            return HtmConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "epub":
            return EpubConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "pdf":
            return PdfConverter(file=file, parse_mode=parse_mode, **kwargs)
        elif file_extension == "rtf":
            return RtfConverter(file=file, parse_mode=parse_mode, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
