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
    items = ['marketcap']

    for item in items:
        r = mercury.financials_by_item(['AAPL', 'T', 'INTC', 'EA', 'ATVI', 'NVDA', 'GOOG', 'TWTR'], sequence=0, item=item)
        # r = mercury.financials_by_identifier('AAPL',['pricetoearnings','marketcap'], sequence=-1,type='FY')
        print(r)

    print('done')

    # json_data = mercury.financials(['AAPL', 'T', 'INTC', 'EA', 'ATVI', 'NVDA', 'GOOG'], sequence=-1,
    #                                item='dividend')
    # index = json_data[0]['tag']['name']
    # # json_data = {'AAPL':1.2,'T':1.3,'INTC':'1.4', 'EA':1.5, 'ATVI':1.6, 'NVDA':1.7, 'GOOG':1.8}
    # json_data = np.array([data['data']['value'] for data in json_data])
    # json_data = json_data.reshape(1, json_data.shape[0])
    # df = pd.DataFrame(json_data, index=[index, ], columns=['AAPL', 'T', 'INTC', 'EA', 'ATVI', 'NVDA', 'GOOG'])
    # print(df)
