import logging
from langchain_community.chat_models import ChatOllama
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


class OllamaChainHandler(BaseChainHandler):
    """

    Ollama Chain Handler
    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Ollama model: {model}")
        elif Config.OLLAMA_DEFAULT_MODEL:
            model = Config.OLLAMA_DEFAULT_MODEL
            logger.info(f"Using default Ollama model: {model}")
        else:
            model = "ollama3"
            logger.info(
                f"You have not specified an Ollama model. Using default model: {model}"
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
            chat_model = ChatOllama(model=model, base_url=Config.OLLAMA_BASE)
            messages = [("human", OCR_FIX_TO_MARKDOWN_PROMPT)]
            if addition:
                messages.append(("human", ADDITIONAL_PROMTPT))
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
            chat_model = ChatOllama(model=model, base_url=Config.OLLAMA_BASE)
            messages = [("human", OCR_FIX_TO_JSON_PROMPT)]
            if addition:
                messages.append(("human", ADDITIONAL_PROMTPT))
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
            chat_model = ChatOllama(model=model, base_url=Config.OLLAMA_BASE)
            messages = [("human", EXTRACT_MARKDOWN_PROMPT)]
            if addition:
                messages.append(("human", ADDITIONAL_PROMTPT))
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
            chat_model = ChatOllama(model=model, base_url=Config.OLLAMA_BASE)
            messages = [("human", EXTRACT_JSON_PROMPT)]
            if addition:
                messages.append(("human", ADDITIONAL_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]
