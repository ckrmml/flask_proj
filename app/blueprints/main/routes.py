from flask import render_template

from app import db #, app
from app.blueprints.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.tmpl', title='home')
