from pydantic import BaseModel, Field, field_validator
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

    @field_validator("parse_mode")
    def check_parse_mode(cls, parse_mode, values):
        if parse_mode not in ["auto", "general", "book", "law", "manual", "paper"]:
            raise ValueError('parse_mode must be one of "auto", "markdown", or "html"')
        return parse_mode

    def to_dict(self):
        return self.model_dump(mode="json")

    def __str__(self) -> str:
        return str(self.to_dict())
