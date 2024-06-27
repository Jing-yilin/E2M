import logging
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class DeepseekChainHandler(BaseChainHandler):
    """
    OpenAI Chain Handler

    You can set the following environment variables to use the OpenAI API:
    - OPENAI_API_KEY: Your OpenAI API key
    - OPENAI_API_BASE: https://api.deepseek.com
    - OPENAI_PROXY: The proxy URL for the OpenAI API

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Deepseek model: {model}")
        elif Config.DEEPSEEK_DEFAULT_MODEL:
            model = Config.DEEPSEEK_DEFAULT_MODEL
            logger.info(f"Using default Deepseek model: {model}")
        else:
            model = "deepseek-chat"
            logger.info(
                f"You have not specified an Deepseek model. Using default model: {model}"
            )

        super().__init__(model)

    def _init_chat_model(self, model, **kwargs) -> BaseChatModel:
        return ChatOpenAI(
            model=model,
            api_key=Config.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
            **kwargs,
        )
