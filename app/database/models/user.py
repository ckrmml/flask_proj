import jwt

from time import time
from hashlib import md5
from datetime import datetime

# import app
from app import db, login
from app.database import Base

from flask import current_app
from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    mail = Column(String(120), index=True, unique=True)
    hash = Column(String(128))
    deleted = Column(Boolean, default=False)
    creation = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def avatar(self, size):
        digest = md5(self.mail.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_token(self, token_type='', expires_in=600):
        return jwt.encode(
            {f'{token_type}': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(token, token_type=''):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])[f'{token_type}']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'<User {self.name}>'
