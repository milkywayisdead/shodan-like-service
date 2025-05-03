ASN = 'ASN'
APP = 'total_ports.application'
COMPONENT = 'total_ports.component'
SOFT = 'total_ports.software'
SERVICE = 'total_ports.service'
ORG = 'Organization'
LOC = 'Location'
OS = 'OS'
DOMAIN = 'domain'
PORT = 'total_ports.port'
COUNTRY = 'Location.0.country'
CITY = 'Location.0.city'

SK_DICT = {
    'asn': ASN,
    'app': APP,
    'application': APP,
    'component': COMPONENT,
    'software': SOFT,
    'soft': SOFT,
    'service': SERVICE,
    'org': ORG,
    'loc': LOC,
    'os': OS,
    'port': PORT,
    'country': COUNTRY,
    'city': CITY,
}

SK_TP_DICT = {
    'app': 'application',
    'soft': 'software',
    'service': 'service',
    'port': 'port',
    'component': 'component'
}


REGEX_SEARCH = [
    'Organization',
    'OS',
    'total_ports.service',
    'total_ports.software',
    'total_ports.application',
    'total_ports.component',
]