from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .db import db
from .utils.generic_views import (
    GenericSearchView,
    GenericSearchWithAuth,
    GenericPageView,
    GenericPageWithAuth
)
from .utils import search_keys as sk


def hosts(request):
    ip = request.GET['search']
    res = db.hosts(ip)
    return JsonResponse({'host': res})


def port(request):
    port_str = request.GET['search']
    resp = {
        'hosts': db.port_hosts(port_str),
        'hosts_total': db.port_hosts_total(port_str), 
        'ports': [],
        'tops': db.port_tops(port_str),
    }
    return JsonResponse(resp)


def net(request):
    net_str = request.GET['search']
    resp = {
        'hosts': db.net_hosts(net_str),
        'hosts_total': db.net_hosts_total(net_str),
        'ports': db.net_ports(net_str),
        'tops': db.net_tops(net_str),
    }
    return JsonResponse(resp)


def get_net_page(request):
    net_str = request.GET['search']
    page = int(request.GET.get('page', 1))
    resp = db.net_hosts(net_str, page=page)
    return JsonResponse({'hosts': resp})


def get_port_page(request):
    port_str = request.GET['search']
    page = int(request.GET.get('page', 1))
    resp = db.port_hosts(port_str, page=page)
    return JsonResponse({'hosts': resp})


class DomainSearch(GenericSearchWithAuth):
    search_type = sk.DOMAIN


class ASNSearch(GenericSearchView):
    search_type = sk.ASN


class ASNPage(GenericPageView):
    search_type = sk.ASN


class AppSearch(GenericSearchWithAuth):
    search_type = sk.APP


class AppPage(GenericPageWithAuth):
    search_type = sk.APP


class ComponentSearch(GenericSearchWithAuth):
    search_type = sk.COMPONENT


class ComponentPage(GenericPageWithAuth):
    search_type = sk.COMPONENT


class LocSearch(GenericSearchWithAuth):
    search_type = sk.LOC


class LocPage(GenericPageWithAuth):
    search_type = sk.LOC


class OrgSearch(GenericSearchWithAuth):
    search_type = sk.ORG


class OrgPage(GenericPageWithAuth):
    search_type = sk.ORG


class OsSearch(GenericSearchWithAuth):
    search_type = sk.OS


class OsPage(GenericPageWithAuth):
    search_type = sk.OS


class SoftSearch(GenericSearchWithAuth):
    search_type = sk.SOFT


class SoftPage(GenericPageWithAuth):
    search_type = sk.SOFT


class ServiceSearch(GenericSearchWithAuth):
    search_type = sk.SERVICE


class ServicePage(GenericPageWithAuth):
    search_type = sk.SERVICE