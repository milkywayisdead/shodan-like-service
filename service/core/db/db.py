import pymongo

from django.conf import settings

from .utils import (
    get_range, 
    ip_to_int, 
    net_extend_params,
    port_extend_params,
    extend_generic
)
from . import query


_client = pymongo.MongoClient(settings.MONGODB_URL)
_db = _client[settings.MONGODB_DB_NAME]
_collection = _db[settings.MONGODB_COLLECTION_NAME]


_TOTAL_PORTS = 'total_ports'
_PAGE_LENGTH = 10
_TOPS_LIMIT = 6


def mock_db():
    from ..utils.mocks import HOSTS
    import ipaddress
    h = HOSTS[0]
    del h['_id']
    _collection.insert_one(h)

    ip = ip_to_int(h['IP'])
    for i in range(200):
        del h['_id']
        ip += 1
        h['address'] = str(ip)
        h['IP'] = str(ipaddress.IPv4Address(ip))
        _collection.insert_one(h)
    print('OK')


_regex = query.regex


def hosts(address):
    """
    Поиск хоста по адресу.
    """
    address = ip_to_int(address)
    res = _collection.find_one({'address': address, 'total_ports': {'$ne': []}})
    if res:
        del res['_id']
    return res


def generic_hosts(key, value, *args, 
    extra_type=None, extra_query=None, 
    page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для asn, loc, org, app, component, service, soft, os.
    """
    if page < 1:
        page = 1

    if key.lower() == 'asn':
        params = {'ASN': value, 'total_ports': {'$ne': []}}
    else:
        params = {key: _regex(value)}
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    hosts_list = query.find(
        _collection, 
        params, 
        skip=(page - 1)*page_length, 
        limit=page_length
    )

    for host in hosts_list:
        del host['_id']
    return hosts_list


def generic_hosts_total(key, value, extra_type=None, extra_query=None):
    """
    Подсчёт хостов для asn, loc, org, app, component, service, soft, os.
    """
    if key.lower() == 'asn':
        params = {'ASN': value, 'total_ports': {'$ne': []}}
    else:
        params = {key: _regex(value)}
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.count(_collection, params)


def generic_tops(key, value, extra_type=None, extra_query=None, limit=5):
    """
    Получение топ-{limit} для asn, loc, org, app, component, service, soft, os.
    """
    if key.lower() == 'asn':
        match = {'ASN': value}
    else:
        match = {key: _regex(value)}

    params = query.get_tops_filter(match, limit)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def generic_ports(key, value, extra_type=None, extra_query=None):
    """
    Подсчёт портов для asn, loc, org, app, component, service, soft, os.
    """
    if key.lower() == 'asn':
        match = {'ASN': value}
    else:
        match = {key: _regex(value)}
    params = query.get_ports_filter(match)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def net_hosts_total(net_str, extra_type=None, extra_query=None):
    """
    Подсчёт хостов для net.
    """
    params = query.get_range_filter('address', net_str)
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    else:
        params['total_ports'] = {'$ne': []}

    return query.count(_collection, params)


def net_ports(net_str, extra_type=None, extra_query=None):
    """
    Подсчёт портов для net.
    """
    params = query.get_ports_filter(
        query.get_range_filter('address', net_str)
    )
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def net_tops(net_str, extra_type=None, extra_query=None, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для net.
    """
    params = query.get_tops_filter(
        query.get_range_filter('address', net_str),
        limit
    )
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def net_hosts(net_str, *args, extra_type=None, extra_query=None, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для net.
    """
    if page < 1:
        page = 1

    params = query.get_range_filter('address', net_str)
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    else:
        params['total_ports'] = {'$ne': []}

    hosts_list = query.find(
        _collection,
        params,
        skip=(page - 1)*page_length,
        limit=page_length
    )

    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts(port_str, *args, extra_type=None, extra_query=None, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для port.
    """
    if page < 1:
        page = 1

    params = {_TOTAL_PORTS: {'$elemMatch': {'port': query.regex(port_str)}}}
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)

    hosts_list = query.find(
        _collection,
        params,
        skip=(page - 1)*page_length,
        limit=page_length
    )

    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts_total(port_str, extra_type=None, extra_query=None):
    """
    Подсчёт хостов для port.
    """
    params = {_TOTAL_PORTS: {'$elemMatch': {'port': query.regex(port_str)}}}
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    return query.count(_collection, params)


def port_tops(port_str, extra_type=None, extra_query=None, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для port.
    """
    params = query.get_port_tops_filter(
        port_str,
        limit
    )
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    return query.aggregate(_collection, params)


def country_hosts(
    loc_str, *args,
    extra_type=None, extra_query=None,
    page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для country.
    """
    params = query.get_country_filter(loc_str)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    hosts_list = query.find(
        _collection,
        params,
        skip=(page - 1)*page_length,
        limit=page_length
    )
    for host in hosts_list:
        del host['_id']

    return hosts_list


def country_hosts_total(loc_str, extra_type=None, extra_query=None,):
    """
    Подсчёт хостов для country.
    """
    params = query.get_country_filter(loc_str)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.count(_collection, params)


def country_ports_total(loc_str, extra_type=None, extra_query=None,):
    """
    Подсчёт портов для country.
    """
    params = query.get_ports_filter(query.get_country_filter(loc_str))
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def country_tops(loc_str, extra_type=None, extra_query=None, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для country.
    """
    params = query.get_tops_filter(
        query.get_country_filter(loc_str),
        limit
    )
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def city_hosts(
    loc_str, *args, 
    extra_type=None, extra_query=None,
    page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для city.
    """
    params = query.get_city_filter(loc_str)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    hosts_list = query.find(
        _collection,
        params,
        skip=(page - 1)*page_length,
        limit=page_length
    )
    for host in hosts_list:
        del host['_id']

    return hosts_list


def city_hosts_total(loc_str, extra_type=None, extra_query=None,):
    """
    Подсчёт хостов для city.
    """
    params = query.get_city_filter(loc_str)
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.count(_collection, params)


def city_ports_total(loc_str, extra_type=None, extra_query=None,):
    """
    Подсчёт портов для city.
    """
    params = query.get_ports_filter(query.get_city_filter(loc_str))
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def city_tops(loc_str, extra_type=None, extra_query=None, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для city.
    """
    params = query.get_tops_filter(
        query.get_city_filter(loc_str),
        limit
    )
    if extra_type and extra_query:
        params = extend_generic(params, extra_type, extra_query)

    return query.aggregate(_collection, params)


def get_details(t, q, facet, et='', eq=''):
    details = []
    if t != 'domain':
        details = query.aggregate(
            _collection,
            query.get_facet_details_filter(t, q, facet, et=et, eq=eq)
        )
    return details