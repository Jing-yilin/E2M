from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ConvertRequest(BaseModel):
    parse_mode: Optional[str] = Field(
        default="auto", description="The parse mode to use. The default is 'auto'."
    )
    start_page: Optional[int] = Field(
        default=0, description="The start page to convert from."
    )
    end_page: Optional[int] = Field(
        default=None, description="The end page to convert to."
    )
    extract_images: Optional[bool] = Field(
        default=False, description="Whether to extract images from the file."
    )

    @field_validator("end_page")
    def check_pages(cls, end_page, values):
        start_page = values.data.get("start_page")
        if end_page is not None and start_page is not None and start_page > end_page:
            raise ValueError("start_page cannot be greater than end_page")
        return end_page

    @field_validator("parse_mode")
    def check_parse_mode(cls, parse_mode, values):
        if parse_mode not in ["auto", "general", "book", "law", "manual", "paper"]:
            raise ValueError('parse_mode must be one of "auto", "markdown", or "html"')
        return parse_mode

    def to_dict(self):
        return self.model_dump(mode="json")

    def __str__(self) -> str:
        return str(self.to_dict())
