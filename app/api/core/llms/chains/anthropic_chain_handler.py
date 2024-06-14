import logging
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables.base import RunnableSequence
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.core.llms.prompts import (
    OCR_FIX_TO_MARKDOWN_PROMPT,
    OCR_FIX_TO_JSON_PROMPT,
    EXTRACT_MARKDOWN_PROMPT,
    EXTRACT_JSON_PROMPT,
    ADDITIONAL_PROMTPT,
)
from api.config import Config

logger = logging.getLogger(__name__)


class AnthropicChainHandler(BaseChainHandler):
    """
    Anthropic Chain Handler

    You can set the following environment variables to use the Anthropic API:
    - ANTHROPIC_API_KEY: Your Anthropic API key

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Anthropic model: {model}")
        elif Config.ANTHROPIC_DEFAULT_MODEL:
            model = Config.ANTHROPIC_DEFAULT_MODEL
            logger.info(f"Using default Anthropic model: {model}")
        else:
            model = "claude-3-opus-20240229"
            logger.info(
                f"You have not specified an Anthropic model. Using default model: {model}"
            )

        super().__init__(model)

    def ocr_fix_to_markdown_chain(
        self, model=None, addition: str = None
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="ocr_fix_to_markdown", model=model, addition=addition
        )
        if hash_key not in self.chains:
            chat_model = ChatAnthropic(model=model)
            messages = [("system", OCR_FIX_TO_MARKDOWN_PROMPT)]
            if addition:
                messages.append(("system", ADDITIONAL_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def ocr_fix_to_json_chain(
        self, model=None, addition: str = None
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="ocr_fix_to_json", model=model, addition=addition
        )
        if hash_key not in self.chains:
            chat_model = ChatAnthropic(model=model)
            messages = [("system", OCR_FIX_TO_JSON_PROMPT)]
            if addition:
                messages.append(("system", ADDITIONAL_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def extract_markdown_chain(
        self, model=None, addition: str = None
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="extract_markdown", model=model, addition=addition
        )
        if hash_key not in self.chains:
            chat_model = ChatAnthropic(model=model)
            messages = [("system", EXTRACT_MARKDOWN_PROMPT)]
            if addition:
                messages.append(("system", ADDITIONAL_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def extract_json_chain(self, model=None, addition: str = None) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="extract_json", model=model, addition=addition
        )
        if hash_key not in self.chains:
            chat_model = ChatAnthropic(model=model)
            messages = [("system", EXTRACT_JSON_PROMPT)]
            if addition:
                messages.append(("system", ADDITIONAL_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]
