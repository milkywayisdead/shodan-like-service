from django.urls import path
from django.urls import path
from . import views


urlpatterns = [
    path('api/register', views.register, name='register'),
    path('api/reg-check-username', views.reg_check_username, name='reg_check_username'),
    path('api/reg-check-email', views.reg_check_email, name='reg_check_email'),
    path('api/request-confirmation-code', views.request_confirmation_code, name='request_confirmation_code'),
]