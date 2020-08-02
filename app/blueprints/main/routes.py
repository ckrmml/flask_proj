from flask import render_template

from app import app_name
from app.blueprints.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='home', content='Hello, World!', app_name=app_name)
