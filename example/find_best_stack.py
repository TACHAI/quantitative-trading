# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-06-07 14:42
# @File     : find_best_stack.py
# @Project  : DeltaTrader

# 查询2021 一季度 市值大于130亿 收益率在10%-100% 不是ST的股票


import data.stock as st
from jqdatasdk import finance


# stocks = st.get_stock_list()



df = st.get_fundamentals(st.query(st.indicator,st.valuation).filter(st.valuation.market_cap>130,st.indicator.roe>=10,st.indicator.roe<=100),date=None,statDate='2021q1')
goodStocks = df[['code','roe']]

# goodStocks.sort_values('roe',inplace=True)
goodStocks.insert(1,'name',None)

for index, row in goodStocks.iterrows():
    # print(codeName)
    code = row['code']
    roe = row['roe']
    codeName = st.get_security_info(row['code']).display_name

    goodStocks.loc[index, 'name'] = codeName
    # 排除 ST的股票
    # if "ST" in codeName :
    #     goodStocks.dorp([index])


goodStocks.to_excel("/Users/mac/Desktop/pyCharm/DeltaTrader/goodStocks.xls", sheet_name='Sheet1',
                    na_rep='', float_format=None,
                    columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)

# print(goodStocks)