import requests
from urllib import parse
from .settings import *
from collections import namedtuple


def getSession():
    session = requests.Session()
    session.auth = (username, password)
    return session


def get_financials(identifier, sequence=0, type='FY', statement='calculations'):
    url = parse.urljoin(intrinio_host, intrinio_financials_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'sequence': sequence, 'type': type,
                                        'statement': statement})
    result = namedtuple('Fin', ['type', 'statement', 'sequence', 'identifier', 'data'])
    result.type = type
    result.statement = statement
    result.sequence = sequence
    result.identifier = identifier
    if response.status_code == 200:
        obj = response.json()['data']
        data = dict()
        for tag_value_dict in obj:
            data[tag_value_dict['tag']] = tag_value_dict['value']
        result.data = data
    else:
        result.data = response.text
    return result


def get_fundamentals(identifier, sequence=0, type='FY', statement='calculations'):
    url = parse.urljoin(intrinio_host, intrinio_fundamentals_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'sequence': sequence, 'type': type,
                                        'statement': statement})
    result = namedtuple('Fun', ['type', 'statement', 'sequence', 'identifier', 'data'])
    result.type = type
    result.statement = statement
    result.sequence = sequence
    result.identifier = identifier
    if response.status_code == 200:
        result.data = response.json()['data']
    else:
        result.data = response.text
    return result


def get_datapoint(identifier, item):
    url = parse.urljoin(intrinio_host, intrinio_datapoint_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'item': item})
    result = namedtuple('DP', ['identifier', 'item', 'value'])
    result.identifier = identifier
    if response.status_code == 200:
        obj = response.json()
        result.item = obj['item']
        result.value = obj['value']
    else:
        result.data = response.text
    return result


def intrinioFinancials(identifier, sequence, item, statement='', type=''):
    result = namedtuple('IntrinioFinancials',
                        ['type', 'statement', 'sequence', 'identifier', 'item', 'value', 'fiscal_year', 'end_date',
                         'start_date', 'fiscal_period', 'filing_date'])
    if sequence == -1:
        datapoint = get_datapoint(identifier, item)
        result.identifier = identifier
        result.item = item
        result.value = datapoint.value
        result.sequence = sequence
        result.statement = None
        result.type = None
        result.fiscal_year = None
        result.start_date = None
        result.end_date = None
        result.fiscal_period = None
        result.filing_date = None
        return result

    financials = get_financials(identifier, sequence, type, statement)
    fundamentals = get_fundamentals(identifier, sequence, type, statement)

    result.type = type
    result.sequence = sequence
    result.statement = statement
    result.identifier = identifier
    result.item = item
    result.value = financials.data[item]
    result.fiscal_year = fundamentals.data['fiscal_year']
    result.start_date = fundamentals.data['start_date']
    result.end_date = fundamentals.data['end_date']
    result.fiscal_period = fundamentals.data['fiscal_period']
    result.filing_date = fundamentals.data['filing_date']

    return result


def initrinioTags(identifier, statement):
    url = parse.urljoin(intrinio_host, intrinio_tags_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'statement': statement})
    result = namedtuple('DP', ['identifier', 'statement', 'data'])
    result.identifier = identifier
    result.statement = statement
    if response.status_code == 200:
        result.data = response.json()['data']
    else:
        result.data = response.text
    return result

