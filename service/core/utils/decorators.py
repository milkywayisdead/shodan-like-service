from django.http import JsonResponse

from . import ratelimit as rl
from core.db.utils import get_ip


_DENIED = JsonResponse({'error': 'denied'}, status=429)


def check_auth(view, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 401}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


def _denied_view(request, *args, **kwargs):
    return _DENIED


def limit_check(view, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        user = request.user
        ok = False

        # проверка лимита запросов для пользователя
        if user.is_authenticated:
            state = rl.get_user_state(user.id)
            if not state:
                state = rl.create_user_counter(user.id)
            ok = rl.db_request_allowed(state, target='user')

        # проверка лимита запросов для ip
        else:
            ip_address = get_ip(request)
            state = rl.get_ip_state(ip_address)
            if not state:
                state = rl.create_ip_counter(ip_address)
            ok = rl.db_request_allowed(state, target='ip')

        if ok:
            return view(request, *args, **kwargs)
        return _denied_view(request, *args, **kwargs)
    
    return wrapper