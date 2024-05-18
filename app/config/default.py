from dotenv import load_dotenv
import os

load_dotenv()


class DefaultConfig:
    DEBUG = False
    TESTING = False

    # converter
    CONVERTER = os.environ.get("CONVERTER", "default")  # unstructured / default
