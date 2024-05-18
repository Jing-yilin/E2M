from dotenv import load_dotenv
import os

load_dotenv()


class DefaultConfig:
    DEBUG = False
    TESTING = False

    # converter
    CONVERTER = os.environ.get("CONVERTER", "default")  # unstructured / default

    # base api url
    API_URL = os.environ.get("API_URL", "http://127.0.0.1:8765")
