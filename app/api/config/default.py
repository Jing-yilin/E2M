from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict


class DefaultConfig(BaseSettings):
    DEBUG: bool = Field(default=True, description="Enable or disable debug mode")
    TESTING: bool = Field(default=False, description="Enable or disable testing mode")

    TRANSFORMERS_CACHE: str = Field(
        default="./transformers_cache",
        env="TRANSFORMERS_CACHE",
        description="Transformers cache directory",
    )

    # converters
    # pydantic.errors.PydanticUserError: Field 'DOC_CONVERTER' requires a type annotation
    DOC_CONVERTER: str = Field(
        default="default", env="DOC_CONVERTER", description="DOC Converter to use"
    )  # unstructured / default
    DOCX_CONVERTER: str = Field(
        default="default", env="DOCX_CONVERTER", description="DOCX Converter to use"
    )  # unstructured / default
    PDF_CONVERTER: str = Field(
        default="default", env="PDF_CONVERTER", description="PDF Converter to use"
    )  # unstructured / default
    TXT_CONVERTER: str = Field(
        default="default", env="TXT_CONVERTER", description="TXT Converter to use"
    )  # unstructured / default
    HTML_CONVERTER: str = Field(
        default="default", env="HTML_CONVERTER", description="HTML Converter to use"
    )  # unstructured / jina / default
    HTM_CONVERTER: str = Field(
        default="default", env="HTM_CONVERTER", description="HTM Converter to use"
    )  # unstructured / jina / default

    JPG_CONVERTER: str = Field(
        default="default", env="JPG_CONVERTER", description="JPG Converter to use"
    )  # unstructured / default
    JPEG_CONVERTER: str = Field(
        default="default", env="JPEG_CONVERTER", description="JPEG Converter to use"
    )  # unstructured / default
    PNG_CONVERTER: str = Field(
        default="default", env="PNG_CONVERTER", description="PNG Converter to use"
    )  # unstructured / default
    GIF_CONVERTER: str = Field(
        default="default", env="GIF_CONVERTER", description="GIF Converter to use"
    )  # unstructured / default
    SVG_CONVERTER: str = Field(
        default="default", env="SVG_CONVERTER", description="SVG Converter to use"
    )  # unstructured / default

    CSV_CONVERTER: str = Field(
        default="default", env="CSV_CONVERTER", description="CSV Converter to use"
    )  # unstructured / default
    XLSX_CONVERTER: str = Field(
        default="default", env="XLSX_CONVERTER", description="XLSX Converter to use"
    )  # unstructured / default
    XLS_CONVERTER: str = Field(
        default="default", env="XLS_CONVERTER", description="XLS Converter to use"
    )  # unstructured / default

    MP3_CONVERTER: str = Field(
        default="default", env="MP3_CONVERTER", description="MP3 Converter to use"
    )  # default
    WAV_CONVERTER: str = Field(
        default="default", env="WAV_CONVERTER", description="WAV Converter to use"
    )  # default
    FLAC_CONVERTER: str = Field(
        default="default", env="FLAC_CONVERTER", description="FLAC Converter to use"
    )  # default

    MP4_CONVERTER: str = Field(
        default="default", env="MP4_CONVERTER", description="MP4 Converter to use"
    )  # default
    AVI_CONVERTER: str = Field(
        default="default", env="AVI_CONVERTER", description="AVI Converter to use"
    )  # default
    MKV_CONVERTER: str = Field(
        default="default", env="MKV_CONVERTER", description="MKV Converter to use"
    )  # default

    # base api url
    API_URL: str = Field(
        default="http://127.0.0.1:8765", env="API_URL", description="Base API URL"
    )
    WEB_URL: str = Field(
        default="http://127.0.0.1:3000", env="WEB_URL", description="Base WEB URL"
    )

    # DB_USER: str = Field(default="e2m", env="DB_USER", description="Database user")
    # DB_PASSWORD: str = Field(
    #     default="password", env="DB_PASSWORD", description="Database password"
    # )
    # DB_HOST: str = Field(
    #     default="localhost", env="DB_HOST", description="Database host"
    # )
    # DB_NAME: str = Field(default="e2m_db", env="DB_NAME", description="Database name")

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI: str = Field(
        default="postgresql+psycopg2://e2m:password@localhost/e2m_db",
        env="SQLALCHEMY_DATABASE_URI",
        description="Database URI",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(
        default=False, description="Track modifications"
    )

    # SQLAlchemy binds for multiple databases
    # SQLALCHEMY_BINDS: Dict[str, str] = Field(
    #     default={"e2m_db": "postgresql+psycopg2://e2m:password@localhost/e2m_db"},
    #     env="SQLALCHEMY_BINDS",
    #     description="SQLAlchemy binds for multiple databases",
    # )
    SQLALCHEMY_BINDS: Dict[str, str] = {
        "e2m_db": "postgresql+psycopg2://e2m:password@localhost/e2m_db"
    }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.model_dump_json()}>"

    def to_dict(self) -> dict:
        return self.model_dump_json()

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


config = DefaultConfig()
