import logging

# from rich.logging import RichHandler
import argparse

from flask import Flask, jsonify
from flasgger import Swagger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from api.config import Config, default
import versions

# load environment variables
API_URL = Config.API_URL


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
        # handlers=[RichHandler()],
    )


setup_logging()

logger = logging.getLogger(__name__)

logger.debug(f"Config: {Config}")


def create_app(config_class=default.DefaultConfig()):
    from api.blueprints.v1.routes import bp as api_v1_bp
    from api.blueprints.v1.models import db, migrate

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Create engine
    try:
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        conn = engine.connect()
        logger.info("Database connected successfully")
        conn.close()
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/api/v1/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
    }

    Swagger(app, config=swagger_config)  # init swagger

    logo_ascii = """
                    ┌──────────────────────────────────────────┐
                    │                                    ____  │
                    │    ,---,.       ,----,           ,'  , `.│
                    │  ,'  .' |     .'   .' \       ,-+-,.' _ |│
                    │,---.'   |   ,----,'    |   ,-+-. ;   , ||│
                    │|   |   .'   |    :  .  ;  ,--.'|'   |  ;|│
                    │:   :  |-,   ;    |.'  /  |   |  ,', |  ':│
                    │:   |  ;/|   `----'/  ;   |   | /  | |  ||│
                    │|   :   .'     /  ;  /    '   | :  | :  |,│
                    │|   |  |-,    ;  /  /-,   ;   . |  ; |--' │
                    │'   :  ;/|   /  /  /.`|   |   : |  | ,    │
                    │|   |    \ ./__;      :   |   : '  |/     │
                    │|   :   .' |   :    .'    ;   | |`-'      │
                    │|   | ,'   ;   | .'       |   ;/          │
                    │`----'     `---'          '---'           │
                    └──────────────────────────────────────────┘
"""

    logger.info("+-----------------------------------------------------------+")
    logger.info("Welcome to E2M API")
    logger.info(logo_ascii)
    logger.info(f"🚀API: {API_URL}/api/v1/")
    logger.info(f"🚀API doc: {API_URL}/swagger/")
    logger.info(f"The github repo: {versions.__github__}")
    logger.info("+-----------------------------------------------------------+")

    # version endpoint
    @app.route("/version")
    def version():
        return jsonify(
            {
                "version": versions.__version__,
                "description": versions.__description__,
            }
        )

    return app


if __name__ == "__main__":
    app = create_app(Config)

    # enable debug mode by passing --debug
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    port = "8765"
    if args.debug:
        app.run(port=port, debug=True)
    else:
        app.run(port=port, debug=False)
