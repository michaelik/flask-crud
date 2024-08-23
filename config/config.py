import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DB_USERNAME = os.environ.get('DB_USERNAME', 'default_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_password')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL',
                                             f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/flask_db')


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')


config = {
    'development': DevelopmentConfig,
    # 'production': ProductionConfig
}
