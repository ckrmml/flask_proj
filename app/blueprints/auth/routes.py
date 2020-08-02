from flask import render_template, flash, redirect, url_for

from app import app_name

from app.blueprints.auth import bp
from app.blueprints.auth.forms import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
        form.username.data, form.remember_me.data))
        return redirect( url_for('main.index') )
    return render_template('auth/login.tmpl', title='login', form=form, app_name=app_name)
