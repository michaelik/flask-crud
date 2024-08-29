import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    CSRF_ENABLED = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Configuration for Development."""
    DB_USERNAME = os.environ.get('DB_USERNAME', 'default_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_password')
    DB_NAME = os.environ.get('DB_NAME', 'default_database')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', '5432'))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DB_URL',
        f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


class TestingConfig(Config):
    """Configuration for Testing."""
    DEBUG = False  # It's generally good practice to disable debugging in tests
    TESTING = True
    DB_NAME = 'test-db.db'
    # DB_NAME = 'test-db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    # SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:@localhost:3306/{DB_NAME}'
    # SQLALCHEMY_BINDS = f'sqlite:///{DB_NAME}'


class ProductionConfig(Config):
    """Configuration for Production."""
    DEBUG = False  # Disable debugging in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')  # Use an in-memory database for testing


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
