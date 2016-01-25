# -*- coding: utf-8 -*-

# 逻辑简述：新三板市场中，由于单个做市商交易量占总交易的权重很大，所以做市商交易本身会很大的影响市场交易均价；
# 所以做市商市场交易带来两方面的影响，一是影响库存股浮盈，二是直接带来交易的损益（买卖价差导致赚钱或者亏损）

# 本页脚本通过模拟不同的交易策略，得到不同买卖价格下，对库存股浮盈和交易损益的影响
# 本页脚本列出的策略generate_simulation_trades和generate_simulation_2是两个交易策略
#   前者假设市场交易价格不变，后者假设市场交易价格均匀变化到给定的价格

# 交易策略的输出即为transactions,格式和函数get_transactions()返回格式相同；
#   返回格式："是否本人交易"（默认为1，表示本人交易），“交易日期”, 交易数量，交易单价

# calculate_profit根据历史交易记录，加上模拟形成的交易记录，计算各项指标并绘图；

from calculate_hist import get_transactions, calculate_cost, plot
from datetime import timedelta
import numpy

FILE_NAME = 'sample_data.xls'


def generate_simulation_trades(file_name, stock_ratio, selling_price_diff, buying_price_diff, days):
    # file_name: 交易数据文件名，stock_ratio: 交易数量占总库存的比例； selling_price_diff: 卖出价格和收盘价之比； buying_price_diff：价差； days: 策略持续时间；
    # 返回 交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、每日收盘价

    # 首先根据历史交易数据，计算各项指标
    hist_tran = get_transactions(file_name)
    hist_value = calculate_cost(hist_tran, value=[])
    # 返回历史数据最后一个交易日的收盘价，交易日期，库存股数量
    closing_price = hist_value[-1][5]
    closing_date = hist_value[-1][0]
    stock_qty = hist_value[-1][1]
    # 卖出价格取前一个交易日的收盘价乘以浮动比例
    selling_price = closing_price * selling_price_diff
    # 买入价格为前一个交易日的收盘价下浮5%；
    buying_price = selling_price * buying_price_diff
    # 交易数量（买入数量和卖出数量）为库存总量的1%；
    trade_qty = stock_qty * stock_ratio
    # 一次交易策略（含一买一卖两次交易）为：
    trades = [(1, closing_date + timedelta(days=1), trade_qty, buying_price),
              (1, closing_date + timedelta(days=1), -trade_qty, selling_price)]
    # 将交易延长到days个交易日
    for day_diff in range(days):
        trades.append((1, closing_date + timedelta(days=day_diff+2), trade_qty, buying_price))
        trades.append((1, closing_date + timedelta(days=day_diff+2), -trade_qty, selling_price))
    return trades


def generate_simulation_2(file_name, target_price, stock_ratio, buying_price_diff, days):
    # 与上一个策略不同，该策略考虑了市场价格在days时间内，从收盘价变动到目标价格target_price的情况；为了简化策略，假设价格变动是均匀的
    # file_name: 交易数据文件名，stock_ratio: 交易数量占总库存的比例； selling_price_diff: 卖出价格和收盘价之比； buying_price_diff：价差； days: 策略持续时间；
    # 返回 交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、每日收盘价

    # 首先根据历史交易数据，计算各项指标
    hist_tran = get_transactions(file_name)
    hist_value = calculate_cost(hist_tran, value=[])
    # 返回历史数据最后一个交易日的收盘价，交易日期，库存股数量
    closing_price = hist_value[-1][5]
    closing_date = hist_value[-1][0]
    stock_qty = hist_value[-1][1]
    # 交易数量（买入数量和卖出数量）为库存总量的1%；
    trade_qty = stock_qty * stock_ratio
    # 默认每日的卖出均价是收盘价，默认价格变动是均匀的
    selling_price_coll = numpy.linspace(closing_price, target_price, days)
    # 买入出价格是卖出价乘以买卖价差比例buying_price_diff
    buying_price_coll = selling_price_coll * buying_price_diff
    trades = []
    # 将交易延长到days个交易日
    for day_diff in range(days):
        trades.append((1, closing_date + timedelta(days=day_diff+2), trade_qty, buying_price_coll[day_diff]))
        trades.append((1, closing_date + timedelta(days=day_diff+2), -trade_qty, selling_price_coll[day_diff]))
    return trades


# 计算模拟前后的总利润差额；
# 输入为历史交易数据，模拟交易数据，库存浮盈/交易损益 的比例； 之所以使用 库存浮盈/交易损益 的比例，
#   是考虑到有些公司考核交易的指标是 库存浮盈+交易损益，而有些仅考核交易损益
def calculate_profit(file_name, simulation_tran, ratio):
    hist_tran = get_transactions(file_name)
    historical_value = calculate_cost(hist_tran, value=[])
    new_tran = hist_tran + simulation_tran
    new_value = calculate_cost(new_tran, value=[])
    plot(new_value)
    simulation_profit = (new_value[-1][3] - historical_value[-1][3]) * ratio + new_value[-1][4] - historical_value[-1][4]
    return simulation_profit


if __name__ == "__main__":
    # a = generate_simulation_data(FILE_NAME, 0.1, 1, 0.95, 100)
    simulation_trades = generate_simulation_2(FILE_NAME, 10, 0.01, 0.98, 180)
    b = calculate_profit(FILE_NAME, simulation_trades, 1)
