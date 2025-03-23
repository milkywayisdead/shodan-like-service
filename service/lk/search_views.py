from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

from .mocks import HOSTS
from .db import db


def check_auth(view, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 401}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


class GenericSearchView(View):
    search_type = ''

    def get(self, request, *args, **kwargs):
        term = request.GET['search']
        _ = self.search_type
        resp = {
            'hosts': db.generic_hosts(_, term),
            'hosts_total': db.generic_hosts_total(_, term),
            'ports': db.generic_ports(_, term),
            'tops': db.generic_tops(_, term),
        }
        return JsonResponse(resp)


class GenericSearchWithAuth(GenericSearchView):
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GenericPageView(View):
    search_type = ''

    def get(self, request, *args, **kwargs):
        term = request.GET['search']
        _ = self.search_type
        page = int(request.GET.get('page', 1))
        hosts = db.generic_hosts(_, term, page=page)
        return JsonResponse({'hosts': hosts})


class ASNSearch(GenericSearchView):
    search_type = 'ASN'


class ASNPage(GenericPageView):
    search_type = 'ASN'


class AppSearch(GenericSearchWithAuth):
    search_type = 'total_ports.application'


class AppPage(GenericPageView):
    search_type = 'total_ports.application'


class ComponentSearch(GenericSearchWithAuth):
    search_type = 'total_ports.component'


class ComponentPage(GenericPageView):
    search_type = 'total_ports.component'


class LocSearch(GenericSearchWithAuth):
    search_type = 'Location'


class LocPage(GenericPageView):
    search_type = 'Location'


class OrgSearch(GenericSearchWithAuth):
    search_type = 'Organization'


class OrgPage(GenericPageView):
    search_type = 'Organization'


def hosts(request):
    ip = request.GET['search']
    res = db.hosts(ip)
    return JsonResponse(res)


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


@check_auth
def app(request):
    application = request.GET['search']
    _ = 'total_ports.application'
    resp = {
        'hosts': db.generic_hosts(_, application),
        'hosts_total': db.generic_hosts_total(_, application),
        'ports': db.generic_ports(_, application),
        'tops': db.generic_tops(_, application),
    }
    return JsonResponse(resp)


@check_auth
def component(request):
    component = request.GET['search']
    _ = 'total_ports.component'
    resp = {
        'hosts': db.generic_hosts(_, component),
        'hosts_total': db.generic_hosts_total(_, component),
        'ports': db.generic_ports(_, component),
        'tops': db.generic_tops(_, component),
    }
    return JsonResponse(resp)


@check_auth
def loc(request):
    loc = request.GET['search']
    _ = 'Location'
    resp = {
        'hosts': db.generic_hosts(_, loc),
        'hosts_total': db.generic_hosts_total(_, loc),
        'ports': db.generic_ports(_, loc),
        'tops': db.generic_tops(_, loc),
    }
    return JsonResponse(resp)


@check_auth
def org(request):
    org = request.GET['search']
    _ = 'Organization'
    resp = {
        'hosts': db.generic_hosts(_, org),
        'hosts_total': db.generic_hosts_total(_, org),
        'ports': db.generic_ports(_, org),
        'tops': db.generic_tops(_, org),
    }
    return JsonResponse(resp)


@check_auth
def domain(request):
    domain = request.GET['search']
    _ = 'domain'
    resp = {
        'hosts': db.generic_hosts(_, domain),
        'hosts_total': db.generic_hosts_total(_, domain),
        'ports': db.generic_ports(_, domain),
        'tops': db.generic_tops(_, domain),
    }
    return JsonResponse(resp)


@check_auth
def os(request):
    osys = request.GET['search']
    _ = 'OS'
    resp = {
        'hosts': db.generic_hosts(_, osys),
        'hosts_total': db.generic_hosts_total(_, osys),
        'ports': db.generic_ports(_, osys),
        'tops': db.generic_tops(_, osys),
    }
    return JsonResponse(resp)


@check_auth
def soft(request):
    soft = request.GET['search']
    _ = 'total_ports.software'
    resp = {
        'hosts': db.generic_hosts(_, soft),
        'hosts_total': db.generic_hosts_total(_, soft),
        'ports': db.generic_ports(_, soft),
        'tops': db.generic_tops(_, soft),
    }
    return JsonResponse(resp)


@check_auth
def service(request):
    service = request.GET['search']
    _ = 'total_ports.service'
    resp = {
        'hosts': db.generic_hosts(_, service),
        'hosts_total': db.generic_hosts_total(_, service),
        'ports': db.generic_ports(_, service),
        'tops': db.generic_tops(_, service),
    }
    return JsonResponse(resp)