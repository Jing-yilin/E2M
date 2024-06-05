# get a converter by extension

from api.core.converters.base_converter import ParseMode
from api.core.converters.base_converter import BaseConverter
from api.core.converters.doc import (
    ALL_SUPPORT_TYPES,
)

# todo: more converters


class ConverterStrategy:
    """This class is used to get a converter by extension."""

    @classmethod
    def get_converter(
        cls, file: str, parse_mode: str = "auto", **kwargs
    ) -> BaseConverter:

        # identify parse mode
        for mode in ParseMode:
            if parse_mode == mode.value:
                parse_mode = mode
                break

        # get a converter by extension
        file_extension = file.split(".")[-1]
        if file_extension not in ALL_SUPPORT_TYPES:
            raise ValueError(
                f"Unsupported file type: {file_extension}, your file type should be \
                one of {ALL_SUPPORT_TYPES}"
            )

        for converter in BaseConverter.__subclasses__():
            if file_extension in converter.allowed_formats():
                return converter(file=file, parse_mode=parse_mode, **kwargs)

        raise ValueError(f"Unsupported file type: {file_extension}")
