import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    APP_NAME = 'testname for app'

    # >>> import secrets
    # >>> secrets.token_urlsafe()
    SECRET_KEY = 'Iw4nilrNMIYuhsSBQxnxhj0ntOPCjA3Ydmia4li4w4s'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_proj:1234@localhost:3306/test'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = None
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ADMINS = ['admin@test.de']

    LOG_DIR = 'logs'

    ENABLE_LOGIN = True

    ENABLE_REGISTRATION = True
    CONFIRM_REGISTRATION = False
    MAIL_ON_CONFIRMATION = False
    LOGIN_ON_CONFIRMATION = True

    ENABLE_PASSWORD_RESET = False
