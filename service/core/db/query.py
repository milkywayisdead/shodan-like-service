import re

from .utils import get_range
from core.utils.search_keys import SK_DICT

from django.conf import settings


IGNORECASE = settings.SEARCH_INGORECASE


def aggregate(collection, params):
    return collection.aggregate(params, maxTimeMS=120*1000).to_list()


def count(collection, params):
    return collection.count_documents(params, maxTimeMS=120*1000)


def find(collection, params, skip=0, limit=10): 
    return collection.find(params, max_time_ms=120*1000).skip(skip).limit(limit).to_list()


def regex(value):
    return {'$regex': f'^{value}'}


def get_country_filter(value):
    return {
        'Location.0.country': value  
    }


def get_city_filter(value):
    return {
        'Location.0.city': value  
    }


def get_range_filter(key, net_str):
    addr1, addr2 = get_range(net_str)
    result = {key: {'$gte': addr1, '$lte': addr2}}
    return result


def get_ports_filter(match):
    return  [
        {'$match': match},
        {
            '$unwind': "$total_ports" 
        },
        {
            '$count': "total_ports_count"
        }
    ]


def get_tops_filter(match, limit=5):
    return [
        {'$match': match},
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


def get_port_tops_filter(port_str, limit=5):
    return [
        {
            '$match': { "total_ports.port": port_str},
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


def get_facet_details_filter(t, q, facet):
    if t == 'port':
        match = {"total_ports.port": regex(q)}
    elif t == 'net':
        match = get_range_filter('address', q)
    elif t == 'loc':
        match = get_loc_filter(q)
    elif t == 'asn':
        match = {'ASN': q, 'total_ports': {'$ne': []}}
    else:
        match = {SK_DICT[t]: regex(q)}

    facet = SK_DICT[facet]

    return [
        {'$match': match},
        { 
            '$unwind': "$total_ports" 
        },
        {
            '$facet': {
                'top_ports': [
                    {
                        '$group': { 
                            '_id': f'${facet}', 
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
                ],
            }
        }
    ]