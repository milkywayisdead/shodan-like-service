import pymongo
import re

from django.conf import settings

from .utils import get_range, ip_to_int
from . import query

_client = pymongo.MongoClient(settings.MONGODB_URL)
_db = _client[settings.MONGODB_DB_NAME]
_collection = _db[settings.MONGODB_COLLECTION_NAME]


_TOTAL_PORTS = 'total_ports'
_PAGE_LENGTH = 10
_TOPS_LIMIT = 5


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
        h['address'] = ip
        h['IP'] = str(ipaddress.IPv4Address(ip))
        _collection.insert_one(h)
    print('OK')


def _regex(value):
    return re.compile(value, re.IGNORECASE)


def hosts(address):
    """
    Поиск хоста по адресу.
    """
    address = ip_to_int(address)
    res = _collection.find_one({'address': address})
    if res:
        del res['_id']
    return res


def generic_hosts(key, value, *args, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для asn, loc, org, app, component, service, soft, os.
    """
    if page < 1:
        page = 1

    params = {key: _regex(value)}
    hosts_list = _collection.find(params).skip((page - 1)*page_length).limit(page_length).to_list()
    for host in hosts_list:
        del host['_id']
    return hosts_list


def generic_hosts_total(key, value):
    """
    Подсчёт хостов для asn, loc, org, app, component, service, soft, os.
    """
    return _collection.count_documents({key: _regex(value)})


def generic_tops(key, value, limit=5):
    """
    Получение топ-{limit} для asn, loc, org, app, component, service, soft, os.
    """
    params = query.get_tops_filter(
        {key: _regex(value)},
        limit
    )
    return _collection.aggregate(params).to_list()


def generic_ports(key, value):
    """
    Подсчёт портов для asn, loc, org, app, component, service, soft, os.
    """
    params = query.get_ports_filter(
        {key: _regex(value)}
    )
    return _collection.aggregate(params).to_list()


def net_hosts_total(net_str):
    """
    Подсчёт хостов для net.
    """
    params = query.get_range_filter('address', net_str)
    return _collection.count_documents(params)


def net_ports(net_str):
    """
    Подсчёт портов для net.
    """
    params = query.get_ports_filter(
        query.get_range_filter('address', net_str)
    )
    return _collection.aggregate(params).to_list()


def net_tops(net_str, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для net.
    """
    params = query.get_tops_filter(
        query.get_range_filter('address', net_str),
        limit
    )
    return _collection.aggregate(params).to_list()


def net_hosts(net_str, *args, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для net.
    """
    if page < 1:
        page = 1

    params = query.get_range_filter('address', net_str)
    hosts_list = _collection.find(
        params
        ).skip((page - 1)*page_length).limit(page_length).to_list()

    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts(port_str, *args, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для port.
    """
    if page < 1:
        page = 1
    params = query.get_elemmatch_filter('port', port_str)
    hosts_list = _collection.find(
        {_TOTAL_PORTS: params}
    ).skip((page - 1)*page_length).limit(page_length).to_list()

    for host in hosts_list:
        del host['_id']
    return hosts_list


def port_hosts_total(port_str):
    """
    Подсчёт хостов для port.
    """
    params = query.get_elemmatch_filter('port', port_str)
    return _collection.count_documents({_TOTAL_PORTS: params})


def port_tops(port_str, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для port.
    """
    params = query.get_port_tops_filter(
        port_str,
        limit
    )
    return _collection.aggregate(params).to_list()


def loc_hosts(loc_str, *args, page=1, page_length=_PAGE_LENGTH):
    """
    Поиск хостов для loc.
    """
    params = query.get_loc_filter(loc_str)
    hosts_list = _collection.find(params).skip((page - 1)*page_length).limit(page_length).to_list()
    for host in hosts_list:
        del host['_id']
    return hosts_list


def loc_hosts_total(loc_str):
    """
    Подсчёт хостов для loc.
    """
    params = query.get_loc_filter(loc_str)
    return _collection.count_documents(params)


def loc_ports_total(loc_str):
    """
    Подсчёт портов для loc.
    """
    params = query.get_ports_filter(query.get_loc_filter(loc_str))
    return _collection.aggregate(params).to_list()


def loc_tops(loc_str, limit=_TOPS_LIMIT):
    """
    Получение топ-{limit} для port.
    """
    params = query.get_tops_filter(
        query.get_loc_filter(loc_str),
        limit
    )
    return _collection.aggregate(params).to_list()