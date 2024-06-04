# get a converter by extension

from typing import Union

from api.core.converters.base_converter import ParseMode
from api.core.converters.base_converter import BaseConverter
from api.core.converters.doc import (
    ALL_SUPPORT_TYPES,
    DocxConverter,
    HtmlConverter,
    HtmConverter,
    EpubConverter,
    PdfConverter,
    RtfConverter,
)

# todo: more converters


class ConverterStrategy:
    """This class is used to get a converter by extension."""

    @classmethod
    def get_converter(
        cls, file: str, parse_mode: Union[ParseMode, str] = "auto", **kwargs
    ) -> BaseConverter:

        # identify parse mode
        if isinstance(parse_mode, str):
            if parse_mode == "auto":
                parse_mode = ParseMode.AUTO
            elif parse_mode == "general":
                parse_mode = ParseMode.GENERAL
            elif parse_mode == "book":
                parse_mode = ParseMode.BOOK
            elif parse_mode == "law":
                parse_mode = ParseMode.LAW
            elif parse_mode == "manual":
                parse_mode = ParseMode.MANUAL
            elif parse_mode == "paper":
                parse_mode = ParseMode.PAPER
            elif parse_mode == "resume":
                parse_mode = ParseMode.RESUME
            elif parse_mode == "qa":
                parse_mode = ParseMode.QA
            elif parse_mode == "table":
                parse_mode = ParseMode.TABLE
            else:
                raise ValueError(
                    f"Unsupported parse mode: {parse_mode}, your parse mode should be \
                          one of {ParseMode.__members__}"
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
        if file_extension in ["docx", "doc"]:
            return DocxConverter(file=file, parse_mode=parse_mode, **kwargs)
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
