import time
import redis

from django.core import settings


_REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
_R = redis.Redis(_REDIS_URL)
_USERS_HASH = settings.RATELIMIT_USERS_HASH_NAME
_IPS_HASH = settings.RATELIMIT_IPS_HASH_NAME
_USER_LIMIT = settings.RATELIMIT_USER_LIMIT
_IP_LIMIT = settings.RATELIMIT_IP_LIMIT
_USER_INTERVAL = settings.RATELIMIT_USER_INTERVAL
_IP_INTERVAL = settings.RATELIMIT_IP_INTERVAL

_COUNTER_KEY = 'counter'
_INTERVAL_START_KEY = 'interval_start'

state = {'n': 1, 'ts': time.time()}


def db_request_allowed(state):
    n, ts = state[_COUNTER_KEY], state[_INTERVAL_START_KEY]
    now = time.time()
    ts_ok, n_ok = False, False
    if ts + _USER_INTERVAL < now:
        return True
    if n < _USER_LIMIT:
        return True
    return False


def new_state():
    return {_COUNTER_KEY: 0, _INTERVAL_START_KEY: time.time()}


def _create_counter(hash, key):
    state = new_state()
    _R.hset(hash, key, state)
    return state


def create_user_counter(user_id):
    _create_counter(_USERS_HASH, user_id)
    

def increment_counter(user_id, state):
    state[_COUNTER_KEY] += 1
    return _R.hset(_USERS_HASH, user_id, state)


def get_user_state(user_id):
    return _R.hget(_USERS_HASH, user_id)


def set_user_state(user_id, state):
    return _R.hset(_USERS_HASH, user_id, state)


def get_ip_state(user_id):
    pass


def set_ip_state(user_id):
    pass