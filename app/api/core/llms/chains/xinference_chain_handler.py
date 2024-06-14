
# llm = Xinference(
#     server_url="http://0.0.0.0:9997",
#     model_uid = {model_uid} # replace model_uid with the model UID return from launching the model
# )

# llm(
#     prompt="Q: where can we visit in the capital of France? A:",
#     generate_config={"max_tokens": 1024, "stream": True},
# )

import logging
from langchain_community.llms import Xinference
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables.base import RunnableSequence
from api.core.llms.chains.base_chain_handler import BaseChainHandler
from api.core.llms.prompts import (
    OCR_FIX_TO_MARKDOWN_PROMPT,
    OCR_FIX_TO_JSON_PROMPT,
    EXTRACT_MARKDOWN_PROMPT,
    EXTRACT_JSON_PROMPT,
    ADDITIONAL_PROMTPT,
)
from api.config import Config

logger = logging.getLogger(__name__)


class XinferenceChainHandler(BaseChainHandler):
    """
    Xinference Chain Handler

    You can set the following environment variables to use the Xinference API:
    - XINFERENCE_API_KEY: Your Xinference API key

    """

    @NotImplemented
    def __init__(self, model: str = None):
        pass