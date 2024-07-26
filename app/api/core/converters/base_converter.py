# app/api/core/converters/base_converter.py
from abc import abstractmethod
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from api.core.llms.chains import BaseChainHandler
from api.core.converters.md_elements import MarkdownPage
from api.core.utils import (
    clean_to_markdown,
    estimate_char_to_token,
    estimate_token_to_char,
    break_text_into_chunks,
)
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

# FileLikeType includes str, bytes, and file-like objects
FileLikeType = Union[str, Path]  # todo: more types


class ParseMode(str, Enum):
    """
    An enumeration class representing different parsing modes.

    Attributes:
        AUTO (str): Automatically determine the parsing mode.
        FAST (str): Fast parsing mode.
        OCR_LOW (str): Use Tesseract OCR, fast but less accurate.
        OCR_HIGH (str): Use Surya model for OCR, accurate but slow.
    """

    AUTO = "auto"
    FAST = "fast"
    OCR_LOW = "ocr-low"  # use tesseract, fast but less accurate
    OCR_HIGH = "ocr-high"  # use surya model, accurate but slow

    @classmethod
    def all_models(cls) -> list[str]:
        """
        Get a list of all available parsing modes as strings.

        Returns:
            list[str]: A list of parsing mode strings.
        """
        return [mode.value for mode in cls.__members__.values()]


class BaseConverter(BaseModel):
    """
    Base class for file converters.

    Attributes:
        file (FileLikeType): The file path.
        parse_mode (Optional[ParseMode]): The parsing mode. Default is ParseMode.AUTO.
        md_data (Optional[MdData]): The markdown data.
        json_data (Optional[dict]): The JSON data.
        request_data (Optional[RequestData]): The request information.
        file_info (Optional[FileInfo]): The file information.
        llm_info (Optional[LlmInfo]): The LLM (Large Language Model) information.
        metadata (Optional[Metadata]): The metadata.
        resp_data (Optional[ResponseData]): The response data.
    """

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
        """
        Abstract method to be implemented by subclasses.
        Get a list of allowed file formats for the converter.

        Returns:
            list[str]: A list of allowed file formats.
        """
        pass

    # file not empty
    @field_validator("file")
    def check_file_exists(cls, v):
        """
        Field validator to check if the file exists.

        Args:
            v (FileLikeType): The file path.

        Raises:
            ValueError: If the file does not exist.

        Returns:
            FileLikeType: The file path if the file exists.
        """
        if not Path(v).exists():
            raise ValueError(f"File {v} does not exist")
        return v

    @abstractmethod
    def process(self, **kwargs) -> str:
        """
        Abstract method to be implemented by subclasses.
        Core function to convert the file to raw text.

        Returns:
            str: The raw text extracted from the file.
        """
        pass

    def convert(self, **kwargs) -> ResponseData:
        """
        Main method to convert the file to markdown or JSON.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            ResponseData: The response data containing the conversion result.
        """
        try:
            raw = self.process(**kwargs)
            if Config.ENABLE_LLM and self.request_data.use_llm:
                self.llm_enforce(raw)
            self.set_response_data(status="success", raw=raw)
        except Exception as e:
            logger.error(f"Error converting file: {e}")
            self.set_response_data(status="error", error=str(e))
        finally:
            self.rm_file()

        return self.resp_data

    def to_dict(self):
        """
        Convert the BaseConverter instance to a dictionary.

        Returns:
            dict: A dictionary representation of the BaseConverter instance.
        """
        return self.model_dump()

    def rm_file(self):
        """
        Remove the file if it exists.

        Returns:
            bool: True if the file was removed, False otherwise.
        """
        if Path(self.file).exists():
            Path(self.file).unlink()
            return True

    def set_file_info(
        self,
        file_info: FileInfo,
    ) -> None:
        """
        Set the file information for the converter.

        Args:
            file_info (FileInfo): The file information.
        """
        logger.debug(f"Setting file info: {file_info}")
        self.file_info = file_info

    def set_request_data(
        self,
        request_data: RequestData,
    ) -> None:
        """
        Set the request data for the converter.

        Args:
            request_data (RequestData): The request data.
        """
        logger.debug(f"Setting request info: {request_data}")
        self.request_data = request_data

    def set_llm_info(
        self,
        model_source: str,
        model: str,
        cb: OpenAICallbackHandler,
        messages: Optional[list] = None,
    ) -> None:
        """
        Set the LLM (Large Language Model) information for the converter.

        Args:
            model_source (str): The source of the LLM model.
            model (str): The name of the LLM model.
            cb (OpenAICallbackHandler): The OpenAI callback handler.
            messages (Optional[list]): The list of messages. Default is None.
        """
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

    def add_llm_cb(self, cb: OpenAICallbackHandler):
        """
        Add LLM callback information to the existing LLM info.

        Args:
            cb (OpenAICallbackHandler): The OpenAI callback handler.

        Raises:
            ValueError: If LLM info is not set.
        """
        if not self.llm_info:
            raise ValueError("You must run set_llm_info() before add_llm_cb()")

        self.llm_info.total_tokens += cb.total_tokens
        self.llm_info.prompt_tokens += cb.prompt_tokens
        self.llm_info.completion_tokens += cb.completion_tokens
        self.llm_info.total_cost += cb.total_cost

    def set_md_data(self, md: str) -> None:
        """
        Set the markdown data for the converter.

        Args:
            md (str): The markdown content.
        """
        logger.debug(f"Setting markdown data: {md}")

        markdown_page = MarkdownPage.from_md(md)
        self.md_data = MdData(
            content=markdown_page.to_md(),
            elements=markdown_page.to_elements_list(),
            toc=markdown_page.toc(),
        )

    def add_md_data(self, md: str) -> None:
        """
        Add markdown data to the existing markdown data for the converter.

        Args:
            md (str): The markdown content to be added.
        """
        logger.debug(f"Adding markdown data: {md}")

        markdown_page = MarkdownPage.from_md(md)

        if markdown_page.to_md().startswith("#"):
            self.md_data.content += "\n\n"
        self.md_data.content += markdown_page.to_md()
        self.md_data.elements.extend(markdown_page.to_elements_list())
        self.md_data.toc.extend(markdown_page.toc())

    def set_json_data(self, json: dict) -> None:
        """
        Set the JSON data for the converter.

        Args:
            json (dict): The JSON data.
        """
        logger.debug(f"Setting JSON data: {json}")
        self.json_data = json

    def set_metadata(self) -> None:
        """
        Set the metadata for the converter.

        Raises:
            ValueError: If request data or file info is not set.
        """
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
        Set the response data for the converter.

        Args:
            status (str): The status of the response. Default is None.
            raw (str): The raw content extracted from the file. Default is None.
            error (str): The error message. Default is None.

        Raises:
            ValueError: If metadata is not set.
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
        max_tokens: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> str:
        """
        Convert OCR text to markdown format using LLM.

        Args:
            ocr_text (str): The OCR text to be converted.
            split_len (int): The maximum length of each text block. Default is 8000.
            model_source (Optional[str]): The source of the LLM model. Default is None.
            model (Optional[str]): The name of the LLM model. Default is None.
            comment (Optional[str]): An optional comment for the LLM. Default is None.

        Returns:
            str: The converted markdown content.
        """
        # split text into parts so that the tokens don't exceed the limit
        chunks = []
        md_blocks = []
        chunks = break_text_into_chunks(ocr_text, max_tokens)

        logger.info(f"Text split into {len(chunks)} parts")

        for i, text in enumerate(chunks):
            logger.info(f"Processing text chunk {i + 1}/{len(chunks)}")
            if i == 0:
                md_blocks.append(
                    self.first_block_ocr_fix_to_markdown(
                        text,
                        model_source=model_source,
                        model=model,
                        comment=comment,
                    )
                )
            else:
                md_blocks.append(
                    self.block_ocr_fix_to_markdown(
                        text,
                        pre_toc=self.md_data.toc,
                        pre_overlap=md_blocks[-1],
                        model_source=model_source,
                        model=model,
                        comment=comment,
                    )
                )
            self.set_md_data("".join(md_blocks))

    def first_block_ocr_fix_to_markdown(
        self,
        ocr_text: str,
        model_source: Optional[str] = None,
        model: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> str:
        """
        Convert the first block of OCR text to markdown format using LLM.

        Args:
            ocr_text (str): The OCR text to be converted.
            model_source (Optional[str]): The source of the LLM model. Default is None.
            model (Optional[str]): The name of the LLM model. Default is None.
            comment (Optional[str]): An optional comment for the LLM. Default is None.

        Returns:
            str: The converted markdown content for the first block.
        """
        chain = BaseChainHandler.get_instance(
            model_source, model
        ).ocr_fix_to_markdown_chain(comment=comment)
        logger.info(f"Converting OCR text to markdown: {ocr_text}")

        chain_params = {"ocr_text": ocr_text}
        if comment:
            chain_params["comment"] = comment

        with get_openai_callback() as cb:
            result: str = chain.invoke(chain_params).strip()
            self.set_llm_info(model_source, model, cb)

        result = clean_to_markdown(result)

        logger.info(f"OCR text converted to markdown: {result}")

        return result

    def block_ocr_fix_to_markdown(
        self,
        ocr_text: str,
        pre_toc: str,
        pre_overlap: str,
        model_source: Optional[str] = None,
        model: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> str:
        """
        Convert a block of OCR text to markdown format using LLM.

        Args:
            ocr_text (str): The OCR text to be converted.
            pre_toc (str): The table of contents from the previous block.
            pre_overlap (str): The overlapping text from the previous block.
            model_source (Optional[str]): The source of the LLM model. Default is None.
            model (Optional[str]): The name of the LLM model. Default is None.
            max_tokens (Optional[int]): The maximum number of tokens. Default is None.
            comment (Optional[str]): An optional comment for the LLM. Default is None.

        Returns:
            str: The converted markdown content for the block.
        """
        chain = BaseChainHandler.get_instance(
            model_source, model
        ).block_ocr_fix_to_markdown_chain(comment=comment)
        logger.info(f"Converting block OCR text to markdown: {ocr_text}")

        chain_params = {
            "ocr_text": ocr_text,
            "pre_toc": pre_toc,
            "overlap": len(pre_overlap),
            "pre_overlap": pre_overlap,
        }
        if comment:
            chain_params["comment"] = comment

        with get_openai_callback() as cb:
            result: str = chain.invoke(chain_params).strip()
            self.add_llm_cb(cb)

        result = clean_to_markdown(result)

        logger.info(f"Block OCR text converted to markdown: {result}")

        return result

    def ocr_fix_to_json(
        self,
        ocr_text: str,
        enforced_json_format: Optional[str | dict] = None,
        model_source: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> str:
        """
        Convert OCR text to JSON format using LLM.

        Args:
            ocr_text (str): The OCR text to be converted.
            enforced_json_format (Optional[str | dict]): The enforced JSON format. Default is None.
            model_source (Optional[str]): The source of the LLM model. Default is None.
            model (Optional[str]): The name of the LLM model. Default is None.
            comment (Optional[str]): An optional comment for the LLM. Default is None.

        Returns:
            str: The converted JSON data.
        """
        chain = BaseChainHandler.get_instance(
            model_source, model
        ).ocr_fix_to_json_chain(comment=comment)
        logger.info(f"Converting OCR text to json: {ocr_text}")

        chain_params = {
            "ocr_text": ocr_text,
            "enforced_json_format": enforced_json_format,
        }
        if comment:
            chain_params["comment"] = comment

        with get_openai_callback() as cb:
            result = chain.invoke(chain_params)
            self.set_llm_info(model_source, model, cb)  # todo: add messages
        self.set_json_data(result)

        return result

    def llm_enforce(self, text: str):
        """
        Use LLM to clean and enforce the text to structured format.

        Args:
            text (str): The text to be cleaned and enforced.
        """
        model_source = self.request_data.model_source
        model = self.request_data.model
        max_tokens = self.request_data.max_tokens
        return_type = self.request_data.return_type
        enforced_json_format = self.request_data.enforced_json_format
        comment = self.request_data.comment

        if return_type == "json":
            self.ocr_fix_to_json(
                text,
                enforced_json_format=enforced_json_format,
                model_source=model_source,
                model=model,
                max_tokens=max_tokens,
                comment=comment,
            )
        elif return_type == "md":
            self.ocr_fix_to_markdown(
                text,
                model_source=model_source,
                model=model,
                max_tokens=max_tokens,
                comment=comment,
            )

        else:
            raise ValueError("return_type must be one of 'md' or 'json")

    # todo: add model
    def extract_markdown(self, image: str, model: Optional[str] = None) -> str:
        """
        Abstract method to be implemented by subclasses.
        Extract markdown content from an image.

        Args:
            image (str): The image file path or URL.
            model (Optional[str]): The name of the LLM model. Default is None.

        Returns:
            str: The extracted markdown content.
        """
        raise NotImplementedError

    # todo: add model
    def extract_json(self, image: str, model: Optional[str] = None) -> dict:
        """
        Abstract method to be implemented by subclasses.
        Extract JSON data from an image.

        Args:
            image (str): The image file path or URL.
            model (Optional[str]): The name of the LLM model. Default is None.

        Returns:
            dict: The extracted JSON data.
        """
        raise NotImplementedError
