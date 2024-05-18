from ..base_converter import (
    BaseConverter,
)


class EpubConverter(BaseConverter):
    def convert(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
