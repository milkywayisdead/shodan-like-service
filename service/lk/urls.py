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
    path('search/asn', sv.ASNSearch.as_view(), name='search_asn'),
    path('search/net', sv.net, name='search_net'),
    path('search/loc', sv.LocSearch.as_view(), name='search_loc'),
    path('search/org', sv.OrgSearch.as_view(), name='search_org'),
    path('search/domain', sv.domain, name='search_domain'),
    path('search/os', sv.os, name='os'),
    path('search/service', sv.service, name='search_service'),
    path('search/soft', sv.soft, name='search_soft'),
    path('search/app', sv.AppSearch.as_view(), name='search_app'),
    path('search/component', sv.ComponentSearch.as_view(), name='search_component'),

    path('search/net/page', sv.get_net_page, name='get_net_page'),
    path('search/asn/page', sv.ASNPage.as_view(), name='asn_page'),
    path('search/app/page', sv.AppPage.as_view(), name='app_page'),
    path('search/component/page', sv.ComponentPage.as_view(), name='component_page'),
    path('search/loc/page', sv.LocPage.as_view(), name='loc_page'),
    path('search/org/page', sv.OrgPage.as_view(), name='org_page'),
]