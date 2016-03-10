# -*- coding: utf-8 -*-

# 逻辑简述：新三板市场中，由于单个做市商交易量占总交易的权重很大，所以做市商交易本身会很大的影响市场交易均价；
# 所以做市商市场交易带来两方面的影响，一是影响库存股的公允价值，二是直接带来投资损益


# 根据历史交易记录，加上模拟形成的交易记录，计算各项指标并绘图；

from calculate_hist import get_transactions, calculate_cost, plot, get_market_average_prices, stock_calendar, HOLIDAY
from datetime import timedelta
import numpy

TRANS_FILE_NAME = 'hist_trans.xls'
MARKET_PRICE_FILE_NAME = 'update_market_prices.xlsx'


def generate_simulation_data(hist_tran, market_average_prices, target_price, target_qty, stock_ratio,
                               price_diff_ratio, days):
    # 根据输入的约束条件，返回模拟的成交明细
    # hist_tran: 历史交易明细数据，数据格式和函数get_transactions的返回值相同；
    # market_average_prices: 市场成交均价，数据格式和get_market_average_prices相同；
    # target_price: 目标价位； target_qty: 库存股目标数量； stock_ratio: 交易的股票占库存股的比例； 卖出价格和收盘价之比； rice_diff_ratio：买卖价差； days: 策略持续时间；
    # 返回 是否本人交易，交易日期，交易数量，交易价格

    # 首先根据历史交易数据，计算各项指标
    hist_value = calculate_cost(hist_tran, market_average_prices, value=[])
    # 返回历史数据最后一个交易日的市场成交均价，交易日期，库存股数量
    closing_date = hist_value[-1][0]
    closing_price = market_average_prices[closing_date]
    stock_qty = hist_value[-1][1]
    # 库存股的数量差，表示以后每天要实现的交易数量差
    qty_diff = (target_qty - stock_qty) / days
    # 交易数量（买入数量和卖出数量）为库存总量的百分比；
    trade_qty = stock_qty * stock_ratio
    # 模拟每日的市场成交均价： 历史交易最后一天的 价格 均匀变动到 目标价格
    average_prices = numpy.linspace(closing_price, target_price, days)
    # 买入、卖出价格是市场成交均价价乘以买卖价差比例（1±(1-price_diff_ratio)/2）
    buying_prices = average_prices * (1.5 - price_diff_ratio/2)
    selling_prices = average_prices * (0.5 + price_diff_ratio/2)
    # 模拟N个交易日的交易与市场交易均价
    trade_date = closing_date
    for day_diff in range(days):
        trade_date = stock_calendar(trade_date, 1, HOLIDAY)
        hist_tran.append((1, trade_date, trade_qty + qty_diff, buying_prices[day_diff]))
        hist_tran.append((1, trade_date, -trade_qty, selling_prices[day_diff]))
        market_average_prices[trade_date] = average_prices[day_diff]
    return hist_tran, market_average_prices


if __name__ == "__main__":
    hist_trans = get_transactions(TRANS_FILE_NAME)
    hist_market_average_prices = get_market_average_prices(MARKET_PRICE_FILE_NAME)
    simulation_trans, simulation_market_average_prices = generate_simulation_data(hist_trans,
                                                                                  hist_market_average_prices,
                                                                                  target_price=5.13, target_qty=886000,
                                                                                  stock_ratio=0.01,
                                                                                  price_diff_ratio=0.98, days=60)
    data1 = calculate_cost(simulation_trans, simulation_market_average_prices, value=[])
    data2 = calculate_cost(get_transactions('update_trans.xls'), get_market_average_prices(MARKET_PRICE_FILE_NAME),
                           value=[])
    plot(*[data1, data2])