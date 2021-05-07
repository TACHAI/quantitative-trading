# -*- coding: utf-8 -*-
# @Author   : tachai
# @Time     : 2021-04-07 19:11
# @File     : base.py
# @Project  : DeltaTrader
import data.stock as st
import numpy as np
import datetime
import matplotlib; matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd


def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe, 包含单次收益率数据
    :return results: dict, 评估指标数据
    """
    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    data = calculate_cum_prof(data)

    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]
    # 计算年化收益率（每月开仓）
    annual_return = data['profit_pct'].mean() * 12

    # 计算近一年最大回撤
    data = caculate_max_drawdown(data, window=12)
    # print(data)
    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]

    # 计算夏普比率
    sharpe, annual_sharpe = calculate_sharpe(data)

    # 放到dict中
    results = {'总收益率': total_return, '年化收益率': annual_return,
               '最大回撤': max_drawdown, '夏普比率': annual_sharpe}

    # 打印评估指标
    for key, value in results.items():
        print(key, value)

    return data


def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    data['buy_signal'] = np.where((data['buy_signal'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1)
                                   & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    """
    data = data[data['signal'] != 0]  # 筛选
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data['profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]
    return data

def calculate_prof_pct2(data):
    """
    计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    """
    data.loc[data['signal'] != 0,'profit_pct']=data['close'].pct_change()  # 筛选
    data = data[data['signal'] == -1]
    return data


def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data: dataframe
    :return:
    """
    print(data['profit_pct'])
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def caculate_portfolio_return(data, signal, n):
    """
    计算组合收益率
    :param data: dataframe
    :param signal: dataframe
    :param n: int
    :return returns: dataframe
    """
    returns = data.copy()
    # 投组收益率（等权重）= 收益率之和 / 股票个数
    returns['profit_pct'] = (signal * returns.shift(-1)).T.sum() / n
    returns = calculate_cum_prof(returns)
    return returns.shift(1)  # 匹配对应的交易月份


def caculate_max_drawdown(data):
    """
    计算最大回撤比
    :param data:
    :return:
    """
    # 选取时间周期（时间窗口）
    window = 252

    # 模拟持仓金额：投入的总金额 *（1+收益率）
    data['close'] = 10000 * (1 + data['cum_profit'])
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = (谷值 — 峰值)/峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data


def calculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe, stock
    :return: float
    df.mean()等价于df.mean(0)。把轴向数据求平均，得到每列数据的平均值。

    """
    # 公式：sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    daily_return = data['close'].pct_change()
    # daily_return = data['profit_pct']
    avg_return = daily_return.mean()
    sd_reutrn = daily_return.std()
    # 计算夏普：每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_reutrn
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


def week_period_strategy(code, time_freq, start_date, end_date):
    """
    周期选股（周四买，周一卖）
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    """
    data = st.get_single_stock_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    data = compose_signal(data)  # 整合信号
    data = calculate_prof_pct(data)  # 计算收益
    data = calculate_cum_prof(data)  # 计算累计收益率
    # data = caculate_max_drawdown(data)  # 最大回撤
    return data


if __name__ == '__main__':
    df = week_period_strategy('000001.XSHE', 'daily', None, datetime.date.today())
    # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    # print(df.describe())
    print(df['profit_pct'])
    df['profit_pct'].plot()
    plt.show()



    # 查看平安银行最大回撤
    # df = st.get_single_stock_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    # df = caculate_max_drawdown(df)
    # # print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    # 计算夏普比率
    # df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    # sharpe = calculate_sharpe(df)
    # print(sharpe)
