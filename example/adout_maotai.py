# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-05-03 13:43
# @File     : adout_maotai.py
# @Project  : DeltaTrader

import data.stock as st

# 茅台600519

data = st.get_security_info('600519.XSHG', date=None).display_name

# 茅台最新的收盘价格
price = st.get_single_stock_price('600519.XSHG', 'daily', start_date='2021-04-30', end_date='2021-05-03')['close']
print(price[0])

# A股上市总股本
capitalization = st.get_fundamentals(st.query(st.valuation).filter(st.valuation.code=='600519.XSHG'), date='2021-04-30')[['code','circulating_cap','market_cap']]

# 茅台的市值
market_cap =capitalization['circulating_cap'][0]*price[0]/10000

print(capitalization)
print(market_cap)

# 茅台的市盈率

valuation =st.get_fundamentals(st.query(st.valuation).filter(st.valuation.code=='600519.XSHG'), date='2021-04-30')


basic_eps = st.get_fundamentals(st.query(st.income,statDate='2020').filter(st.valuation.code=='600519.XSHG'))['basic_eps'][0]
print(valuation)


print(basic_eps)
print(price[0]/basic_eps)

