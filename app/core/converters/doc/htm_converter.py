from ..base_converter import (
    BaseConverter,
)


class HtmConverter(BaseConverter):
    def convert(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
