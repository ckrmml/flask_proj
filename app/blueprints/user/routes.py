from datetime import datetime

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from app import app_name, db
from app.blueprints.user import bp
from app.database.models import User
from app.blueprints.user.forms import EditProfileForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.commit()


@bp.route('/user/<name>')
@login_required
def profile(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash((f'We could not find a user with the name {name}'))
        return redirect(url_for('main.index'))
    return render_template('user/profile.tmpl', user=user)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.name, current_user.mail)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.mail = form.mail.data
        db.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.profile', name=current_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.mail.data = current_user.mail
    return render_template('user/edit.tmpl', title='Edit Profile',
                           form=form)
