import re

from .utils import get_range, ip_to_int
from core.utils.search_keys import SK_DICT


def regex(value):
    return re.compile(value, re.IGNORECASE)


def get_match_filter(key, value):
    return {'$match': {key: value}}


def get_elemmatch_filter(key, value):
    return {'$elemMatch': {key: {'$regex': value, '$options': 'i'}}}


def get_loc_filter(value):
    return {
        'Location': {
            '$elemMatch': {
                '$or': [
                    {'city': {'$regex': value, '$options': 'i'}},
                    {'country': {'$regex': value, '$options': 'i'}},
                ]
            }
        }
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
            '$match': { "total_ports.port": {'$regex': port_str, '$options': 'i'}},

            #'$match': {
            #    'total_ports': {'$elemMatch': {'port': {'$regex': port_str, '$options': 'i'}}}
            #},
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
        match = {"total_ports.port": {'$regex': q, '$options': 'i'}}
    elif t == 'net':
        match = get_range_filter('address', q)
    elif t == 'loc':
        match = get_loc_filter(q)
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