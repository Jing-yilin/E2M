import logging
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class ZhipuaiChainHandler(BaseChainHandler):
    """
    Zhipuai Chain Handler

    You can set the following environment variables to use the Zhipuai API:
    - ZHIPUAI_API_KEY: Your Zhipuai API key
        Generate your api key from: https://open.bigmodel.cn

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Zhipuai model: {model}")
        elif Config.ZHIPUAI_DEFAULT_MODEL:
            model = Config.ZHIPUAI_DEFAULT_MODEL
            logger.info(f"Using default Zhipuai model: {model}")
        else:
            model = "glm-4"
            logger.info(
                f"You have not specified an Zhipuai model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatZhipuAI(model=model, api_key=Config.ZHIPUAI_API_KEY)
