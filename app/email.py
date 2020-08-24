from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_token(token_type='reset_password')
    send_email(f'[{current_app.config["APP_NAME"]}] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.mail],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token, app=current_app),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token, app=current_app))


def send_account_confirmation_mail(user):
    token = user.get_token(token_type='confirm_registration')
    send_email(f'[{current_app.config["APP_NAME"]}] Confirm your account',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.mail],
               text_body=render_template('email/confirm_account.txt',
                                         user=user, token=token, app=current_app),
               html_body=render_template('email/confirm_account.html',
                                         user=user, token=token, app=current_app))


def send_account_confirmed_mail(user):
    send_email(f'[{current_app.config["APP_NAME"]}] Your account has been confirmed',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.mail],
               text_body=render_template('email/account_confirmed.txt',
                                         user=user, app=current_app),
               html_body=render_template('email/account_confirmed.html',
                                         user=user, app=current_app))
