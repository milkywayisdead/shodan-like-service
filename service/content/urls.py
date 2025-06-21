from django.urls import path
from django.urls import path
from . import views


urlpatterns = [
    path('api/get_content', views.get_content, name='get_content'),
    path('api/get_content_item', views.get_content_item, name='get_content_item'),
]