import time
import string
import random
import redis
import json
import uuid

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


def get_code(key):
    r = _R.get(key)
    if not r:
        return r
    return json.loads(r)


def inc_code(key):
    data = get_code(key)
    if data:
        data = json.loads(data)
        data['attempts'] += 1
        _R.set(key, json.dumps(data))


def code_exists(key):
    if get_code(key):
        return True


def check_code(key, code):
    code_to_check = get_code(key)
    if not code_to_check:
        return False
    return code == code_to_check['code']


def reg_send_code(key, email):
    code = set_code(key)
    send_mail(
        'Регистрация на agiss.site',
        code,
        settings.EMAIL_SENDER,
        [email],
        fail_silently=False,
    )


def send_code(key, email):
    code = set_code(key)
    send_mail(
        'Код подтверждения agiss.site',
        code,
        settings.EMAIL_SENDER,
        [email],
        fail_silently=False,
    )


def create_id():
    return str(uuid.uuid4())