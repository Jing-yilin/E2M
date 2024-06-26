import logging
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class TongyiChainHandler(BaseChainHandler):
    """
    Tongyi Chain Handler

    You can set the following environment variables to use the Tongyi API:
    - DASHSCOPE_API_KEY: Your Tongyi API key
        Generate your api key from: https://dashscope.console.aliyun.com/apiKey
    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Tongyi model: {model}")
        elif Config.BAICHUAN_DEFAULT_MODEL:
            model = Config.BAICHUAN_DEFAULT_MODEL
            logger.info(f"Using default Tongyi model: {model}")
        else:
            model = "qwen-turbo"
            logger.info(
                f"You have not specified an Tongyi model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatTongyi(model=model, api_key=Config.DASHSCOPE_API_KEY)
