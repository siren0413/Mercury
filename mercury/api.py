from .client import initrinioTags, intrinioFinancials
from .settings import *
import concurrent.futures as cf


def financials(identifiers, sequence=-1, type='FY', item='marketcap'):
    statements = [INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW_STATEMENT, CALCULATIONS, CURRENT]
    result = []

    def sub_task(identifier):
        sub_result = dict()
        for statement in statements:
            current = initrinioTags(identifier, statement)
            if not current:
                break
            for tag_dict in current['data']:
                if tag_dict['tag'] == item:
                    sub_result['tag'] = tag_dict
                    break
            if sub_result:
                data = intrinioFinancials(identifier, sequence, item, statement, type)
                sub_result['data'] = data
                break
        return sub_result

    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subtask = {executor.submit(sub_task,identifier): identifier for identifier in identifiers}
        for future in cf.as_completed(future_to_subtask):
            sub_result = future_to_subtask[future]
            try:
                data = future.result()
                if data:
                    result.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (sub_result, exc))

    print(result)
