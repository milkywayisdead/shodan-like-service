import string
import random
import redis
import json

from django.conf import settings
from django.core.mail import send_mail


_REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}?db=4'
_R = redis.Redis.from_url(_REDIS_URL)
_EX = settings.CONFIRMATION_CODE_EXPIRY

_CHARS = [i for i in (string.digits + string.ascii_letters)]


def _get_char():
    return random.choice(_CHARS)


def generate_code(length=6):
    result, i = '', 0
    while i < length:
        result += _get_char()
        i += 1

    return result


def set_code(key, ex=_EX):
    code = generate_code()
    _R.set(key, json.dumps({'code': code, 'attempts': 0}), ex=ex)
    return code


def get_code(username):
    r = _R.get(username)
    if not r:
        return r
    return json.loads(r)


def inc_code(username):
    data = get_code(username)
    if data:
        data = json.loads(data)
        data['attempts'] += 1
        _R.set(username, json.dumps(data))


def check_code(key, code):
    code_to_check = get_code(key)
    if not code_to_check:
        return False
    return code == code_to_check.decode()


def reg_send_code(username, email):
    code = set_code(username)
    send_mail(
        'Регистрация на agiss.site',
        code,
        settings.EMAIL_SENDER,
        [email],
        fail_silently=False,
    )