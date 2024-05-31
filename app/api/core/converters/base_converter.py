from abc import abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from api.core.parsers.base_parser import ParserMode

from typing import Union, List

# FikeLikeType includes str, bytes, and file-like objects
FileLikeType = Union[str | Path]  # todo: more types


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

    file: FileLikeType = Field(..., title="File path")
    parse_mode: ParserMode = Field(ParserMode.AUTO, title="Parser mode")

    # file not empty
    @field_validator("file")
    def check_file_exists(cls, v):
        if not Path(v).exists():
            raise ValueError(f"File {v} does not exist")
        return v

    @abstractmethod
    def convert(self, **kwargs) -> str:
        pass

    def to_dict(self):
        return self.model_dump()

    def rm_file(self):
        if Path(self.file).exists():
            Path(self.file).unlink()
            return True
