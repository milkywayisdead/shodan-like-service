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
    delete_code,
)
from .models import (
    User,
    register_user,
    change_user_email, 
    change_user_pass,
)
from .forms import UpdatePassForm


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
    email = data['email']

    if not check_code(code_id, code, reason=f'register_{email}'):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    try:
        register_user(data)
        data, status = {'success': 'User registered successfully'}, 201
        delete_code(code_id)
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
    reason = f'{data["type"]}_{email}'
    if not email:
        return JsonResponse({}, status=400)

    code_id = create_id()
    send_code(code_id, email, reason=reason)
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

    if not check_code(code_id, code, reason=f'change_email_{email}'):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    change_user_email(request.user, data)
    delete_code(code_id)
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

    user = request.user
    if not check_code(code_id, code, reason=f'change_pass_{user.email}'):
        inc_code(code_id)
        return JsonResponse({'active': code_is_active(code_id)}, status=422)

    change_user_pass(user, data)
    delete_code(code_id)
    return JsonResponse({})


@require_http_methods(['POST'])
def check_username_and_email(request):
    data = json.loads(request.body.decode('utf-8'))
    username, email = data['username'], data['email']
    if not username or not email:
        return JsonResponse({}, status=400)

    valid = False
    try:
        User.objects.get(username=username, email=email)
        valid = True
    except User.DoesNotExist:
        pass
    return JsonResponse({'valid': valid})


@require_http_methods(['POST'])
def code_check(request):
    data = json.loads(request.body.decode('utf-8'))
    code_id, code_to_check = data['confirmation'], data['code']
    code = get_code(code_id)
    if get_code and code['code'] == code_to_check:
        return JsonResponse({'valid': True})
    return JsonResponse({'valid': False}, status=422)


@require_http_methods(['POST'])
def restore_pass(request):
    data = json.loads(request.body.decode('utf-8'))
    username, email = data['username'], data['email']
    password, code_id, code = data['password'], data['confirmation'], data['code']
    if not check_code(code_id, code, reason=f'restore_pass_{email}'):
        inc_code(code_id)
        return JsonResponse({}, status=400)

    user = User.objects.get(username=username, email=email)
    form = UpdatePassForm(data, instance=user)
    if form.is_valid():
        form.save()
        delete_code(code_id)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
