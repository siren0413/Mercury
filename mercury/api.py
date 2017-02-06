from .client import initrinioTags, intrinioFinancials
from .settings import *
import concurrent.futures as cf
import logging


def financials_by_item(identifiers, sequence=-1, type='FY', item='marketcap'):
    statements = [INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW_STATEMENT, CALCULATIONS, CURRENT]
    result = dict()

    def sub_task(identifier):
        for statement in statements:
            try:
                result = intrinioFinancials(identifier, sequence, item, statement, type)
            except IOError as e:
                logging.error('io error. %s' % e)
                return
            if result:
                return result

    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subtask = {executor.submit(sub_task, identifier): identifier for identifier in identifiers}
        for future in cf.as_completed(future_to_subtask):
            name = future_to_subtask[future]
            try:
                data = future.result()
                if data:
                    result[data['identifier']] = data
            except Exception as exc:
                logging.error('Unable to get [%s]: %s' % (name, exc))
    return result


def financials_by_identifier(identifier, items, sequence=-1, type='FY'):
    statements = [INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW_STATEMENT, CALCULATIONS, CURRENT]
    result = dict()

    def sub_task(item):
        for statement in statements:
            try:
                result = intrinioFinancials(identifier, sequence, item, statement, type)
            except IOError as e:
                logging.error('io error. %s' % e)
                return
            if result:
                return result

    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subtask = {executor.submit(sub_task, item): item for item in items}
        for future in cf.as_completed(future_to_subtask):
            name = future_to_subtask[future]
            try:
                data = future.result()
                if data:
                    result[data['item']] = data
            except Exception as exc:
                logging.error('Unable to get [%s]: %s' % (name, exc))
    return result


def tag_lookup(identifier, tag):
    statements = [INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW_STATEMENT, CALCULATIONS, CURRENT]
    for statement in statements:
        try:
            tags = initrinioTags(identifier, statement)
        except IOError as e:
            logging.error('io error. %s' % e)
            return
        for tag_dict in tags['data']:
            if tag_dict['tag'] == tag:
                return tag_dict


def get_financials(identifiers, items, sequence=-1, type='FY'):
    result = dict()
    for identifier in identifiers:
        fin = financials_by_identifier(identifier, items, sequence, type)
        data_list = list()
        for item in items:
            if item in fin and 'value' in fin[item]:
                data_list.append(fin[item]['value'])
            else:
                data_list.append(None)
        result[identifier] = data_list
    return result
