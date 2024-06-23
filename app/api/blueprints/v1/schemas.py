from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional
import json
import logging
import hashlib

logger = logging.getLogger(__name__)


class RequestData(BaseModel):

    file_hash: str = Field(
        ..., description="The hash of the file, e.g. 1234567890abcdef"
    )

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

    use_llm: Optional[bool] = Field(
        default=False,
        description="Whether to use the LLM for parsing. The default is False.",
    )

    model_source: Optional[str] = Field(
        default="openai",
        description="The model source to use for parsing. The default is 'openai'.",
    )

    model: Optional[str] = Field(
        default="gpt-3.5-turbo",
        description="The model to use for parsing. The default is 'gpt-3.5-turbo'.",
    )

    return_type: Optional[str] = Field(
        default="md", description="The return type. The default is 'md'."
    )

    enforced_json_format: Optional[str | dict] = Field(
        default=None, description="The enforced JSON format."
    )

    comment: Optional[str] = Field(
        default=None, description="The comment for the request."
    )

    save_to_cache: Optional[bool] = Field(
        default=True, description="Whether to save the result to the cache."
    )

    use_cache: Optional[bool] = Field(
        default=True, description="Whether to use the cache."
    )

    @field_validator("parse_mode")
    def check_parse_mode(cls, parse_mode, info: ValidationInfo):
        from api.core.converters.base_converter import ParseMode

        if parse_mode not in ParseMode.all_modes():
            raise ValueError(
                'parse_mode must be one of "auto", "ocr-low", "ocr-high", "fast"'
            )
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

    @field_validator("return_type")
    def check_return_type(cls, return_type, info: ValidationInfo):
        if return_type not in ["md", "json"]:
            raise ValueError('return_type must be one of "md" or "json"')
        return return_type

    @field_validator("enforced_json_format")
    def check_enforced_json_format(cls, enforced_json_format, info: ValidationInfo):
        # try to parse the enforced_json_format as a dict, if not , keep it as a string
        if isinstance(enforced_json_format, str):
            enforced_json_format = enforced_json_format.strip()
        if not enforced_json_format:
            return ""
        try:
            enforced_json_format = json.loads(enforced_json_format)
        except json.JSONDecodeError:
            logger.debug("enforced_json_format is not a valid JSON string")
        return enforced_json_format

    def to_dict(self):
        return self.model_dump(mode="json")

    def __str__(self) -> str:
        return str(self.to_dict())

    def get_hash_key(self):
        return hashlib.md5(
            f"{self.file_hash}{self.parse_mode}{self.langs}{self.first_page}{self.last_page}{self.model}{self.return_type}{self.enforced_json_format}".encode()
        ).hexdigest()


class MdData(BaseModel):
    content: str = Field(..., description="The markdown content.")
    elements: list = Field(..., description="The markdown elements.")
    toc: list = Field(..., description="The table of contents.")


class FileInfo(BaseModel):
    file_path: str = Field(
        ..., description="The path to the file, e.g. /path/to/test.pdf"
    )
    file_name: str = Field(..., description="The name of the file, e.g. test.pdf")
    file_size: int = Field(..., description="The size of the file in bytes, e.g. 12345")
    file_type: str = Field(..., description="The type of the file, e.g. pdf")
    file_hash: str = Field(
        ..., description="The hash of the file, e.g. 1234567890abcdef"
    )

    def to_dict(self):
        return self.model_dump(mode="json")


class LlmInfo(BaseModel):
    model: str = Field(..., description="The LLM model used.")
    messages: Optional[list] = Field(
        ...,
        description="The messages exchanged between the system, user, and assistant.",
    )
    total_tokens: int = Field(..., description="The total number of tokens used.")
    prompt_tokens: int = Field(..., description="The number of tokens in the prompt.")
    completion_tokens: int = Field(
        ..., description="The number of tokens in the completion."
    )
    successful_requests: int = Field(
        ..., description="The number of successful requests."
    )
    total_cost: float = Field(..., description="The total cost of the LLM operation.")

    def to_dict(self):
        return self.model_dump(mode="json")


class Metadata(BaseModel):
    request_data: RequestData = Field(..., description="The request information.")
    file_info: FileInfo = Field(..., description="The file information.")
    llm_info: Optional[LlmInfo] = Field(..., description="The LLM information.")

    def to_dict(self):
        return self.model_dump(mode="json")


class ResponseData(BaseModel):
    status: str = Field(..., description="The status of the response.")
    raw: Optional[str] = Field(
        ..., description="The raw content extracted from the file."
    )
    md_data: Optional[MdData] = Field(..., description="The markdown content.")
    json_data: Optional[dict] = Field(..., description="The JSON content.")
    metadata: Metadata = Field(..., description="The metadata.")
    error: Optional[str] = Field(None, description="The error message.")

    def to_dict(self):
        return self.model_dump(mode="json")
