import logging
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.config import Config

logger = logging.getLogger(__name__)


class AnthropicChainHandler(BaseChainHandler):
    """
    Anthropic Chain Handler

    You can set the following environment variables to use the Anthropic API:
    - ANTHROPIC_API_KEY: Your Anthropic API key

    """

    def __init__(self, model: str = None):
        if model is not None:
            model = model
            logger.info(f"Using Anthropic model: {model}")
        elif Config.ANTHROPIC_DEFAULT_MODEL:
            model = Config.ANTHROPIC_DEFAULT_MODEL
            logger.info(f"Using default Anthropic model: {model}")
        else:
            model = "claude-3-opus-20240229"
            logger.info(
                f"You have not specified an Anthropic model. Using default model: {model}"
            )

        super().__init__(model)

    def init_chat_model(self, model) -> BaseChatModel:
        return ChatAnthropic(model=model, api_key=Config.ANTHROPIC_API_KEY)
