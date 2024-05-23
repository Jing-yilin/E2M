import api.config.development as development
import api.config.production as production

import os
from dotenv import load_dotenv

load_dotenv()

config_name = os.getenv("FLASK_ENV", "default")

Config = None

if config_name == "default":
    from api.config.default import config

    Config = config
elif config_name == "development":
    from api.config.development import config

    Config = config
elif config_name == "production":
    from api.config.production import config

    Config = config
