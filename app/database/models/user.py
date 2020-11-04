import jwt

from time import time
from hashlib import md5
from datetime import datetime

from app import db
from app import utils
from app import login

from app.database import Base

from flask import current_app

from flask_login import UserMixin

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    mail = Column(String(120), index=True, unique=True)
    hash = Column(String(128))
    creation = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    confirmed = Column(Boolean, default=False)
    confirmed_on = Column(DateTime)
    active = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    deleted_on = Column(DateTime)
    # NOTE: FINISH THIS
    # hidden = Column(Boolean, default=False)

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def confirm(self):
        self.confirmed = True
        self.confirmed_on = datetime.utcnow()
        self.active = True

    def avatar(self, size):
        digest = md5(self.mail.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def delete(user):
        user.name = utils.get_uuid(f'{user.name}{user.id}')
        user.mail = utils.get_uuid(f'{user.mail}{user.id}')
        user.hash = utils.get_uuid(f'{user.hash}{user.id}')
        user.creation = utils.get_uuid(f'{user.creation}{user.id}')
        user.last_seen = utils.get_uuid(f'{user.last_seen}{user.id}')
        user.confirmed = False
        user.confirmed_on = utils.get_uuid(f'{user.confirmed_on}{user.id}')
        user.active = False
        user.deleted = True
        user.deleted_on = datetime.utcnow()
        db.commit()

    @staticmethod
    def verify_token(token, token_type):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])[f'{token_type}']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'<User {self.name}>'
