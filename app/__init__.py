import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from app.database import db

mail = Mail()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

toolbar = DebugToolbarExtension()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.default')
    app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_pyfile('config.py')

    mail.init_app(app)
    login.init_app(app)

    if os.getenv("FLASK_ENV") == 'development':
        toolbar.init_app(app)

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.blueprints.errors import bp as error_bp
    app.register_blueprint(error_bp)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=f'{app.config["APP_NAME"]} Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists(app.config['LOG_DIR']):
            os.mkdir(app.config['LOG_DIR'])

        file_handler = RotatingFileHandler(f'{app.config["LOG_DIR"]}/{app.config["APP_NAME"].replace(" ", "_")}.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{app.config["APP_NAME"]} startup')

    return app
