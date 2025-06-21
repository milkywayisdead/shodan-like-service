from django.urls import path
from django.urls import path
from . import views


urlpatterns = [
    path('api/get_content', views.get_content, name='get_content'),
]