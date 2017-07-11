from os import path
from os import urandom
from binascii import hexlify


APP_DIR = path.abspath(path.dirname(__file__))

SECRET_KEY = hexlify(urandom(32))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + APP_DIR + "/database.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
