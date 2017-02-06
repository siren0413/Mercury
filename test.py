import mercury
import pandas as pd
import json
import numpy as np

if __name__ == '__main__':
    # r = mercury.get_financials('AAPL')
    # r = mercury.get_datapoint('AAPL','totalrevenue')
    # r = mercury.intrinioFinancials('T', sequence=-1, item='totalrevenue')
    # r = mercury.initrinioTags('T','income_statement')
    # r = mercury.intrinioFinancials('T', sequence=1, item='totalrevenue', statement='income_statement',type='FY')
    # items = ['marketcap']
    #
    # for item in items:
    #     r = mercury.financials_by_item(['AAPL', 'T', 'INTC', 'EA', 'ATVI', 'NVDA', 'GOOG', 'TWTR'], sequence=0, item=item)
    #     print(r)
    #
    # r = mercury.translate_and_rounding(['marketcap', 'pricetoearnings'],{'ATVI': [30247560000.0, 36.8423], 'EA': [24465280000.0, 19.4787]})
    # print(r)


    symbols = ['EA', 'ATVI']
    items = ['marketcap', 'pricetoearnings']
    result = mercury.get_financials(symbols, items, sequence=4, type='FY')
    tags, datas = mercury.translate_and_rounding(items, result)