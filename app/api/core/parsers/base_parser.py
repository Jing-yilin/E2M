from enum import Enum


class ParserMode(Enum):

    AUTO = "auto"
    GENERAL = "general"
    BOOK = "book"
    LAW = "law"
    MANUAL = "manual"
    PAPER = "paper"
    RESUME = "resume"
    QA = "qa"  # question and answer
    TABLE = "table"


class BaseParser:
    def __init__(self, mode: ParserMode):
        self.mode = mode

    def parse(self, file_path: str) -> str:
        raise NotImplementedError("parse method must be implemented")
