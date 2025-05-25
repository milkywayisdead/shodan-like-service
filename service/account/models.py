from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .forms import UpdateEmailForm


def check_email(email):
    exists = True
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        exists = False
    return exists


def change_user_email(user, data):
    email = data['email']
    exists = check_email(email)
    if exists:
        raise IntegrityError('Email exists')

    form = UpdateEmailForm(data, instance=user)
    if not form.is_valid():
        raise Exception('Form not valid')
    form.save()
    return 'ok'


def change_user_pass(username):
    pass