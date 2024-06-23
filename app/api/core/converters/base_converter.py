from abc import abstractmethod
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from api.core.llms.chains import BaseChainHandler
from api.core.converters.md_elements import MarkdownPage
from api.blueprints.v1.schemas import (
    RequestData,
    MdData,
    FileInfo,
    LlmInfo,
    Metadata,
    ResponseData,
)
from api.config import Config
from typing import Union, Optional, Tuple
from langchain_community.callbacks import get_openai_callback, OpenAICallbackHandler

import logging

logger = logging.getLogger(__name__)

# FikeLikeType includes str, bytes, and file-like objects
FileLikeType = Union[str | Path]  # todo: more types


class ParseMode(str, Enum):
    AUTO = "auto"
    FAST = "fast"
    OCR_LOW = "ocr-low"  # use tesseract, fast but less accurate
    OCR_HIGH = "ocr-high"  # use surya model, accurate but slow

    @classmethod
    def all_modes(cls) -> list[str]:
        return [mode.value for mode in cls.__members__.values()]


class BaseConverter(BaseModel):

    file: FileLikeType = Field(..., title="File path")
    parse_mode: Optional[ParseMode] = Field(ParseMode.AUTO, title="Parser mode")
    # response
    md_data: Optional[MdData] = Field(None, title="Markdown data")
    json_data: Optional[dict] = Field(None, title="JSON data")
    request_data: Optional[RequestData] = Field(None, title="Request info")
    file_info: Optional[FileInfo] = Field(None, title="File info")
    llm_info: Optional[LlmInfo] = Field(None, title="LLM info")
    metadata: Optional[Metadata] = Field(None, title="Metadata")
    resp_data: Optional[ResponseData] = Field(None, title="Response data")

    @classmethod
    @abstractmethod
    def allowed_formats(cls) -> list[str]:
        pass

    # file not empty
    @field_validator("file")
    def check_file_exists(cls, v):
        if not Path(v).exists():
            raise ValueError(f"File {v} does not exist")
        return v

    @abstractmethod
    def process(self, **kwargs) -> str:
        """Core function to convert the file to raw"""
        pass

    def convert(self, **kwargs) -> ResponseData:
        """Main method to convert the file to markdown or json.
        function process() should be implemented in the subclass.
        """
        # try:
        raw = self.process(**kwargs)
        if Config.ENABLE_LLM and self.request_data.use_llm:
            self.llm_enforce(raw)
        self.set_response_data(status="success", raw=raw)
        # except Exception as e:
        #     logger.error(f"Error converting file: {e}")
        #     self.set_response_data(status="error", error=str(e))
        # finally:
        #     self.rm_file()

        return self.resp_data

    def to_dict(self):
        return self.model_dump()

    def rm_file(self):
        if Path(self.file).exists():
            Path(self.file).unlink()
            return True

    def set_file_info(
        self,
        file_info: FileInfo,
    ) -> None:
        logger.debug(f"Setting file info: {file_info}")
        self.file_info = file_info

    def set_request_data(
        self,
        request_data: RequestData,
    ) -> None:
        logger.debug(f"Setting request info: {request_data}")
        self.request_data = request_data

    def set_llm_info(
        self,
        model_source: str,
        model: str,
        cb: OpenAICallbackHandler,
        messages: Optional[list] = None,
    ) -> None:
        logger.debug("Setting LLM info")

        self.llm_info = LlmInfo(
            model_source=model_source,
            model=model,
            messages=messages,
            total_tokens=cb.total_tokens,
            prompt_tokens=cb.prompt_tokens,
            completion_tokens=cb.completion_tokens,
            successful_requests=cb.successful_requests,
            total_cost=cb.total_cost,
        )

    def set_md_data(self, md: str) -> None:
        logger.debug(f"Setting markdown data: {md}")

        markdown_page = MarkdownPage.from_md(md)
        self.md_data = MdData(
            content=markdown_page.to_md(),
            elements=markdown_page.to_elements_list(),
            toc=markdown_page.toc(),
        )

    def set_json_data(self, json: dict) -> None:
        logger.debug(f"Setting JSON data: {json}")
        self.json_data = json

    def set_metadata(self) -> None:
        logger.debug("Setting metadata")

        if not self.request_data:
            raise ValueError("Request data not set")
        if not self.file_info:
            raise ValueError("File info not set")
        if not self.llm_info and Config.ENABLE_LLM and self.request_data.use_llm:
            # raise ValueError("LLM info not set")
            logger.warning("LLM info not set")

        self.metadata = Metadata(
            request_data=self.request_data,
            file_info=self.file_info,
            llm_info=self.llm_info,
        )

    def set_response_data(
        self, status: str = None, raw: str = None, error: str = None
    ) -> None:
        """
        status: Optional[str] = Field(..., description="The status of the response.")
        raw: Optional[str] = Field(..., description="The raw content extracted from the file.")
        md_data: Optional[MdData] = Field(..., description="The markdown content.")
        json_data: Optional[dict] = Field(..., description="The JSON content.")
        metadata: Optional[Metadata] = Field(..., description="The metadata.")
        error: Optional[str] = Field(None, description="The error message.")
        """
        logger.debug("Setting response data")
        if not self.metadata:
            self.set_metadata()
        if not self.md_data:
            logger.warning("Markdown data not set")
        if not self.json_data:
            logger.warning("JSON data not set")
        if not self.metadata:
            raise ValueError("Metadata not set")
        self.resp_data = ResponseData(
            status=status,
            raw=raw,
            md_data=self.md_data,
            json_data=self.json_data,
            metadata=self.metadata,
            error=error,
        )

    def ocr_fix_to_markdown(
        self,
        ocr_text: str,
        model_source: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Tuple[str, OpenAICallbackHandler]:
        chain = BaseChainHandler.get_instance(model_source).ocr_fix_to_markdown_chain(
            model
        )
        logger.info(f"Converting OCR text to markdown: {ocr_text}")

        with get_openai_callback() as cb:
            result: str = chain.invoke({"ocr_text": ocr_text}).strip()
            self.set_llm_info(model_source, model, cb)
        # todo: add more rules or use a parser
        if result.startswith("```markdown") and result.endswith("```"):
            result = result[11:-3]
        elif result.startswith("```") and result.endswith("```"):
            result = result[3:-3]
        elif result.startswith("```markdown") and not result.endswith("```"):
            logger.warning("Markdown code block not closed")
            result = result[11:]
        elif result.startswith("```") and not result.endswith("```"):
            logger.warning("Markdown code block not closed")
            result = result[3:]
        self.set_md_data(result)
        return result.strip()

    def ocr_fix_to_json(
        self,
        ocr_text: str,
        enforced_json_format: Optional[str | dict] = None,
        model_source: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Tuple[dict, OpenAICallbackHandler]:
        chain = BaseChainHandler.get_instance(model_source).ocr_fix_to_json_chain(model)
        logger.info(f"Converting OCR text to json: {ocr_text}")
        with get_openai_callback() as cb:
            result = chain.invoke(
                {"ocr_text": ocr_text, "enforced_json_format": enforced_json_format}
            )
            self.set_llm_info(model_source, model, cb)  # todo: add messages
        self.set_json_data(result)

        return result

    def llm_enforce(self, text: str):
        """Use LLM to clean and enforce the text to structured format"""
        model_source = self.request_data.model_source
        model = self.request_data.model
        return_type = self.request_data.return_type
        enforced_json_format = self.request_data.enforced_json_format

        if return_type == "json":
            self.ocr_fix_to_json(
                text,
                enforced_json_format=enforced_json_format,
                model_source=model_source,
                model=model,
            )
        elif return_type == "md":
            self.ocr_fix_to_markdown(text, model_source=model_source, model=model)
        else:
            raise ValueError("return_type must be one of 'md' or 'json")

    # todo: add model
    def extract_markdown(self, image: str, model: Optional[str] = None) -> str:
        raise NotImplementedError

    # todo: add model
    def extract_json(self, image: str, model: Optional[str] = None) -> dict:
        raise NotImplementedError
