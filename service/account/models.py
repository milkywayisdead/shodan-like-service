from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .forms import CreateUserForm, UpdateEmailForm, UpdatePassForm


def check_email(email):
    exists = True
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        exists = False
    return exists


def check_username(username):
    exists = True
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        exists = False
    return exists


def register_user(data):
    username, email = data['username'], data['email']
    username_exists = check_username(username)
    email_exists = check_email(email)
    if username_exists or email_exists:
        raise IntegrityError('User or email exists')

    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
    else:
        raise Exception('Error when creating user')


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


def change_user_pass(user, data):
    #if not user.check_password(data['current']):
    #    raise Exception('Wrong password')

    form = UpdatePassForm(data, instance=user)
    if not form.is_valid():
        raise Exception('Form not valid')
    form.save()
    return 'ok'