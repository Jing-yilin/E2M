from api.core.converters.base_converter import (
    BaseConverter,
)


class HtmConverter(BaseConverter):
    def convert(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
