import jwt
import uuid
import random

from time import time

from flask import current_app


def string_to_int(string):
    return int.from_bytes(string.encode("utf-8"), byteorder="big")

def get_uuid(string, uuid_length=10):
    """Returns a random string of length string_length."""
    rd = random.Random()
    rd.seed(string_to_int(string))
    return str(uuid.UUID(int=rd.getrandbits(128))).upper().replace('-','')

def get_token(user, token_type, expires_in=600):
    return jwt.encode(
        {f'{token_type}': user.id, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
