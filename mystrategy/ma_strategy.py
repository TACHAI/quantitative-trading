# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-04-11 19:20
# @File     : ma_strategy.py
# @Project  : DeltaTrader
import data.stock as st
import mystrategy.base as strat
import pandas as pd
import numpy as np
import datetime

def ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线，默认
    :param long_window: 长期n日移动平均线
    :return:
    """
    print("=====当前周期参数:",short_window,long_window)

    data = pd.DataFrame(data)
    # 计算技术指标：ma短期、ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # 过滤信号：st.compose_signal
    data = strat.compose_signal(data)
    # 计算单次收益
    data = strat.calculate_prof_pct2(data)
    # print(data.describe())
    # profit_pct
    # 计算累计收益
    data = strat.calculate_cum_prof(data)


    # 删除多余的数据
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    # 数据预览
    print(data[['close', 'short_ma', 'long_ma', 'signal', 'cum_profit']])

    return data


if __name__ == '__main__':
    df = st.get_single_stock_price('000001.XSHE', 'daily', '2020-01-01', '2021-01-01')
    df = ma_strategy(df)

    # 筛选有信号点
    df = df[df['signal'] != 0]

    # 预览数据
    print("开仓次数：", int(len(df) / 2))
    print(df)
