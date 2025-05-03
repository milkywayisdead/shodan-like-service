import pymongo
import re

from django.conf import settings

from .utils import (
    get_range, 
    ip_to_int, 
    net_extend_params,
    port_extend_params,
    extend_generic
)
from . import query
from .logger import QLogger
from core.utils.search_keys import REGEX_SEARCH


qlogger = QLogger()


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
        
    hosts_list = _collection.find(params).skip((page - 1)*page_length).limit(page_length).to_list()
    qlogger.add(key, 'hosts', params, _collection.find(params).skip((page - 1)*page_length).limit(page_length))
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
    qlogger.add(key, 'hosts_total', params, collection=_collection, meth='count_documents')
    return _collection.count_documents(params)


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
    qlogger.add(key, 'tops', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


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
    qlogger.add(key, 'ports', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


def net_hosts_total(net_str, extra_type=None, extra_query=None):
    """
    Подсчёт хостов для net.
    """
    params = query.get_range_filter('address', net_str)
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    else:
        params['total_ports'] = {'$ne': []}
    qlogger.add('net', 'hosts_total', params, collection=_collection, meth='count_documents')
    return _collection.count_documents(params)


def net_ports(net_str, extra_type=None, extra_query=None):
    """
    Подсчёт портов для net.
    """
    params = query.get_ports_filter(
        query.get_range_filter('address', net_str)
    )
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    qlogger.add('net', 'ports', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


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
    qlogger.add('net', 'tops', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


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

    hosts_list = _collection.find(
        params
        ).skip((page - 1)*page_length).limit(page_length).to_list()
    qlogger.add('net', 'hosts', params, _collection.find(
        params
        ).skip((page - 1)*page_length).limit(page_length))
    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts(port_str, *args, extra_type=None, extra_query=None, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для port.
    """
    if page < 1:
        page = 1

    params = {_TOTAL_PORTS: {'$elemMatch': {'port': port_str}}}
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)

    hosts_list = _collection.find(
        params
    ).skip((page - 1)*page_length).limit(page_length).to_list()

    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts_total(port_str, extra_type=None, extra_query=None):
    """
    Подсчёт хостов для port.
    """
    params = {_TOTAL_PORTS: {'$elemMatch': {'port': port_str}}}
    if extra_type and extra_query:
        params = net_extend_params(params, extra_type, extra_query)
    return _collection.count_documents(params)


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
    qlogger.add('port', 'tops', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


def loc_hosts(loc_str, *args, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для loc.
    """
    params = query.get_loc_filter(loc_str)
    hosts_list = _collection.find(params).skip((page - 1)*page_length).limit(page_length).to_list()
    for host in hosts_list:
        del host['_id']
    qlogger.add('loc', 'hosts', params, _collection.find(params).skip((page - 1)*page_length).limit(page_length))
    return hosts_list


def loc_hosts_total(loc_str):
    """
    Подсчёт хостов для loc.
    """
    params = query.get_loc_filter(loc_str)
    qlogger.add('loc', 'hosts_total', params, collection=_collection, meth='count_documents')
    return _collection.count_documents(params)


def loc_ports_total(loc_str):
    """
    Подсчёт портов для loc.
    """
    params = query.get_ports_filter(query.get_loc_filter(loc_str))
    qlogger.add('loc', 'ports_total', params)
    return _collection.aggregate(params).to_list()


def loc_tops(loc_str, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для port.
    """
    params = query.get_tops_filter(
        query.get_loc_filter(loc_str),
        limit
    )
    qlogger.add('loc', 'tops', params, collection=_collection, meth='aggregate')
    return _collection.aggregate(params).to_list()


def get_details(t, q, facet):
    details = []
    if t != 'domain':
        details = _collection.aggregate(
            query.get_facet_details_filter(t, q, facet)
        ).to_list()
    return details