from flask import Blueprint

bp = Blueprint('main', __name__,
               template_folder='templates',
               static_folder='static'
              )

from app.blueprints.main import routes
