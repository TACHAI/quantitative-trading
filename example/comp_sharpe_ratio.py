# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-04-10 19:55
# @File     : comp_sharpe_ratio.py
# @Project  : DeltaTrader

import data.stock as st
import mystrategy.base as stb
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 获取3只股票的数据: 比亚迪、宁德时代、隆基

codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']

# 容器：存放夏普
sharpes = []
for code in codes:
    data = st.get_single_stock_price(code, 'daily', '2019-01-01', '2021-01-01')
    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_sharpe(data)
    print(data.head)
    name = st.get_security_info(code,date=None).display_name
    title=name+"("+code+")"
    sharpes.append([title, annual_sharpe])  # 存放[[c1, s1],[c2, s2]..]



# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['title', 'sharpe']).set_index('title')


print(sharpes)



# 可视化3只股票做比较

sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()
