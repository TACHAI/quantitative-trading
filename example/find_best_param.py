# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-04-24 20:15
# @File     : find_best_param.py
# @Project  : DeltaTrader
import mystrategy.ma_strategy as ma
import data.stock as st
import pandas as pd

# 参数1: 股票池
data = st.get_csv_price('000001.XSHE', '2016-01-01', '2021-01-01')
# data = st.get_single_stock_price('000001.XSHE', 'daily', '2016-01-01', '2021-01-01')
# 参数2：周期参数
params = [5, 10, 20, 60, 120, 250]
# 存放参数与收益
res = []
# 匹配并计算不同的周期参数对：5-10，5-20 …… 120-250
for short in params:
    for long in params:
        if long > short:
            data_res = ma.ma_strategy(data=data, short_window=short,
                                      long_window=long)
            # 获取周期参数，及其对应累计收益率
            cum_profit = data_res['cum_profit'].iloc[-1]  # 获取累计收益率最终数据
            res.append([short, long, cum_profit])  # 将参数放入结果列表

# 将结果列表转换为df，并找到最优参数
res = pd.DataFrame(res, columns=['short_win', 'long_win', 'cum_profit'])
# 排序
res = res.sort_values(by='cum_profit', ascending=False)  # 按收益倒序排列
print(res)