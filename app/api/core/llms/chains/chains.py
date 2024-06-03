from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables.base import RunnableSequence
from api.core.llms.prompts.prompts import (
    OCR_FIX_TO_MARKDOWN_PROMPT,
    OCR_FIX_TO_JSON_PROMPT,
    EXTRACT_MARKDOWN_PROMPT,
    EXTRACT_JSON_PROMPT,
)
import hashlib


class ChainHandler:
    # singleton

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ChainHandler, cls).__new__(cls)
            cls.instance.chains = {}
            cls.instance.model = "gpt-3.5-turbo"
        return cls.instance

    @classmethod
    def set_model(cls, model):
        cls.model = model

    @classmethod
    def ocr_fix_to_markdown_chain(cls, model=None) -> RunnableSequence:
        if model is None:
            model = cls.model
        hash_key = _get_hash_key(model=model, chain_name="ocr_fix_to_markdown")
        if hash_key not in cls().chains:
            chat_model = ChatOpenAI(model=model)
            prompt_template = ChatPromptTemplate.from_messages(
                [("system", OCR_FIX_TO_MARKDOWN_PROMPT)]
            )
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            cls().chains[hash_key] = chain
        return cls().chains[hash_key]

    @classmethod
    def ocr_fix_to_json_chain(cls, model=None) -> RunnableSequence:
        if model is None:
            model = cls.model
        hash_key = _get_hash_key(model=model, chain_name="ocr_fix_to_json")
        if hash_key not in cls().chains:
            chat_model = ChatOpenAI(model=model)
            prompt_template = ChatPromptTemplate.from_messages(
                [("system", OCR_FIX_TO_JSON_PROMPT)]
            )
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            cls().chains[hash_key] = chain
        return cls().chains[hash_key]

    @classmethod
    def extract_markdown_chain(cls, model=None) -> RunnableSequence:
        if model is None:
            model = cls.model
        hash_key = _get_hash_key(model=model, chain_name="extract_markdown")
        if hash_key not in cls().chains:
            chat_model = ChatOpenAI(model=model)
            prompt_template = ChatPromptTemplate.from_messages(
                [("system", EXTRACT_MARKDOWN_PROMPT)]
            )
            parser = StrOutputParser()
            chain = prompt_template | chat_model | parser
            cls().chains[hash_key] = chain
        return cls().chains[hash_key]

    @classmethod
    def extract_json_chain(cls, model=None) -> RunnableSequence:
        if model is None:
            model = cls.model
        hash_key = _get_hash_key(model=model, chain_name="extract_json")
        if hash_key not in cls().chains:
            chat_model = ChatOpenAI(model=model)
            prompt_template = ChatPromptTemplate.from_messages(
                [("system", EXTRACT_JSON_PROMPT)]
            )
            parser = JsonOutputParser()
            chain = prompt_template | chat_model | parser
            cls().chains[hash_key] = chain
        return cls().chains[hash_key]


def _get_hash_key(*args, **kwargs):
    hash_key = hashlib.md5(f"{args}{kwargs}".encode()).hexdigest()
    return hash_key
