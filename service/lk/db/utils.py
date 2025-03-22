import ipaddress

def ip_to_int(ip_str):
    return int(ipaddress.IPv4Address(ip_str))


def get_range(net_str):
    nw = ipaddress.IPv4Network(net_str)
    nw = tuple(nw)
    return int(nw[0]), int(nw[-1])