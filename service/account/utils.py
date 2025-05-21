import string
import random
import redis

from django.conf import settings


_REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}?db=4'
_R = redis.Redis.from_url(_REDIS_URL)

_CHARS = [i for i in (string.digits + string.ascii_letters)]


def _get_char():
    return random.choice(_CHARS)


def get_code(length=6):
    result, i = '', 0
    while i < length:
        result += _get_char()
        i += 1

    return result