import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .utils import (
    get_code, 
    check_code, 
    reg_send_code, 
    inc_code,
    code_exists,
    create_id,
    send_code,
    code_is_active,
)
from .models import (
    register_user,
    change_user_email, 
    change_user_pass
)


@require_http_methods(['POST'])
def reg_confirmation_code(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username', None)
    email = data.get('email', None)
    if not username or not email:
        return JsonResponse({}, status=400)

    code_exists = get_code(username)
    if code_exists:
        return JsonResponse({}, status=409)

    reg_send_code(username, email)
    return JsonResponse({})


@require_http_methods(['POST'])
def register(request):
    payload = json.loads(request.body.decode('utf-8'))
    data, code_id, code = payload['data'], payload['confirmation'], payload['code']

    if not check_code(code_id, code):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    try:
        register_user(data)
        data, status = {'success': 'User registered successfully'}, 201
    except IntegrityError:
        data, status = {'error': 'Already exists'}, 409
    except Exception:
        data, status = {'error': True}, 400
    return JsonResponse(data, status=status)


@require_http_methods(['GET'])
def reg_check_email(request):
    email = request.GET.get('e', None)
    if not email:
        return JsonResponse({}, status=400)

    exists = True
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        exists = False
    return JsonResponse({'exists': exists})


@require_http_methods(['GET'])
def reg_check_username(request):
    username = request.GET.get('e', None)
    if not username:
        return JsonResponse({}, status=400)

    exists = True
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        exists = False
    return JsonResponse({'exists': exists})


@require_http_methods(['POST'])
def get_confirmation_code(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email', None)
    if not email:
        return JsonResponse({}, status=400)

    code_id = create_id()
    send_code(code_id, email)
    return JsonResponse({'id': code_id})


@require_http_methods(['POST'])
def change_email(request):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)

    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email', None)
    code_id = data.get('confirmation', None)
    code = data.get('code', None)
    if not email or not code_id or not code:
        return JsonResponse({}, status=400)

    if not check_code(code_id, code):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    change_user_email(request.user, data)
    return JsonResponse({})


@require_http_methods(['POST'])
def change_pass(request):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)

    data = json.loads(request.body.decode('utf-8'))
    password = data.get('password', None)
    code_id = data.get('confirmation', None)
    code = data.get('code', None)
    if not password or not code_id or not code:
        return JsonResponse({}, status=400)

    if not check_code(code_id, code):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    change_user_pass(request.user, data)
    return JsonResponse({})