import mercury

if __name__ == '__main__':
    # r = mercury.get_financials('AAPL')
    # r = mercury.get_datapoint('AAPL','totalrevenue')
    # r = mercury.intrinioFinancials('T', sequence=-1, item='totalrevenue')
    # r = mercury.initrinioTags('T','income_statement')
    # r = mercury.intrinioFinancials('T', sequence=1, item='totalrevenue', statement='income_statement',type='FY')
    items = ['totalrevenue','operatingcostofrevenue','depreciationexpense','investedcapitalincreasedecrease','ebit','netincome','operatingrevenue']

    for item in items:
        r = mercury.financials(['AAPL', 'T', 'INTC', 'EA', 'ATVI', 'NVDA', 'GOOG', 'TWTR'], sequence=0, item=item)
        print(r)

    print('done')
