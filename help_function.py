# 首先将数据转化成后续处理的格式，日期：数量；价格； 数量>0时表示买入，数量<0时表示卖出
from datetime import date, timedelta
import re
import tkinter
from tkinter import filedialog
import xlrd
import matplotlib.pyplot as plt


def data_format_conversion(input_date):
    # 如果输入的日期类型是字符串，则用正则表达式，把年月日取出来（一定按顺序取出），并转化成datetime.date格式
    # 如果输入的日期类型是datetime.date；则不作处理，返回本身，否则，提示类型错误
    # 将日期由字符串转化为datetime.date类型
    if type(input_date) is type(''):
        nums = re.split('\D+0?', input_date)
        return date(int(nums[0]), int(nums[1]), int(nums[2]))
    elif type(input_date) is date:
        return input_date
    else:
        raise TypeError('The format of date is not correct')


def due_date_info_summary(transactions, due_date=None):
    # 计算截止到指定日期时，买入数量,买入金额, 库存股数量
    # 如果没有指定截止日，则默认为昨天
    if not due_date:
        due_date = date.today() - timedelta(days=1)
    elif type(due_date) is type(''):
        due_date = data_format_conversion(due_date)
    all_data = list(filter(lambda x: data_format_conversion(x[1]) <= due_date,  transactions))
    buy_data = list(filter(lambda x: x[2] > 0, all_data))
    return sum([element[2] for element in buy_data]), sum(list(map(lambda x: x[2]*x[3], buy_data))), \
           sum([element[2] for element in all_data])


def trade(stock_qty, stock_cost,  sell_qty, sell_price, price_diff):
    stock_cost_current = sell_qty * stock_cost + price_diff
    trade_profit = (sell_price - stock_cost_current) * sell_qty
    stock_profit = (stock_cost_current - stock_cost) * stock_qty
    return trade_profit + stock_profit


def calculate_profit(transactions, target_date=None, trade_average_price=None):
    # 计算截止到目前为止的交易损益和浮盈
    # 针对传入的target_date做格式转换，如果传入为空，则默认为当天；如果传入的格式为字符串，则转化为日期
    if not target_date:
        target_date = date.today()
    elif type(target_date) is type(''):
        target_date = data_format_conversion(target_date)
    # 以目标日的前一天作为截止日，返回买入数量、买入金额和库存数量；计算库存成本；
    due_date_info = due_date_info_summary(transactions, due_date=target_date - timedelta(days=1))
    due_date_stock_cost = due_date_info[1] / due_date_info[0]

    target_date_info = due_date_info_summary(transactions, target_date)
    target_date_stock_cost = target_date_info[1] / target_date_info[0]
    # 将目标日的交易数据单据取出来，后续用于计算当日成交均价和浮盈
    # （当日成交均价 - 目标日的库存成本） * 库存股数量 等于浮盈
    data = list(filter(lambda x: data_format_conversion(x[1]) == target_date, transactions))
    if not trade_average_price:
        trade_average_price = sum([abs(element[2]*element[3]) for element in data]) / sum( [abs(element[2]) for element in data] )
    print(trade_average_price)
    print(sum([element[2] for element in data]) + due_date_info[2])
    print(due_date_stock_cost, target_date_stock_cost)
    stock_profit = (trade_average_price - target_date_stock_cost) * (sum([element[2] for element in data]) + due_date_info[2])
    # 将本做市商的卖出数据取出，后续计算交易损益
    # 交易损益等于 每一笔 （卖出价格 - 上一个交易日的库存成本） * 卖出数量 的 汇总
    sell_data = list(filter(lambda x: x[2] < 0 and x[0] == 1, data))
    trade_profit = sum([(element[3] - due_date_stock_cost) * abs(element[2]) for element in sell_data])
    return stock_profit, trade_profit


def get_transactions(file_name):
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_index(0)
    transactions = []
    # 最后一行是合计
    for row_num in range(worksheet.nrows-2):
        # print(worksheet.cell_value(row_num+1, 2))
        year, month, day = worksheet.cell_value(row_num+1, 2).split('-')
        # year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(row_num+1, 2), 0)
        qty = worksheet.cell_value(row_num+1, 14) if worksheet.cell_value(row_num+1, 12) == '买入' else -1 * worksheet.cell_value(row_num+1, 14)
        transactions.append((1, date(int(year), int(month), int(day)), qty, worksheet.cell_value(row_num+1, 15)))
    return transactions


def choose_file():
    """
    让用户选择要导入的文件，并返回文件的绝对路径
    :return: 导入的Excel文件绝对地址 filename
    """
    root = tkinter.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename()
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_index(0)
    transactions = []
    # 最后一行是合计
    for row_num in range(worksheet.nrows-2):
        # print(worksheet.cell_value(row_num+1, 2))
        year, month, day = worksheet.cell_value(row_num+1, 2).split('-')
        # year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(row_num+1, 2), 0)
        qty = worksheet.cell_value(row_num+1, 14) if worksheet.cell_value(row_num+1, 12) == '买入' else -1 * worksheet.cell_value(row_num+1, 14)
        transactions.append((1, date(int(year), int(month), int(day)), qty, worksheet.cell_value(row_num+1, 15)))
    return transactions


def calculate_cost(transactions, stock_qty, stock_price, due_date):
    # 计算方法为 历史买入金额 除以 历史买入数量
    if due_date == date(2015, 10, 30):
        # print(stock_price, stock_qty)
        return stock_qty, stock_price
    else:
        print(due_date, stock_qty, stock_price)
        all_data = list(filter(lambda x: data_format_conversion(x[1]) == due_date, transactions))
        buy_data = list(filter(lambda x: x[2] > 0, all_data))
        sell_data = list(filter(lambda x: x[2] < 0, all_data))
        stock_value = stock_qty * stock_price
        stock_qty += sum([element[2] for element in buy_data])
        stock_value += sum([element[2]*element[3] for element in buy_data])
        stock_price = round(stock_value / stock_qty, 8)
        print(stock_price, stock_qty)
        due_date += timedelta(days=1)
        calculate_cost(transactions, stock_qty, stock_price, due_date)


def calculate_cost_2(transactions, stock_qty=0, stock_price=0, trade_date=None, end_date=None, value=[]):
    # 方法2在计算库存成本时，考虑了股票卖出对成本的影响
    #
    if not trade_date:
        trade_date = transactions[0][1]
    if not end_date:
        end_date = transactions[-1][1]
    if trade_date > end_date:
        return value
    else:
        all_data = list(filter(lambda x: data_format_conversion(x[1]) == trade_date, transactions))
        buy_data = list(filter(lambda x: x[2] > 0, all_data))
        sell_data = list(filter(lambda x: x[2] < 0, all_data))
        stock_value = stock_qty * stock_price
        # 库存股数量
        stock_qty += sum([element[2] for element in all_data])
        # 库存金额是 买入数量*买入单价 + 卖出数量 * 前一个交易日的成本价， 注意卖出数量是负值；
        stock_value += sum([element[2]*element[3] for element in buy_data]) + sum([element[2]*stock_price for element in sell_data])
        # 库存成本是 库存金额/库存股数量 ，取8位小数
        stock_price = round(stock_value / stock_qty, 8)
        # 库存浮盈 = （当日市场成交均价 - 当日库存成本） * 库存股数量
        # 当日市场成交均价 = sum(abs(qty) * price)/ sum(qty)
        market_price = sum([abs(element[2])*element[3] for element in all_data]) / sum([abs[element[2]] for element in all_data])
        value.append((trade_date, stock_qty, stock_price))
        trade_date += timedelta(days=1)
        return calculate_cost_2(transactions, stock_qty, stock_price, trade_date, end_date, value)


def legend(trade_data):
    print(type(trade_data[0][0]))
    x_val = [element[0] for element in trade_data]
    qty_val = [element[1] for element in trade_data]
    cost_val = [element[2] for element in trade_data]
    plt.plot(x_val, cost_val, label="Stock cost")
    plt.legend(loc="upper left")
    plt.locator_params(tight=True, nbins=4)
    plt.show()


if __name__ == "__main__":
    trans = choose_file()
    data = calculate_cost_2(trans)
    legend(data)