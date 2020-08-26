import uuid
import random

def string_to_int(string):
    return int.from_bytes(string.encode("utf-8"), byteorder="big")

def get_deleted_uuid(string, uuid_length=10):
    """Returns a random string of length string_length."""
    rd = random.Random()
    rd.seed(string_to_int(string))
    return str(uuid.UUID(int=rd.getrandbits(128))).upper().replace('-','')
