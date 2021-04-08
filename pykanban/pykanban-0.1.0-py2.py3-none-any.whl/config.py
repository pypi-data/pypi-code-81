import os
import datetime

# defining general app configurations and configurations specific to different environments

class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')

class ProductionConfig(Config):
    """Uses production database server."""
    SQLALCHEMY_DATABASE_URI = DATABASE_URL = os.getenv('DATABASE_URL') or 'sqlite:///web.db'

class DevelopmentConfig(Config):
    DEBUG = True
    # DB_SERVER = 'localhost'
    FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
    # SERVER_NAME="127.0.0.1"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL = os.getenv('DATABASE_URL') or 'sqlite:///web.db'
    MAIL_USE_SSL = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB_SERVER = 'localhost'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI=DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY='testing_key'

config = {
    "prod": ProductionConfig,
    "dev": DevelopmentConfig,
    "test": TestingConfig
}