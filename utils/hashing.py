import hmac
import hashlib
import os


def hash_string_sha256(msg: str):
    hashed = hmac.new(os.getenv('SECRET_KEY').encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()
    return hashed
