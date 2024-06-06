from api.core.converters.base_converter import (
    BaseConverter,
)


class RtfConverter(BaseConverter):
    def process(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
