from hashlib import md5
from datetime import datetime

from app import db
from app import login
from app.database import Base

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

    def __repr__(self):
        return f'<User {self.name}>'
