from flask import Flask

from config import Config

app_name = Config.APP_NAME
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
