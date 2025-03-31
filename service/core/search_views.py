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


def details(request):
    get = request.GET.get
    try:
        q = get('q')
        t = get('t')
        facet = get('facet')
    except:
        return JsonResponse({'details': []}, status=400)

    details = db.get_details(t, q, facet)
    return JsonResponse({'details': details})

def hosts(request):
    ip = request.GET['search']
    res = db.hosts(ip)
    return JsonResponse({'host': res})


class PortSearch(GenericSearchView):
    hosts_func = db.port_hosts
    hosts_total_func = db.port_hosts_total
    ports_func = lambda x: []
    tops_func = db.port_tops

    def get_args(self, request):
        return (request.GET['search'],)


class NetSearch(GenericSearchView):
    hosts_func = db.net_hosts
    hosts_total_func = db.net_hosts_total
    ports_func = db.net_ports
    tops_func = db.net_tops

    def get_args(self, request):
        return (request.GET['search'],)


class NetPage(GenericPageView):
    search_func = db.net_hosts

    def get_args(self, request):
        return (request.GET['search'], )


class PortPage(GenericPageView):
    search_func = db.port_hosts

    def get_args(self, request):
        return (request.GET['search'], )


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
    hosts_func = db.loc_hosts
    hosts_total_func = db.loc_hosts_total
    ports_func = db.loc_ports_total
    tops_func = db.loc_tops

    def get_args(self, request):
        return (request.GET['search'], )


class LocPage(GenericPageWithAuth):
    search_type = sk.LOC
    search_func = db.loc_hosts

    def get_args(self, request):
        return (request.GET['search'], )


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