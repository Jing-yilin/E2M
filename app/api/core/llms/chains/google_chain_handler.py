import logging
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class GoogleChainHandler(BaseChainHandler):
    """
    Google Chain Handler

    You can set the following environment variables to use the Google API:
    - GOOGLE_API_KEY: Your Google API key

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Google model: {model}")
        elif Config.OPENAI_DEFAULT_MODEL:
            model = Config.OPENAI_DEFAULT_MODEL
            logger.info(f"Using default Google model: {model}")
        else:
            model = "gemini-pro"
            logger.info(
                f"You have not specified an Google model. Using default model: {model}"
            )

        super().__init__(model)

    def _init_chat_model(self, model, **kwargs) -> BaseChatModel:
        return GoogleGenerativeAI(model=model, api_key=Config.GOOGLE_API_KEY, **kwargs)
