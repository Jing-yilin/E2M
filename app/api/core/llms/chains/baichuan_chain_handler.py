import logging
from langchain_community.chat_models.baichuan import ChatBaichuan
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class BaichuanChainHandler(BaseChainHandler):
    """
    Baichuan Chain Handler

    You can set the following environment variables to use the Baichuan API:
    - BAICHUAN_API_KEY: Your Baichuan API key
        Generate your api key from: https://platform.baichuan-ai.com/console/apikey
    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Baichuan model: {model}")
        elif Config.BAICHUAN_DEFAULT_MODEL:
            model = Config.BAICHUAN_DEFAULT_MODEL
            logger.info(f"Using default Baichuan model: {model}")
        else:
            model = "Baichuan3-Turbo"
            logger.info(
                f"You have not specified an Baichuan model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatBaichuan(model=model, api_key=Config.BAICHUAN_API_KEY)
