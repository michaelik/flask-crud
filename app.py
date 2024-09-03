from os import environ
from flask import Flask
from flask_pymongo import PyMongo
from models.db import db
from flask_marshmallow import Marshmallow
from flask_restful import Api
from controllers.user_controller import UserController
from errors.error_handlers import register_error_handlers
from config import config, LogConfig
import flask_profiler
from prometheus_flask_exporter import PrometheusMetrics

logger = LogConfig.configure_logging()
mongo = PyMongo()


def create_app(environment: str = 'development'):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    configure_app(app, environment)
    initialize_extensions(app)
    setup_routes(app)
    setup_error_handlers(app)
    configure_prometheus_metrics(app, environment)
    configure_profiler(app)

    return app


def configure_app(app: Flask, environment: str = 'development'):
    """
    Configure the Flask application based on the provided environment.
    """
    if environment == 'development':
        app.config.from_object(config['development'])
    elif environment == 'testing':
        app.config.from_object(config['testing'])
    elif environment == 'production':
        app.config.from_object(config['production'])


def configure_profiler(app: Flask):
    """
    Configure Flask-Profiler based on the application's configuration.
    """
    profiler_config = app.config.get('PROFILER_CONFIG')
    if profiler_config and profiler_config.get("enabled", False):
        mongo.init_app(app)
        app.config["flask_profiler"] = profiler_config
        flask_profiler.init_app(app)


def initialize_extensions(app: Flask):
    """
    Initialize Flask extensions and set up the database.
    """
    db.init_app(app)
    Marshmallow(app)
    Api(app)

    # Only create tables in the PostgreSQL database for the main app
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


def configure_prometheus_metrics(app: Flask, environment: str = 'development'):
    """
    Register Prometheus metrics
    """
    if environment == 'development':
        metrics = PrometheusMetrics(app, path=app.config['PROMETHEUS_METRICS_ENDPOINT'])
        logger.debug(f"Prometheus metrics endpoint registered at "
                     f"{app.config['PROMETHEUS_METRICS_ENDPOINT']}")
        metrics.info('app_info', 'Application info', version='1.0.0')


def setup_error_handlers(app: Flask):
    """
    Register error handlers with the Flask application.
    """
    register_error_handlers(app)


if __name__ == '__main__':
    env = environ.get('FLASK_ENV', 'development')
    flask_app = create_app(environment=env)
    APP_PORT = int(environ.get("APP_PORT", 4000))  # Default port to 4000 if not set
    APP_HOST = environ.get("APP_HOST", "0.0.0.0")  # Default host to 0.0.0.0 if not set
    APP_DEBUG = environ.get("APP_DEBUG", "True").lower() == 'true'  # Convert to boolean
    flask_app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
