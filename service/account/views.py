import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .forms import CreateUserForm


@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        try:
            form.save()
            data, status = {'success': 'User registered successfully'}, 201
        except IntegrityError:
            data, status = {'error': 'Already exists'}, 409
        return JsonResponse(data, status=status)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)


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