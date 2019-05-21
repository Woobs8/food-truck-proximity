import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    LOGGING_DIR = 'logs'
    LOGGING_INTERVAL_HOURS = 2
    LOGGING_LOG_DURATION = 24
    DEFAULT_SEARCH_RADIUS = 500

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True