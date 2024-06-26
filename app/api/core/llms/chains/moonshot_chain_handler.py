import logging
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class MoonshotChainHandler(BaseChainHandler):
    """
    Moonshot Chain Handler

    You can set the following environment variables to use the Moonshot API:
    - MOONSHOT_API_KEY: Your Moonshot
        Generate your api key from: https://platform.moonshot.cn/console/api-keys


    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Moonshot model: {model}")
        elif Config.MOONSHOT_DEFAULT_MODEL:
            model = Config.MOONSHOT_DEFAULT_MODEL
            logger.info(f"Using default Moonshot model: {model}")
        else:
            model = "moonshot-v1-128k"
            logger.info(
                f"You have not specified an Moonshot model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return MoonshotChat(model=model, api_key=Config.MOONSHOT_API_KEY)
