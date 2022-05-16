import os
import datetime

from dotenv import load_dotenv
from os.path import join, dirname, normpath
from sqlalchemy.engine.url import URL

if 'NODE_ENV' not in os.environ or not os.environ['NODE_ENV'] == 'production':
    load_dotenv(normpath(join(dirname(__file__), '../.local.env')))


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')


DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

DB_URL = URL(
    drivername='postgresql',
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

def _cast_token_expires(value, unit='days'):
    try:
        return datetime.timedelta(**{unit: int(os.getenv(value))})
    except ValueError:
        pass
    try:
        return bool(os.getenv(value))
    except ValueError:
        raise ValueError(f'{os.getenv(value)} is not int or bool value')


SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_PROTOCOL = os.getenv('SERVER_PROTOCOL')


SERVER_HOSTNAME = (
    SERVER_PROTOCOL + "://" + SERVER_HOST + ":" + SERVER_PORT + "/"
)

REFRESH_TOKEN_EXPIRES = _cast_token_expires('REFRESH_TOKEN_EXPIRES', 'days')
ACCESS_TOKEN_EXPIRES = _cast_token_expires('ACCESS_TOKEN_EXPIRES', 'minutes')

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_DISPLAY_NAME = os.getenv('ADMIN_DISPLAY_NAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

MEDIA_FOLDER = os.getenv('MEDIA_FOLDER')
MEDIA_URI = os.getenv('MEDIA_URI')

TESTING = bool(os.getenv('TESTING', False))

if TESTING:
    DB_USER = 'erpsystem_test_user'
    DB_PASSWORD = 'erpsystem_test_user'
    DB_DATABASE = 'erpsystem_test'

    DB_URL = URL(
        drivername='postgresql',
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )


USE_SSL = os.getenv('USE_SSL', False)
