from pydantic import Field
from pydantic_settings import BaseSettings
import json


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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    def to_dict(self):
        return self.model_dump(mode="json")


config = DefaultConfig()
