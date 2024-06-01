from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional


class ConvertRequest(BaseModel):
    parse_mode: Optional[str] = Field(
        default="auto", description="The parse mode to use. The default is 'auto'."
    )

    langs: Optional[list] = Field(
        default=["zh"],
        description="The languages to use for parsing. The default is ['zh'] (Chinese).",
    )

    extract_images: Optional[bool] = Field(
        default=False, description="Whether to extract images from the file."
    )

    first_page: Optional[int] = Field(
        default=1, description="The first page to start parsing from. The default is 1."
    )

    last_page: Optional[int] = Field(
        default=None, description="The last page to parse. The default is None."
    )

    @field_validator("parse_mode")
    def check_parse_mode(cls, parse_mode, info: ValidationInfo):
        if parse_mode not in ["auto", "general", "book", "law", "manual", "paper"]:
            raise ValueError('parse_mode must be one of "auto", "markdown", or "html"')
        return parse_mode

    @field_validator("first_page")
    def check_first_page(cls, first_page, info: ValidationInfo):
        if first_page < 1:
            raise ValueError("first_page must be greater than or equal to 1")
        return first_page

    @field_validator("last_page")
    def check_last_page(cls, last_page, info: ValidationInfo):
        first_page = info.data.get("first_page", 1)
        if last_page is not None and last_page < first_page:
            raise ValueError("last_page must be greater than or equal to first_page")
        return last_page

    def to_dict(self):
        return self.model_dump(mode="json")

    def __str__(self) -> str:
        return str(self.to_dict())
