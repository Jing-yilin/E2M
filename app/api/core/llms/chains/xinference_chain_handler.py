# import logging
# from langchain_community.llms import Xinference
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
# from langchain_core.runnables.base import RunnableSequence
from api.core.llms.chains.base_chain_handler import BaseChainHandler

# from api.core.llms.prompts import (
#     OCR_FIX_TO_MARKDOWN_PROMPT,
#     OCR_FIX_TO_JSON_PROMPT,
#     EXTRACT_MARKDOWN_PROMPT,
#     EXTRACT_JSON_PROMPT,
#     COMMENT_PROMTPT,
# )
# from api.config import Config

# logger = logging.getLogger(__name__)


class XinferenceChainHandler(BaseChainHandler):
    """
    Xinference Chain Handler

    You can set the following environment variables to use the Xinference API:
    - XINFERENCE_API_KEY: Your Xinference API key

    """

    def __init__(self, model: str = None):
        raise NotImplementedError("XinferenceChainHandler is not implemented yet")
