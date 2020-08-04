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

    return app
