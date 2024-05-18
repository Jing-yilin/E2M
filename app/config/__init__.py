from .default import DefaultConfig
from .production import ProductionConfig
from .development import DevelopmentConfig
import os
from dotenv import load_dotenv

load_dotenv()


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DefaultConfig,
}

config_name = os.getenv("FLASK_ENV", "default")

Config: DefaultConfig = configs[config_name]
