import logging
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class OpenaiChainHandler(BaseChainHandler):
    """
    OpenAI Chain Handler

    You can set the following environment variables to use the OpenAI API:
    - OPENAI_API_KEY: Your OpenAI API key
    - OPENAI_API_BASE: The base URL for the OpenAI API
    - OPENAI_PROXY: The proxy URL for the OpenAI API

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using OpenAI model: {model}")
        elif Config.OPENAI_DEFAULT_MODEL:
            model = Config.OPENAI_DEFAULT_MODEL
            logger.info(f"Using default OpenAI model: {model}")
        else:
            model = "gpt-3.5-turbo"
            logger.info(
                f"You have not specified an OpenAI model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatOpenAI(model=model, api_key=Config.OPENAI_API_KEY)
