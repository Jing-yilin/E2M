from api.core.converters.base_converter import (
    BaseConverter,
)


class EpubConverter(BaseConverter):
    def convert(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
