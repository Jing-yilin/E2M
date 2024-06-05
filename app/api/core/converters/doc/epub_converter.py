from api.core.converters.base_converter import BaseConverter


class EpubConverter(BaseConverter):

    @classmethod
    def allowed_formats(cls) -> list[str]:
        return ["epub"]

    def convert(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")
