import ipaddress


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