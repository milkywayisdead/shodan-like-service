from django.urls import path
from django.urls import path
from . import views


urlpatterns = [
    path('api/register', views.register, name='register'),
    path('api/reg-check-username', views.reg_check_username, name='reg_check_username'),
    path('api/reg-check-email', views.reg_check_email, name='reg_check_email'),
    path('api/reg-confirmation-code', views.reg_confirmation_code, name='reg_confirmation_code'),
    path('api/get-confirmation-code', views.get_confirmation_code, name='get_confirmation_code'),
    path('api/change-email', views.change_email, name='change_email'),
    path('api/change-pass', views.change_pass, name='change_pass'),
    path('api/check-username-email', views.check_username_and_email, name='check_username_and_email'),    
    path('api/check-code', views.code_check, name='check_code'),
    path('api/restore-pass', views.restore_pass, name='restore_pass'),
]