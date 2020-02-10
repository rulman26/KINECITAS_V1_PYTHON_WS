import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 4005)

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '1561561561'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = PORT


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    HOST = HOST
    PORT = PORT
    TESTING = True


class ProductionConfig(Config):
    HOST = HOST
    PORT = PORT
    DEBUG = False