from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict


class DefaultConfig(BaseSettings):
    DEBUG: bool = Field(default=True, description="Enable or disable debug mode")
    TESTING: bool = Field(default=False, description="Enable or disable testing mode")

    # converter
    CONVERTER: str = Field(
        default="default", env="CONVERTER", description="Converter to use"
    )  # unstructured / default

    # base api url
    API_URL: str = Field(
        default="http://127.0.0.1:8765", env="API_URL", description="Base API URL"
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
