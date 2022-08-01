import base64
import hashlib
import hmac
import random
import string

import ujson

from game.errors import HttpError

_HMAC_KEY = ''.join(random.choice(string.printable) for _ in range(16)).encode()


def generate_token(data: dict) -> str:
    token_b64 = base64.b64encode(ujson.dumps(data).encode())
    token_hash = get_sha(token_b64)

    return f"{token_b64.decode()}.{token_hash}"


def get_sha(token_b64: bytes) -> str:
    return hmac.new(_HMAC_KEY, token_b64, hashlib.sha1).hexdigest()


def _abort():
    raise HttpError(status=403, message=HttpError.Message(text="token invalid"))


def check_token(token: str):
    if not token:
        _abort()

    split = token.split(".")

    if len(split) != 2:
        _abort()

    token_b64, token_hash = split
    if token_hash != get_sha(token_b64.encode()):
        _abort()

    return ujson.loads(base64.b64decode(token_b64.encode()).decode())
