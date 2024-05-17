from flask import Flask, jsonify
from .api.blueprints.v1.views import bp as api_v1_bp
from .config import default
from . import versions


def create_app(config_class=default.DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # register blueprints
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    # version endpoint
    @app.route("/version")
    def version():
        return jsonify(
            {
                "version": versions.__version__,
                "description": versions.__description__,
            }
        )

    # init_extensions(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8765)
