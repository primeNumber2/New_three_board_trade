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

def generate_simulation_trades(hist_tran, target_price, target_qty, stock_ratio, buying_price_diff, days):
    # 与上一个策略不同，该策略考虑了市场价格在days时间内，从收盘价变动到目标价格target_price的情况；为了简化策略，假设价格变动是均匀的
    # file_name: 交易数据文件名，stock_ratio: 交易数量占总库存的比例； selling_price_diff: 卖出价格和收盘价之比； buying_price_diff：价差； days: 策略持续时间；
    # 返回 交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、每日收盘价

    # 首先根据历史交易数据，计算各项指标
    # hist_tran = get_transactions(file_name)
    hist_value = calculate_cost(hist_tran, value=[])
    # 返回历史数据最后一个交易日的收盘价，交易日期，库存股数量
    closing_price = hist_value[-1][5]
    closing_date = hist_value[-1][0]
    stock_qty = hist_value[-1][1]
    # 库存股的数量差
    qty_diff = (target_qty - stock_qty) / days

    # 交易数量（买入数量和卖出数量）为库存总量的1%；
    trade_qty = stock_qty * stock_ratio
    # 默认每日的卖出均价是收盘价，默认价格变动是均匀的
    selling_price_coll = numpy.linspace(closing_price, target_price, days)
    # 买入出价格是卖出价乘以买卖价差比例buying_price_diff
    buying_price_coll = selling_price_coll * buying_price_diff
    trans = []
    # 将交易延长到days个交易日
    for day_diff in range(days):
        trans.append((1, closing_date + timedelta(days=day_diff+2), trade_qty + qty_diff, buying_price_coll[day_diff]))
        trans.append((1, closing_date + timedelta(days=day_diff+2), -trade_qty, selling_price_coll[day_diff]))
    return trans


if __name__ == "__main__":
    # a = generate_simulation_data(FILE_NAME, 0.1, 1, 0.95, 100)
    trans = get_transactions(FILE_NAME)
    simulation_trades = generate_simulation_trades(trans, target_price=5, target_qty=1000000, stock_ratio=0.01,
                                                   buying_price_diff=0.98, days=20)
    trans = trans + simulation_trades
    simulation_trades2 = generate_simulation_trades(trans, target_price=6, target_qty=1000000, stock_ratio=0.01,
                                                   buying_price_diff=0.98, days=120)
    trans += simulation_trades2
    value = calculate_cost(trans, value=[])
    plot(value)