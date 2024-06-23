from abc import abstractmethod
from langchain_core.runnables.base import RunnableSequence
import hashlib


class BaseChainHandler:

    def __init__(self, model: str = None):
        self.model = model
        self.chains = {}

    @classmethod
    def get_instance(cls, model_source: str):
        if model_source == "anthropic":
            from api.core.llms.chains.anthropic_chain_handler import (
                AnthropicChainHandler,
            )

            return AnthropicChainHandler()
        elif model_source == "ollama":
            from api.core.llms.chains.ollama_chain_handler import OllamaChainHandler

            return OllamaChainHandler()
        elif model_source == "baichuan":
            from api.core.llms.chains.baichuan_chain_handler import BaichuanChainHandler

            return BaichuanChainHandler()
        elif model_source == "openai":
            from api.core.llms.chains.openai_chain_handler import OpenaiChainHandler

            return OpenaiChainHandler()
        elif model_source == "zhipuai":
            from api.core.llms.chains.zhipuai_chain_handler import ZhipuaiChainHandler

            return ZhipuaiChainHandler()
        elif model_source == "moonshot":
            from api.core.llms.chains.moonshot_chain_handler import MoonshotChainHandler

            return MoonshotChainHandler()
        elif model_source == "xinference":
            from api.core.llms.chains.xinference_chain_handler import (
                XinferenceChainHandler,
            )

            return XinferenceChainHandler()
        else:
            raise ValueError(f"Unknown model source: {model_source}")

    @abstractmethod
    def ocr_fix_to_markdown_chain(self, model=None) -> RunnableSequence:
        pass

    @abstractmethod
    def ocr_fix_to_json_chain(self, model=None) -> RunnableSequence:
        pass

    @abstractmethod
    def extract_markdown_chain(self, model=None) -> RunnableSequence:
        pass

    @abstractmethod
    def extract_json_chain(self, model=None) -> RunnableSequence:
        pass

    def _get_hash_key(*args, **kwargs):
        hash_key = hashlib.md5(f"{args}{kwargs}".encode()).hexdigest()
        return hash_key
