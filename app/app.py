import logging

from flask import Flask, jsonify
from flasgger import Swagger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

import versions


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


setup_logging()

logger = logging.getLogger(__name__)


def create_app():
    from api.blueprints.v1.routes import bp as api_v1_bp
    from api.blueprints.v1.models import db, migrate

    app = Flask(__name__)

    from api.config import Config

    API_URL = Config.API_URL

    logger.debug(f"Config: {Config}")

    app.config.from_object(Config)

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
            .----------------------------------.
            |      _____   ____    __  __      |
            |     | ____| |___ \  |  \/  |     |
            |     |  _|     __) | | |\/| |     |
            |     | |___   / __/  | |  | |     |
            |     |_____| |_____| |_|  |_|     |
            '----------------------------------'
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


app = create_app()


if __name__ == "__main__":
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import run_simple

    application = DispatcherMiddleware(app.wsgi_app)

    run_simple("0.0.0.0", 8765, application)
