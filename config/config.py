import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Configuration for Development."""
    DB_USERNAME = os.environ.get('DB_USERNAME', 'default_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_password')
    DB_DATABASE = os.environ.get('DB_DATABASE', 'default_database')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DB_URL',
        f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    )


class ProductionConfig(Config):
    """Configuration for Production."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
