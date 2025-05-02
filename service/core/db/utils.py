import ipaddress
from core.utils.search_keys import SK_TP_DICT, SK_DICT


TOTAL_PORTS_FACETS = [
    'port',
    'component',
    'soft',
    'app',
    'service',
]

HOST_FACETS = [
    'city',
    'country',
    'os',
    'org',
    'asn'
]


def net_extend_params(original_params, extra_type, extra_query):
    print(original_params, extra_type, extra_query)
    if extra_type in TOTAL_PORTS_FACETS:
        try:
            original_params['total_ports'] = {'$elemMatch': {SK_TP_DICT[extra_type]: extra_query}}
        except TypeError:
            #original_params[0]['$match'][f'total_ports'] = {'$elemMatch': {SK_TP_DICT[extra_type]: extra_query}}
            original_params[0]['$match'][f'total_ports.{SK_TP_DICT[extra_type]}'] = extra_query
    elif extra_type in HOST_FACETS:
        key = SK_DICT[extra_type]
        try:
            original_params[key] = extra_query
        except TypeError:
            original_params[0]['$match'][key] = extra_query
    return original_params


def is_ip(ip_str):
    ip_str = str(ip_str)
    try:
        ipaddress.IPv4Address(ip_str)
    except ipaddress.AddressValueError:
        pass
    else:
        return True
    
    try:
        ipaddress.IPv6Address(ip_str)
    except ipaddress.AddressValueError:
        return False
    else:
        return True


def is_net(net_str):
    net_str = str(net_str)
    try:
        ipaddress.IPv4Network(net_str)
    except ipaddress.AddressValueError:
        pass
    else:
        return True
    
    try:
        ipaddress.IPv6Network(net_str)
    except ipaddress.AddressValueError:
        return False
    else:
        return True


def ip_to_int(ip_str):
    return int(ipaddress.IPv4Address(ip_str))


def get_range(net_str):
    nw = ipaddress.IPv4Network(net_str)
    nw = tuple(nw)
    return int(nw[0]), int(nw[-1])


def get_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address