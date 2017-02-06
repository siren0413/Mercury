import mercury
import pandas as pd
import numpy as np



def getsum(col):
    print(col)

symbols = ['INTC', 'QCOM','TXN','MU','NVDA']
items = ['marketcap', 'pricetoearnings','pricetobook','pricetorevenue','investedcapitalturnover']
result = mercury.get_financials(symbols, items, sequence=-1, type='FY')
tags, datas = mercury.translate_and_rounding(items, result)
df = pd.DataFrame(datas, index=tags, columns=symbols)
df.replace('nm',np.nan, inplace=True)
mk = df.loc['Market Capitalization'].values
pe = df.loc['Price to Earnings (P/E)'].values

n = np.reshape(mk/pe,(-1,len(symbols)))

df2 = pd.DataFrame(n, columns=symbols, index=['div'])
df = df.append(df2)
df = df.round(2)
df.loc['Market Capitalization'] = df.loc['Market Capitalization'].map('{:,.0f}'.format)
a = df.apply(getsum, axis=0)
df = df.fillna('-')

