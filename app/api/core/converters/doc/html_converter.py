from api.core.converters.base_converter import (
    BaseConverter,
)


class HtmlConverter(BaseConverter):

    @classmethod
    def allowed_formats(cls) -> list[str]:
        return ["htm", "html"]

    def convert_htm(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def convert_html(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def convert(self, **kwargs) -> str:
        if self.file_info.file_type == "htm":
            self.convert_htm(**kwargs)
        elif self.file_info.file_type == "html":
            self.convert_html(**kwargs)
        else:
            raise ValueError(f"Unsupported file type: {self.file_info.file_type}")

        self.rm_file()
        return self.resp_data
