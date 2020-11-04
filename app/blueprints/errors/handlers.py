from flask import render_template
from flask import request

from app import db

from app.blueprints.errors import bp


@bp.errorhandler(403)
def forbidden_error(error):
    return render_template("errors/403.tmpl"), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.tmpl'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.rollback()
    return render_template('errors/500.tmpl'), 500
