import pymongo
import ipaddress

from django.conf import settings


_client = pymongo.MongoClient(settings.MONGODB_URL)
_db = _client[settings.MONGODB_DB_NAME]
_collection = _db[settings.MONGODB_COLLECTION_NAME]


def ip_to_int(ip_str):
    return str(int(ipaddress.IPv4Address(ip_str)))


def mock_db():
    from .mocks import HOSTS
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
    


def hosts(address):
    """
    Для страницы 'Hosts'
    """
    address = ip_to_int(address)
    res = _collection.find_one({'address': address})
    del res['_id']
    return res


def net(addr1, addr2):
    """
    Для страницы 'Net'
    """
    addr1, addr2 = ip_to_int(addr1), ip_to_int(addr2)
    params = {'address': { '$gte': addr1, '$lte': addr2}}
    return _collection.countDocuments(params)


def ports_sum(addr1, addr2):
    """
    Сумма портов по сети
    """
    addr1, addr2 = ip_to_int(addr1), ip_to_int(addr2)
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
    return _collection.aggregate(params)


def tops(addr1, addr2, limit=5):
    """
    Топ 5 портов, сервисов, софта, приложений и компонентов
    """
    addr1, addr2 = ip_to_int(addr1), ip_to_int(addr2)
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
    return _collection.aggregate(params)


def first_n(addr1, addr2, limit=10):
    addr1, addr2 = ip_to_int(addr1), ip_to_int(addr2)
    params = {"address": {'$gte': addr1, '$lte': addr2}}
    return hosts.find(params).limit(limit).pretty()