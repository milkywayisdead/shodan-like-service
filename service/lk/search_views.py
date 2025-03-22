from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .mocks import HOSTS
from .db import db


def check_auth(view, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 401}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


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


def asn(request):
    asn = request.GET['search']
    _ = 'ASN'
    resp = {
        'hosts': db.generic_hosts(_, asn),
        'hosts_total': db.generic_hosts_total(_, asn),
        'ports': db.generic_ports(_, asn),
        'tops': db.generic_tops(_, asn),
    }
    return JsonResponse(resp)


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
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def org(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


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
    return JsonResponse({'data': {'q': request.GET['search']}})


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