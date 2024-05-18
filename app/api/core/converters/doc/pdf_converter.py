from api.core.converters.base_converter import (
    BaseConverter,
)


class PdfConverter(BaseConverter):
    def convert(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
