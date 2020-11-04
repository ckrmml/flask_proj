from datetime import datetime

from flask import render_template

from flask_login import login_required
from flask_login import current_user

from app import db

from app.blueprints.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.commit()


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('main/index.tmpl', title='home')
