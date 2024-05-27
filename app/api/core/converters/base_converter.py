from abc import abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel, Field
from api.core.parsers.base_parser import ParserMode

from typing import Union, List

# FikeLikeType includes str, bytes, and file-like objects
FileLikeType = Union[str]  # todo: more types


@dataclass
class MdElement:
    text: str

    @abstractmethod
    def to_md(self) -> str:
        pass


@dataclass
class Header1(MdElement):

    def to_md(self) -> str:
        return f"# {self.text}"


@dataclass
class Header2(MdElement):

    def to_md(self) -> str:
        return f"## {self.text}"


@dataclass
class Header3(MdElement):

    def to_md(self) -> str:
        return f"### {self.text}"


@dataclass
class Paragraph(MdElement):

    def to_md(self) -> str:
        return f"{self.text}\n"


def merge_elements_to_md(elements: List[MdElement]) -> str:
    return "\n".join([element.to_md() for element in elements])


class BaseConverter(BaseModel):

    file: FileLikeType = Field(None, title="File to convert")
    parse_mode: ParserMode = Field(ParserMode.AUTO, title="Parser mode")

    @abstractmethod
    def convert(self, **kwargs) -> str:
        pass

    def to_dict(self):
        return self.model_dump()
