import pymongo
import ipaddress

from django.conf import settings


_client = pymongo.MongoClient(settings.MONGODB_URL)
_db = _client[settings.MONGODB_DB_NAME]
_collection = _db[settings.MONGODB_COLLECTION_NAME]


def ip_to_int(ip_str):
    return int(ipaddress.IPv4Address(ip_str))


def get_range(net_str):
    nw = ipaddress.IPv4Network(net_str)
    nw = tuple(nw)
    return int(nw[0]), int(nw[-1])


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


def net_hosts_total(net_str):
    """
    Для страницы 'Net'
    """
    addr1, addr2 = get_range(net_str)
    params = {'address': { '$gte': addr1, '$lte': addr2}}
    return _collection.count_documents(params)


def net_ports(net_str):
    """
    Сумма портов по сети
    """
    addr1, addr2 = get_range(net_str)
    params = [
        {
            '$match': {
                'address': {
                    '$gte': addr1, 
                    '$lte': addr2
                }
            }
        },
        {
            '$unwind': "$total_ports" 
        },
        {
            '$count': "total_ports_count"
        }
    ]
    return _collection.aggregate(params).to_list()


def net_tops(net_str, limit=5):
    """
    Топ 5 портов, сервисов, софта, приложений и компонентов
    """
    addr1, addr2 = addr1, addr2 = get_range(net_str)
    params = [
        {
            '$match': {
                'address': {
                    '$gte': addr1, 
                    '$lte': addr2
                }
            }
        },
        { 
            '$unwind': "$total_ports" 
        },
        {
            '$facet': {
                'top_ports': [
                    {
                        '$group': { 
                            '_id': "$total_ports.port", 
                            'count': {
                                '$sum': 1
                            }
                        }
                    },
                    {
                        '$sort': {
                            'count': -1
                        }
                    },
                    {
                        '$limit': limit 
                    }
                ],
                'top_services': [
                    {
                        '$group': {
                            '_id': "$total_ports.service", 
                            'count': {
                                '$sum': 1
                            }
                        }
                    },
                    {
                        '$sort': {
                            'count': -1
                        }
                    },
                    {
                        '$limit': limit 
                    }
                ],
                'top_software': [
                    {
                        '$group': {
                            '_id': "$total_ports.software", 
                            'count': {
                                '$sum': 1
                            }
                        }
                    },
                    {
                        '$sort': {
                            'count': -1
                        }
                    },
                    {
                        '$limit': limit
                    }
                ],
                'top_applications': [
                    {
                        '$group': 
                        {
                            '_id': "$total_ports.application",
                            'count': {
                                '$sum': 1
                            }
                        }
                    },
                    {
                        '$sort': {
                            'count': -1
                        }
                    },
                    {
                        '$limit': limit
                    }
                ],
                'top_components': [
                    {
                        '$group': {
                            '_id': "$total_ports.component",
                            'count': {
                                '$sum': 1
                            }
                        } 
                    },
                    {
                        '$sort': {'count': -1}
                    },
                    {
                        '$limit': limit
                    }
                ]
            }
        }
    ]
    return _collection.aggregate(params).to_list()


def net_hosts(net_str, limit=10):
    addr1, addr2 = get_range(net_str)
    params = {"address": {'$gte': addr1, '$lte': addr2}}
    hosts_list = _collection.find(params).limit(limit).to_list()
    for host in hosts_list:
        del host['_id']
    return hosts_list