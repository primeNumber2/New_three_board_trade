# 首先将数据转化成后续处理的格式，日期：数量；价格； 数量>0时表示买入，数量<0时表示卖出
from datetime import date, timedelta
import re
import tkinter
from tkinter import filedialog
import xlrd
import matplotlib.pyplot as plt


def data_format_conversion(input_date):
    # 将输入的日期，转化为 日期格式；
    # 如果输入的日期类型是字符串，则用正则表达式，把年月日取出来（一定按顺序取出），并转化成datetime.date格式
    # 如果输入的日期类型是datetime.date；则不作处理，返回本身，否则，提示类型错误
    if type(input_date) is type(''):
        nums = re.split('\D+0?', input_date)
        return date(int(nums[0]), int(nums[1]), int(nums[2]))
    elif type(input_date) is date:
        return input_date
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
    for row_num in range(worksheet.nrows-2):
        year, month, day = worksheet.cell_value(row_num+1, 2).split('-')
        qty = worksheet.cell_value(row_num+1, 14) if worksheet.cell_value(row_num+1, 12) == '买入' else -1 * worksheet.cell_value(row_num+1, 14)
        transactions.append((1, date(int(year), int(month), int(day)), qty, worksheet.cell_value(row_num+1, 15)))
    return transactions


def calculate_cost(transactions, stock_qty=0, stock_price=0, trade_date=None, end_date=None, value=[], trade_profit=0, stock_profit=0, trade_average_price=None):
    # 根据交易记录计算库存成本,库存股数量,计算方法使用递归，逐日计算成本，用前一个交易日的数据计算下一个交易日的数据
    # trade_date是交易日期，在第一次计算时，使用导入数据的第一个日期作为初始计算日期，后续递归计算时，传入交易日期；
    # end_date是截止日期，如果没有指定，使用导入数据的最后一个日期；
    # 如果交易日期大于截止日期，返回计算结果，否则逐日计算成本；
    # 返回： 交易日期、截止交易日期的库存股数量，截止交易日期的库存股成本，截止交易日期的库存股浮盈，截止交易日期的累计损益，交易日的市场成交均价
    if not trade_average_price:
        trade_average_price = transactions[0][3]
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
            stock_value = stock_qty * stock_price
            # 计算交易损益要使用上一个交易日的库存成本价，所以要在计算当日库存成本之前先计算
            # 计算公式是：累计交易损益 = 前一个交易日的交易损益 + SUM(（当日卖出价格 - 上一个交易日的库存成本） * 卖出数量)
            trade_profit += sum([(element[3] - stock_price) * abs(element[2]) for element in sell_data])
            # 计算库存股数量，前一个交易日的库存股数量，加上当天的所有买卖数量；
            stock_qty += sum([element[2] for element in all_data])
            # 当日的库存价值是 前一个交易日的库存价值 + 买入数量*买入单价 + 卖出数量 * 前一个交易日的成本价， 注意卖出数量是负值；
            stock_value += sum([element[2]*element[3] for element in buy_data]) + sum([element[2]*stock_price
                                                                                       for element in sell_data])
            # 库存成本是 库存价值/库存股数量 ，取8位小数
            stock_price = 0 if stock_qty == 0 else round(stock_value / stock_qty, 8)
            # 当日交易均价，当日所有的买卖交易，SUM(交易价格*交易数量) / SUM(交易数量)， 注意买卖都要取绝对值；
            trade_average_price = sum([abs(element[2]*element[3]) for element in all_data]) / sum([abs(element[2]) for element in all_data])
            # 浮盈是 前一个交易日的浮盈 +（当日交易均价 - 当日库存成本）* 库存股数量
            stock_profit += (trade_average_price - stock_price) * stock_qty
        # 将交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、市场交易均价 加入数组；
        # 注意，如果当日没有交易，就将数据带到下一个交易日
        value.append((trade_date, stock_qty, stock_price, stock_profit, trade_profit, trade_average_price))
        # 交易日加1天，然后递归计算
        trade_date += timedelta(days=1)
        return calculate_cost(transactions, stock_qty, stock_price, trade_date, end_date, value, trade_profit, stock_profit, trade_average_price)


def plot(data):
    # 根据calculate_cost函数返回的结果，绘图表示随着时间的变化，
    #   库存股成本、库存股数量、库存股浮盈、累计交易损益以及 库存股浮盈+交易损益 的变化情况
    # x_val = [element[0] for element in data]
    qty_val = [element[1] for element in data]
    cost_val = [element[2] for element in data]
    stock_profit = [element[3] for element in data]
    trade_profit = [element[4] for element in data]
    total_profit = [element[3] + element[4] for element in data]
    trade_price = [element[5] for element in data]
    # plt.ylim(max(cost_val)*1.01, min(cost_val)*0.99)
    # plt.xticks([x_val[0],x_val[int(len(cost_val)/2)] ,x_val[-1]])
    plt.figure(num=1, figsize=(16, 8))
    plt.subplot(321)
    plt.plot(cost_val, label="Stock cost")
    plt.legend(loc=0)
    plt.subplot(322)
    plt.plot(qty_val, label="Stock qty")
    plt.legend(loc=0)
    plt.subplot(323)
    plt.plot(stock_profit, label="Stock profit")
    plt.legend(loc=0)
    plt.subplot(324)
    plt.plot(trade_profit, label="Trade profit")
    plt.legend(loc=0)
    plt.subplot(325)
    plt.plot(total_profit, label="Total profit")
    plt.legend(loc=0)
    plt.subplot(326)
    plt.plot(trade_price, label="Trade price")
    plt.legend(loc=0)
    plt.show()


if __name__ == '__main__':
    trans = get_transactions('sample_data.xls')
    trade = calculate_cost(trans)
    plot(trade)