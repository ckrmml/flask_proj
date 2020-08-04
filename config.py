import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    APP_NAME = 'testname for app'

    # >>> import secrets
    # >>> secrets.token_urlsafe()
    SECRET_KEY = 'Iw4nilrNMIYuhsSBQxnxhj0ntOPCjA3Ydmia4li4w4s'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = None
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ADMINS = ['admin@test.de']

    LOG_DIR = 'logs'
