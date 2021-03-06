import requests
from urllib import parse
from .settings import *
from collections import namedtuple
from .cache import cache
import logging


def getSession():
    session = requests.Session()
    session.auth = (username, password)
    return session


@cache('Financials')
def get_financials(identifier, sequence, type, statement):
    url = parse.urljoin(intrinio_host, intrinio_financials_endpoint)
    session = getSession()
    params = {'identifier': identifier, 'sequence': sequence, 'type': type,
                                        'statement': statement}
    response = session.get(url, params=params)
    logging.info('Request: %s, params: %s ,status: %d' % (url, params, response.status_code))
    result = dict()
    if response.status_code == 200:
        result['type'] = type
        result['statement'] = statement
        result['sequence'] = sequence
        result['identifier'] = identifier
        obj = response.json()['data']
        data = dict()
        if obj:
            for tag_value_dict in obj:
                data[tag_value_dict['tag']] = tag_value_dict['value']
        result['data'] = data
    else:
        logging.error(response.text)
        raise IOError('external call error with status code: %d, msg: %s' % (response.status_code, response.text))
    return result


@cache('Fundamentals')
def get_fundamentals(identifier, sequence, type, statement):
    url = parse.urljoin(intrinio_host, intrinio_fundamentals_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'sequence': sequence, 'type': type,
                                        'statement': statement})
    logging.info('Request: %s, status: %d' % (url, response.status_code))
    result = dict()
    if response.status_code == 200:
        result['type'] = type
        result['statement'] = statement
        result['sequence'] = sequence
        result['identifier'] = identifier
        result['data'] = response.json()['data']
    else:
        logging.error(response.text)
        raise IOError('external call error with status code: %d, msg: %s' % (response.status_code, response.text))
    return result


@cache('Datapoints')
def get_datapoint(identifier, item):
    url = parse.urljoin(intrinio_host, intrinio_datapoint_endpoint)
    session = getSession()
    response = session.get(url, params={'identifier': identifier, 'item': item})
    logging.info('Request: %s, status: %d' % (url, response.status_code))
    result = dict()
    if response.status_code == 200:
        obj = response.json()
        result['identifier'] = identifier
        result['item'] = obj['item']
        result['value'] = obj['value']
    else:
        logging.error(response.text)
        raise IOError('external call error with status code: %d, msg: %s' % (response.status_code, response.text))
    return result


@cache('Tags')
def initrinioTags(statement):
    url = parse.urljoin(intrinio_host, intrinio_tags_endpoint)
    session = getSession()
    response = session.get(url, params={'statement': statement})
    logging.info('Request: %s, status: %d' % (url, response.status_code))
    result = dict()
    if response.status_code == 200:
        result['statement'] = statement
        result['data'] = response.json()['data']
    else:
        raise IOError('external call error with status code: %d, msg: %s' % (response.status_code, response.text))
    return result


def intrinioFinancials(identifier, sequence, item, statement, type):
    result = dict()
    if sequence == -1:
        datapoint = get_datapoint(identifier, item)
        if datapoint and datapoint['value']:
            result['identifier'] = identifier
            result['item'] = item
            result['value'] = datapoint['value']
            result['sequence'] = sequence
            result['statement'] = None
            result['type'] = None
            result['fiscal_year'] = None
            result['start_date'] = None
            result['end_date'] = None
            result['fiscal_period'] = None
            result['filing_date'] = None
        return result

    financials = get_financials(identifier, sequence, type, statement)
    fundamentals = get_fundamentals(identifier, sequence, type, statement)

    if fundamentals and financials and financials['data'] and item in financials['data']:
        result['type'] = type
        result['sequence'] = sequence
        result['statement'] = statement
        result['identifier'] = identifier
        result['item'] = item
        result['value'] = financials['data'][item]
        result['fiscal_year'] = fundamentals['data']['fiscal_year']
        result['start_date'] = fundamentals['data']['start_date']
        result['end_date'] = fundamentals['data']['end_date']
        result['fiscal_period'] = fundamentals['data']['fiscal_period']
        result['filing_date'] = fundamentals['data']['filing_date']

    return result
