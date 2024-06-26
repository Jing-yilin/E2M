import logging
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
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

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatOllama(model=model)
