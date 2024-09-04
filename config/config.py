from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True

    # Determine if the app is running inside Docker
    IS_DOCKER = environ.get('IS_DOCKER', 'false').lower() == 'true'

    # Set DB_HOST based on the environment
    DB_HOST = 'flask_db' if IS_DOCKER else environ.get('DB_HOST', 'localhost')
    MONGO_DB_HOST = 'flask_mongo' if IS_DOCKER else environ.get('MONGO_DB_HOST', 'localhost')

    """Configuration for Development."""
    DB_USERNAME = environ.get('DB_USERNAME', 'default_user')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'default_password')
    DB_NAME = environ.get('DB_NAME', 'default_database')
    DB_PORT = int(environ.get('DB_PORT', '5432'))

    SQLALCHEMY_DATABASE_URI = environ.get(
        'DB_URL',
        f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20
    }

    environ['DEBUG_METRICS'] = '1'
    PROMETHEUS_METRICS_ENDPOINT = '/my-metrics'

    MONGO_URI = environ.get(
        'MONGO_URI',
        f'mongodb://{MONGO_DB_HOST}:27017/flask_profiler'
    )

    PROFILER_CONFIG = {
        "enabled": True,
        "storage": {
            "engine": "mongodb",
            "db": "flask_profiler",
            "collection": "profiler_data",
            "MONGO_URL": MONGO_URI
        },
        "basicAuth": {
            "enabled": True,
            "username": environ.get('PROFILER_USERNAME', 'admin'),
            "password": environ.get('PROFILER_PASSWORD', 'password')
        },
        "ignore": [
            "^/static/.*"
        ]
    } if DEBUG else None


class TestingConfig(Config):
    """Configuration for Testing."""
    DEBUG = False  # It's generally good practice to disable debugging in tests
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Configuration for Production."""
    DEBUG = False  # Disable debugging in production
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
