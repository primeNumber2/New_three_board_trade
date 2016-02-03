# -*- coding: utf-8 -*-
# 首先将数据转化成后续处理的格式，日期：数量；价格； 数量>0时表示买入，数量<0时表示卖出
from datetime import date, timedelta
import re
import xlrd
import matplotlib.pyplot as plt
from pylab import mpl
import matplotlib




HOLIDAY = [date(2015, 10, 1) + timedelta(days=days) for days in range(7)] + [date(2016, 1, 1) + timedelta(days=days)
                                                                             for days in range(3)] + \
          [date(2016, 2, 7) + timedelta(days=days) for days in range(7)] + [date(2016, 4, 2) + timedelta(days=days)
                                                                            for days in range(3)]


def data_format_conversion(input_date):
    # 将输入的日期，转化为 日期格式；
    # 如果输入的日期类型是字符串，则用正则表达式，把年月日取出来（一定按顺序取出），并转化成datetime.date格式
    # 如果输入的日期类型是整数或者浮点数（excel格式），用xlrd的xldate_as_tuple方法，提取年月日，并转化为日期格式
    # 如果输入的日期类型是datetime.date；则不作处理，返回本身，否则，提示类型错误
    if isinstance(input_date, str):
        nums = re.split('\D+0?', input_date)
        return date(int(nums[0]), int(nums[1]), int(nums[2]))
    elif isinstance(input_date, date):
        return input_date
    elif isinstance(input_date, float) or isinstance(input_date, int):
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(input_date, 0)
        return date(year, month, day)
    else:
        raise TypeError('The format of date is not correct')


def get_transactions(file_name):
    # 将指定格式的Excel转化为包含tuple的list，每个tuple对应一条交易记录
    # 增加一列数字标识，如果是自己的交易记录，则为1，如果是别人的交易记录则为0；
    # 返回的列：是否为本人交易、交易日期、交易数量、交易单价；
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_index(0)
    transactions = []
    # 第一行是列名，最后一行是合计，所以row_number的范围要减去2；
    for row_num in range(worksheet.nrows - 2):
        trade_date = data_format_conversion(worksheet.cell_value(row_num + 1, 2))
        trade_qty = worksheet.cell_value(row_num + 1, 14) if worksheet.cell_value(row_num + 1, 12) == '买入' \
            else -1 * worksheet.cell_value(row_num + 1, 14)
        trade_price = worksheet.cell_value(row_num + 1, 15)
        transactions.append((1, trade_date, trade_qty, trade_price))
        # transactions必须按照日期的顺序进行排序
        transactions.sort(key=lambda x: x[1])
    return transactions


def get_market_average_prices(file_name):
    # 读取Excel，得到每日成交均价，返回dict数据类型，key为日期（date类型),value为成交均价
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_index(0)
    market_average_prices = {}
    for row_num in range(worksheet.nrows - 1):
        trade_date = data_format_conversion(worksheet.cell_value(row_num + 1, 2))
        average_price = worksheet.cell_value(row_num + 1, 3)
        market_average_prices[trade_date] = average_price
    return market_average_prices


def stock_calendar(trade_date, days, holiday):
    # 输入参数为交易日期加上一个天数，如果结果是周末或者节假日，则向后推移直到工作日；
    # 节假日的规则不确定，所以作为参数传入
    new_date = trade_date + timedelta(days=days)
    if new_date.weekday() < 5 and new_date not in holiday:
        return new_date
    else:
        new_date += timedelta(days=1)
        return stock_calendar(new_date, 1, holiday)


def calculate_cost(transactions, market_average_prices, stock_qty=0, stock_cost=0, trade_date=None, end_date=None,
                   value=[], trade_profit_total=0):
    # 根据交易记录计算库存成本,库存股数量,计算方法使用递归，逐日计算成本，用前一个交易日的数据计算下一个交易日的数据
    # trade_date是交易日期，在第一次计算时，使用导入数据的第一个日期作为初始计算日期，后续递归计算时，传入交易日期；
    # end_date是截止日期，如果没有指定，使用导入数据的最后一个日期；
    # 如果交易日期大于截止日期，返回计算结果，否则逐日计算成本；
    # 返回： 交易日期、截止交易日期的库存股数量，截止交易日期的库存股成本，截止交易日期的库存股浮盈，截止交易日期的累计损益，交易日的收盘价
    # 注意：transactions必须按照日期的顺序进行排序
    if not trade_date:
        trade_date = data_format_conversion(transactions[0][1])
    if not end_date:
        end_date = data_format_conversion(transactions[-1][1])
    if trade_date > end_date:
        return value
    else:
        # 分别取出交易日的所有交易记录，别分为买入记录和卖出记录，包含所有人的交易记录
        all_data = list(filter(lambda x: data_format_conversion(x[1]) == trade_date, transactions))
        # 如果交易日有交易数据，则执行下面的计算，否则直接跳过计算过程，将交易日加1天，库存股数量和成本带到下一个交易日；
        if all_data:
            # 将买入记录和卖出记录分成两个数组,此处只取本人交易的记录，市场上其他人的交易不参与计算
            buy_data = list(filter(lambda x: x[2] > 0 and x[0] == 1, all_data))
            sell_data = list(filter(lambda x: x[2] < 0 and x[0] == 1, all_data))
            # 首先计算前一个交易日的库存价值
            # 这里的stock_qty和stock_price都是参数传入的，第一次计算时为0，后面每一次都是上一个交易日的库存股数量和库存股成本；
            stock_value = stock_qty * stock_cost
            # 计算交易损益要使用上一个交易日的库存成本价，所以要在计算当日库存成本之前先计算
            # 计算公式是：累计交易损益 = 前一个交易日的交易损益 + SUM(（当日卖出价格 - 上一个交易日的库存成本） * 卖出数量)
            trade_profit_total += sum([(element[3] - stock_cost) * abs(element[2]) for element in sell_data])
            # 计算库存股数量，前一个交易日的库存股数量，加上当天的所有买卖数量；
            stock_qty += sum([element[2] for element in all_data])
            # 当日的库存价值是 前一个交易日的库存价值 + 买入数量*买入单价 + 卖出数量 * 前一个交易日的成本价， 注意卖出数量是负值；
            stock_value += sum([element[2] * element[3] for element in buy_data]) + sum([element[2] * stock_cost
                                                                                         for element in sell_data])
            # 库存成本是 库存价值/库存股数量 ，取8位小数
            stock_cost = 0 if stock_qty == 0 else round(stock_value / stock_qty, 8)
            # # 当日交易均价，当日所有的买卖交易，SUM(交易价格*交易数量) / SUM(交易数量)， 注意买卖都要取绝对值；
        # 浮盈是 （当日市场交易均价 - 当日库存成本）* 库存股数量，虽然成交明细中可能没有交易，但是市场价格会变化，影响浮盈，所以计算浮盈要在if之外
        stock_float_profit = (market_average_prices[trade_date] - stock_cost) * stock_qty
        # 将交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、市场成交均价 加入数组；
        # 注意，如果当日没有交易，就将数据带到下一个交易日
        value.append((trade_date, stock_qty, stock_cost, stock_float_profit, trade_profit_total,
                      market_average_prices[trade_date]))
        # 交易日加1天，如果是节假日，自动向后移，直到工作日为止
        trade_date = stock_calendar(trade_date, 1, HOLIDAY)
        return calculate_cost(transactions=transactions, market_average_prices=market_average_prices,
                              stock_qty=stock_qty,
                              stock_cost=stock_cost, trade_date=trade_date, end_date=end_date, value=value,
                              trade_profit_total=trade_profit_total)


def plot(*data):
    # 根据calculate_cost函数返回的结果，绘图表示随着时间的变化，
    # 库存股成本、库存股数量、库存股浮盈、累计交易损益， 库存股浮盈+累计交易损益， 市场成交 的变化情况
    # 可以多组数据进行对比

    # 下面两行代码解决中文显示的问题
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['axes.unicode_minus'] = False
    # 建立各个指标的数组
    qty_val = [[] for dummy_i in range(len(data))]
    cost_val = [[] for dummy_i in range(len(data))]
    stock_float_profit = [[] for dummy_i in range(len(data))]
    trade_profit_total = [[] for dummy_i in range(len(data))]
    total_profit = [[] for dummy_i in range(len(data))]
    market_average_price = [[] for dummy_i in range(len(data))]
    label = [[] for dummy_i in range(len(data))]
    for num in range(len(data)):
        qty_val[num] = [element[1] for element in data[num]]
        cost_val[num] = [element[2] for element in data[num]]
        stock_float_profit[num] = [element[3] for element in data[num]]
        trade_profit_total[num] = [element[4] for element in data[num]]
        total_profit[num] = [element[3] + element[4] for element in data[num]]
        market_average_price[num] = [element[5] for element in data[num]]
    plt.figure(num=1, figsize=(16, 8))
    for num in range(len(data)):
        plt.subplot(321)
        plt.title("库存股成本", fontsize=16)
        plt.plot(cost_val[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
        plt.subplot(322)
        plt.title("库存股数量", fontsize=16)
        plt.plot(qty_val[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
        plt.subplot(323)
        plt.title("库存浮盈", fontsize=16)
        plt.plot(stock_float_profit[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
        plt.subplot(324)
        plt.title("累计交易损益", fontsize=16)
        plt.plot(trade_profit_total[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
        plt.subplot(325)
        plt.title("库存浮盈+累计交易损益", fontsize=16)
        plt.plot(total_profit[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
        plt.subplot(326)
        plt.title("市场成交均价", fontsize=16)
        plt.plot(market_average_price[num], label="数据%s" % (num + 1))
        plt.legend(loc=0, fontsize=10)
    plt.show()


if __name__ == '__main__':
    trans1 = get_transactions('update_market_trans.xls')
    trans2 = get_transactions('hist_trans.xls')
    average_prices = get_market_average_prices('update_market_prices.xlsx')
    data1 = calculate_cost(transactions=trans1, market_average_prices=average_prices, value=[])
    data2 = calculate_cost(transactions=trans2, market_average_prices=average_prices, value=[])
    plot(data1, data2)