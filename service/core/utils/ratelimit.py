import time
import redis
import json

from django.conf import settings


_REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
_R = redis.Redis.from_url(_REDIS_URL)
_USERS_HASH = settings.RATELIMIT_USERS_HASH_NAME
_IPS_HASH = settings.RATELIMIT_IPS_HASH_NAME
_USER_LIMIT = settings.RATELIMIT_USER_LIMIT
_IP_LIMIT = settings.RATELIMIT_IP_LIMIT
_USER_INTERVAL = settings.RATELIMIT_USER_INTERVAL
_IP_INTERVAL = settings.RATELIMIT_IP_INTERVAL

_COUNTER_KEY = 'counter'
_INTERVAL_START_KEY = 'interval_start'


def db_request_allowed(state, target='user'):
    interval, limit = _USER_INTERVAL, _USER_LIMIT
    if target != 'user':
        interval, limit = _IP_INTERVAL, _IP_LIMIT

    n, ts = state[_COUNTER_KEY], state[_INTERVAL_START_KEY]
    now = time.time()
    if ts + interval < now:
        return True
    if n < limit:
        return True
    return False


def get_new_state():
    return {_COUNTER_KEY: 0, _INTERVAL_START_KEY: time.time()}


def _create_counter(hash, key):
    state = get_new_state()
    _R.hset(hash, key, json.dumps(state))
    return state


def create_user_counter(key):
    return _create_counter(_USERS_HASH, key)


def create_ip_counter(key):
    return _create_counter(_IPS_HASH, key)


def update_counter(key, target='user'):
    hash, interval, get_state = _USERS_HASH, _USER_INTERVAL, get_user_state
    if target != 'user':
        hash, interval, get_state = _IPS_HASH, _IP_INTERVAL, get_ip_state
    
    now = time.time()
    state = get_state(key)
    # если истек интервал, то сбросить
    if state[_INTERVAL_START_KEY] + interval < now:
        new_state = get_new_state()
    # если нет - увеличить счётчик
    else:
        new_state = state
    new_state[_COUNTER_KEY] += 1
    return _R.hset(hash, key, json.dumps(new_state))


def get_user_state(user_id):
    state = _R.hget(_USERS_HASH, user_id)
    if state:
        return json.loads(state)


def get_ip_state(key):
    state = _R.hget(_IPS_HASH, key)
    if state:
        return json.loads(state)