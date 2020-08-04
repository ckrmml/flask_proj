from flask import ( render_template,
                    flash,
                    redirect,
                    url_for,
                    request
                  )

from flask_login import current_user, login_user, logout_user

from werkzeug.urls import url_parse

from app import app_name, db
from app.blueprints.auth import bp
from app.blueprints.auth.forms import LoginForm, RegistrationForm
from app.database.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('main.index') )
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.tmpl', title='login', form=form, app_name=app_name)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, mail=form.mail.data)
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.tmpl', title='Register', form=form)
