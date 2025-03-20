from django.urls import path
from . import views
from . import search_views as sv


urlpatterns = [
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),

    path('search/hosts', sv.hosts, name='search_hosts'),
    path('search/port', sv.port, name='search_port'),
    path('search/asn', sv.asn, name='search_asn'),
    path('search/net', sv.net, name='search_net'),
    path('search/loc', sv.loc, name='search_loc'),
    path('search/org', sv.org, name='search_org'),
    path('search/domain', sv.domain, name='search_domain'),
    path('search/os', sv.os, name='os'),
    path('search/service', sv.service, name='search_service'),
    path('search/soft', sv.soft, name='search_soft'),
    path('search/app', sv.app, name='search_app'),
    path('search/component', sv.component, name='search_component'),
]