import os

class BaseConfig:
    # Statement for enabling the development environment
    DEBUG = True
    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:password@localhost:5432/item-catalog'
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"
    # Secret key for signing cookies
    SECRET_KEY = "secret"
    TESTING = False
    ENVIRONMENT = 'development'
    #


class DevelopmentConfig(BaseConfig):
    ENVIRONMENT = 'development'
    REMOTE_DEBUG_SERVER_HOST = '0.0.0.0'
    REMOTE_DEBUG_SERVER_PORT = '4.4.4.4'