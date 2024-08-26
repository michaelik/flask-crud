import os
from os import environ
from flask import Flask
from db import db
from flask_marshmallow import Marshmallow
from flask_restful import Api
from controllers.user_controller import UserController
from errors.error_handlers import register_error_handlers
from config import config, LogConfig

logger = LogConfig.configure_logging()


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    configure_app(app)
    initialize_extensions(app)
    setup_routes(app)
    setup_error_handlers(app)
    return app


def configure_app(app: Flask):
    """
    Configure the Flask application from environment variables.
    """
    env = environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    logger.info("Using configuration: %s", config[env].__dict__)


def initialize_extensions(app: Flask):
    """
    Initialize Flask extensions and set up the database.
    """
    db.init_app(app)
    Marshmallow(app)
    Api(app)

    with app.app_context():
        try:
            db.create_all()  # Create tables if they do not exist
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")


def setup_routes(app: Flask):
    """
    Register routes and API resources with the Flask application.
    """
    api = Api(app)
    api.add_resource(UserController, '/users', '/users/<int:id>')


def setup_error_handlers(app: Flask):
    """
    Register error handlers with the Flask application.
    """
    register_error_handlers(app)


if __name__ == '__main__':
    flask_app = create_app()
    APP_PORT = int(os.getenv("APP_PORT", 4000))  # Default port to 4000 if not set
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # Default host to 0.0.0.0 if not set
    APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == 'true'  # Convert to boolean
    flask_app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
