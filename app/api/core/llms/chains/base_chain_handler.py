from abc import abstractmethod
from langchain_core.runnables.base import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from api.core.llms.prompts import (
    OCR_FIX_TO_MARKDOWN_PROMPT,
    BLOCK_OCR_FIX_TO_MARKDOWN_PROMPT,
    OCR_FIX_TO_JSON_PROMPT,
    EXTRACT_MARKDOWN_PROMPT,
    EXTRACT_JSON_PROMPT,
    COMMENT_PROMTPT,
)
import hashlib


class BaseChainHandler:

    def __init__(self, model: str = None):
        self.model = model
        self.chains = {}

    @classmethod
    def get_instance(cls, model_source: str, model: str = None):
        if model_source == "anthropic":
            from api.core.llms.chains.anthropic_chain_handler import (
                AnthropicChainHandler,
            )

            return AnthropicChainHandler(model=model)
        elif model_source == "ollama":
            from api.core.llms.chains.ollama_chain_handler import OllamaChainHandler

            return OllamaChainHandler(model=model)
        elif model_source == "baichuan":
            from api.core.llms.chains.baichuan_chain_handler import BaichuanChainHandler

            return BaichuanChainHandler(model=model)
        elif model_source == "openai":
            from api.core.llms.chains.openai_chain_handler import OpenaiChainHandler

            return OpenaiChainHandler(model=model)
        elif model_source == "zhipuai":
            from api.core.llms.chains.zhipuai_chain_handler import ZhipuaiChainHandler

            return ZhipuaiChainHandler(model=model)
        elif model_source == "moonshot":
            from api.core.llms.chains.moonshot_chain_handler import MoonshotChainHandler

            return MoonshotChainHandler(model=model)
        elif model_source == "tongyi":
            from api.core.llms.chains.tongyi_chain_handler import TongyiChainHandler

            return TongyiChainHandler(model=model)
        elif model_source == "xinference":
            from api.core.llms.chains.xinference_chain_handler import (
                XinferenceChainHandler,
            )

            return XinferenceChainHandler(model=model)
        elif model_source == "deepseek":
            from api.core.llms.chains.deepseek_chain_handler import (
                DeepseekChainHandler,
            )

            return DeepseekChainHandler(model=model)
        elif model_source == "google":
            from api.core.llms.chains.google_chain_handler import GoogleChainHandler

            return GoogleChainHandler(model=model)

        else:
            raise ValueError(f"Unknown model source: {model_source}")

    @abstractmethod
    def _init_chat_model(self, model, **kwargs) -> BaseChatModel:
        pass

    def ocr_fix_to_markdown_chain(
        self, model=None, comment: str = None, **kwargs
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="ocr_fix_to_markdown", model=model, comment=comment
        )
        if hash_key not in self.chains:
            chat_model = self._init_chat_model(model=model, **kwargs)
            messages = [("human", OCR_FIX_TO_MARKDOWN_PROMPT)]
            if comment:
                messages.append(("human", COMMENT_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def block_ocr_fix_to_markdown_chain(
        self, model=None, comment: str = None, **kwargs
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="block_ocr_fix_to_markdown", model=model, comment=comment
        )
        if hash_key not in self.chains:
            chat_model = self._init_chat_model(model=model, **kwargs)
            messages = [("human", BLOCK_OCR_FIX_TO_MARKDOWN_PROMPT)]
            if comment:
                messages.append(("human", COMMENT_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def ocr_fix_to_json_chain(
        self, model=None, comment: str = None, **kwargs
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="ocr_fix_to_json", model=model, comment=comment
        )
        if hash_key not in self.chains:
            chat_model = self._init_chat_model(model=model, **kwargs)
            messages = [("human", OCR_FIX_TO_JSON_PROMPT)]
            if comment:
                messages.append(("human", COMMENT_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def extract_markdown_chain(
        self, model=None, comment: str = None, **kwargs
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="extract_markdown", model=model, comment=comment, **kwargs
        )
        if hash_key not in self.chains:
            chat_model = self._init_chat_model(model=model)
            messages = [("human", EXTRACT_MARKDOWN_PROMPT)]
            if comment:
                messages.append(("human", COMMENT_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def extract_json_chain(
        self, model=None, comment: str = None, **kwargs
    ) -> RunnableSequence:
        if model is None:
            model = self.model
        hash_key = self._get_hash_key(
            chain_name="extract_json", model=model, comment=comment
        )
        if hash_key not in self.chains:
            chat_model = self._init_chat_model(model=model, **kwargs)
            messages = [("human", EXTRACT_JSON_PROMPT)]
            if comment:
                messages.append(("human", COMMENT_PROMTPT))
            prompt_template = ChatPromptTemplate.from_messages(messages)
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            self.chains[hash_key] = chain
        return self.chains[hash_key]

    def _get_hash_key(*args, **kwargs):
        hash_key = hashlib.md5(f"{args}{kwargs}".encode()).hexdigest()
        return hash_key
