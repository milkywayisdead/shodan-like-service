import pymongo

from django.conf import settings

from .utils import get_range, ip_to_int
from . import query

_client = pymongo.MongoClient(settings.MONGODB_URL)
_db = _client[settings.MONGODB_DB_NAME]
_collection = _db[settings.MONGODB_COLLECTION_NAME]


def mock_db():
    from .mocks import HOSTS
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
    

def hosts(address):
    """
    Для страницы 'Hosts'
    """
    address = ip_to_int(address)
    res = _collection.find_one({'address': address})
    del res['_id']
    return res


def generic_hosts(key, value, limit=10):
    params = {key: value}
    hosts_list = _collection.find(params).limit(limit).to_list()
    for host in hosts_list:
        del host['_id']
    return hosts_list


def generic_hosts_total(key, value):
    params = {key: value}
    return _collection.count_documents(params)


def generic_tops(key, value, limit=5):
    params = query.get_tops_filter(
        {key: value},
        limit
    )
    return _collection.aggregate(params).to_list()


def net_hosts_total(net_str):
    """
    Для страницы 'Net'
    """
    params = query.get_range_filter('address', net_str)
    return _collection.count_documents(params)


def net_ports(net_str):
    """
    Сумма портов по сети
    """
    params = query.get_ports_filter(
        query.get_range_filter('address', net_str)
    )
    return _collection.aggregate(params).to_list()


def net_tops(net_str, limit=5):
    """
    Топ 5 портов, сервисов, софта, приложений и компонентов
    """
    params = query.get_tops_filter(
        query.get_range_filter('address', net_str),
        limit
    )
    return _collection.aggregate(params).to_list()


def net_hosts(net_str, limit=10):
    params = query.get_range_filter('address', net_str)
    hosts_list = _collection.find(params).limit(limit).to_list()
    for host in hosts_list:
        del host['_id']
    return hosts_list