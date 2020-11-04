from datetime import datetime

from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app
from flask import abort

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from werkzeug.urls import url_parse

from app import db
from app import utils

from app.email import send_password_reset_email
from app.email import send_account_confirmation_mail
from app.email import send_account_confirmed_mail

from app.blueprints.auth import bp
from app.blueprints.auth.forms import LoginForm
from app.blueprints.auth.forms import RegistrationForm
from app.blueprints.auth.forms import ResetPasswordRequestForm
from app.blueprints.auth.forms import ResetPasswordForm

from app.database.models import User
from app.database.queries import is_unique_name
from app.database.queries import is_unique_mail


@bp.route('/login', methods=['GET', 'POST'])
def login():
    config = current_app.config

    if not config['ENABLE_LOGIN']: abort(404)

    if current_user.is_authenticated:
        return redirect( url_for('main.index') )

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        if config['CONFIRM_REGISTRATION'] and not user.confirmed:
            flash('Your account has not been verified. Please check your mails and click the link')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.tmpl', title='login', form=form,
                           register=config['ENABLE_REGISTRATION'],
                           reset=config['ENABLE_PASSWORD_RESET'])


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    config = current_app.config
    if not config['ENABLE_REGISTRATION']:
        abort(404)

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if not is_unique_name(form.name.data):
            flash(f'Please choose another username')
            return redirect(url_for('auth.register'))
        if not is_unique_mail(form.mail.data):
            flash(f'Mail already in use. If this is you, you can reset your password to regain access')
            return redirect(url_for('auth.register'))

        user = User(name=form.name.data, mail=form.mail.data)
        user.set_password(form.password.data)
        db.add(user)
        db.commit()

        flash('Congratulations, you are now a registered user!')
        if not config['CONFIRM_REGISTRATION']:
            user.confirm()
            db.commit()
            if config['LOGIN_ON_CONFIRMATION']:
                login_user(user, remember=False)
                return redirect(url_for('main.index'))
        send_account_confirmation_mail(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.tmpl', title='Register', form=form)


@bp.route('/reset', methods=['GET', 'POST'])
def request_password_reset():
    config = current_app.config
    if not config['ENABLE_PASSWORD_RESET']: abort(404)

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset.tmpl',
                           title='Reset Password', form=form)


@bp.route('/<token>/reset', methods=['GET', 'POST'])
def perform_password_reset(token):
    config = current_app.config
    if not config['ENABLE_PASSWORD_RESET']: abort(404)

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_token(token, token_type='reset_password')

    if not user:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/perform_reset.tmpl', form=form)


@bp.route('/<token>/confirm', methods=['GET', 'POST'])
def confirm_registration(token):
    config = current_app.config
    if not config['ENABLE_REGISTRATION']: abort(404)
    if not config['CONFIRM_REGISTRATION']: abort(404)

    user = User.verify_token(token, token_type='confirm_registration')

    if not user:
        return redirect(url_for('main.index'))
    else:
        user.confirm()
        db.commit()
        flash('Your account has been confirmed.')

        if config['MAIL_ON_CONFIRMATION']:
            send_account_confirmed_mail(user)

        if config['LOGIN_ON_CONFIRMATION']:
            login_user(user, remember=False)
            return redirect(url_for('main.index'))

        return redirect(url_for('auth.login'))
    return render_template('auth/confirm_registration.tmpl')
