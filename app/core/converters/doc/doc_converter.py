from ..base_converter import (
    BaseConverter,
)


class DocConverter(BaseConverter):

    def convert(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
