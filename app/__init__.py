import logging
from logging.handlers import SMTPHandler

from flask import Flask

from config import Config
from app.database import db

app_name = Config.APP_NAME

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.user import bp as user_bp
    app.register_blueprint(user_bp)


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
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app
