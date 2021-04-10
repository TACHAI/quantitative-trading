# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-04-07 15:12
# @File     : stock.py
# @Project  : DeltaTrader


import data.stock as st

# 获取平安银行的行情数据（日K）
data = st.get_single_stock_price('000001.XSHE', 'daily', '2020-01-01', '2020-02-01')
print(data)




data = st.transfer_price_freq(data,'W')

# 计算涨跌幅，验证准确性
data = st.calculate_change_pct(data)

print(data)