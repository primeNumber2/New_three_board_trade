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
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_index(0)
    transactions = []
    # 第一行是列名，最后一行是合计
    for row_num in range(worksheet.nrows-2):
        # print(worksheet.cell_value(row_num+1, 2))
        year, month, day = worksheet.cell_value(row_num+1, 2).split('-')
        # year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(row_num+1, 2), 0)
        qty = worksheet.cell_value(row_num+1, 14) if worksheet.cell_value(row_num+1, 12) == '买入' else -1 * worksheet.cell_value(row_num+1, 14)
        transactions.append((1, date(int(year), int(month), int(day)), qty, worksheet.cell_value(row_num+1, 15)))
    return transactions


def calculate_cost(transactions, stock_qty=0, stock_price=0, trade_date=None, end_date=None, value=[], trade_profit=0):
    # 根据交易记录计算库存成本,计算方法使用递归
    if not trade_date:
        trade_date = data_format_conversion(transactions[0][1])
    if not end_date:
        end_date = data_format_conversion(transactions[-1][1])
    print("the date is", trade_date, end_date)
    if trade_date>end_date:
        return value
    else:
        # 分别取出交易日所以交易记录，交易日买入记录，交易日卖出记录
        all_data = list(filter(lambda x: data_format_conversion(x[1]) == trade_date, transactions))
        if all_data:
            # 如果当日有交易，则计算各项财务指标，否则直接跳过
            buy_data = list(filter(lambda x: x[2] > 0, all_data))
            sell_data = list(filter(lambda x: x[2] < 0, all_data))
            stock_value = stock_qty * stock_price
            # 当日交易损益和累计交易损益,计算交易损益要使用上一个交易日的库存成本价，所以先计算
            trade_profit += sum([(element[3] - stock_price) * abs(element[2]) for element in sell_data])
            # 库存股数量
            stock_qty += sum([element[2] for element in all_data])
            # 库存金额是 买入数量*买入单价 + 卖出数量 * 前一个交易日的成本价， 注意卖出数量是负值；
            stock_value += sum([element[2]*element[3] for element in buy_data]) + sum([element[2]*stock_price for element in sell_data])
            # 库存成本是 库存金额/库存股数量 ，取8位小数
            stock_price = 0 if stock_qty ==0 else round(stock_value / stock_qty, 8)
            # 当日交易均价
            trade_average_price = sum([abs(element[2]*element[3]) for element in all_data]) / sum([abs(element[2]) for element in all_data])
            # 浮盈是（当日交易均价 - 当日库存成本）* 库存股数量
            stock_profit = (trade_average_price - stock_price) * stock_qty
            value.append((trade_date, stock_qty, stock_price, stock_profit, trade_profit))
            print(value)
        trade_date += timedelta(days=1)
        return calculate_cost(transactions, stock_qty, stock_price, trade_date, end_date, value, trade_profit)


class Stock:
    def __init__(self, transactions, stock_qty=0, stock_cost=0):
        self.transactions = transactions
        self.stock_qty = stock_qty
        self.stock_cost = stock_cost
        self.trade_date = data_format_conversion(transactions[0][1])
        self.end_date = data_format_conversion(transactions[-1][1])
        self.stock_profit = 0
        self.trade_profit = 0
        self.info = []

    def trade_transactions(self, trade_date):
        return list(filter(lambda x: data_format_conversion(x[1]) == trade_date, self.transactions))

    def calculation(self):
        print(self.trade_date, self.end_date)
        if self.trade_date > self.end_date:
            return self.info
        else:
            all_data = self.trade_transactions(self.trade_date)
            if all_data:
                # 如果当日有交易，则计算各项财务指标，否则直接跳过
                buy_data = list(filter(lambda x: x[2] > 0, all_data))
                sell_data = list(filter(lambda x: x[2] < 0, all_data))
                stock_value = self.stock_qty * self.stock_cost
                # 当日交易损益和累计交易损益,计算交易损益要使用上一个交易日的库存成本价，所以先计算
                self.trade_profit += sum([(element[3] - self.stock_cost) * abs(element[2]) for element in sell_data])
                # 库存股数量
                self.stock_qty += sum([element[2] for element in all_data])
                # 库存金额是 买入数量*买入单价 + 卖出数量 * 前一个交易日的成本价， 注意卖出数量是负值；
                stock_value += sum([element[2]*element[3] for element in buy_data]) + sum([element[2]*self.stock_cost for element in sell_data])
                # 库存成本是 库存金额/库存股数量 ，取8位小数
                stock_price = 0 if self.stock_qty ==0 else round(stock_value / self.stock_qty, 8)
                # 当日交易均价
                trade_average_price = sum([abs(element[2]*element[3]) for element in all_data]) / sum([abs(element[2]) for element in all_data])
                # 浮盈是（当日交易均价 - 当日库存成本）* 库存股数量
                stock_profit = (trade_average_price - stock_price) * self.stock_qty
            self.info.append((self.trade_date, self.stock_qty, self.stock_cost, self.stock_profit, self.trade_profit))
            self.trade_date += timedelta(days=1)
            return self.calculation()
        print(self.info)

    def get_stock_cost(self):
        return [element[2] for element in self.info]

    def get_stock_qty(self):
        return [element[2] for element in self.info]

    def get_trade_profit(self):
        return [element[4] for element in self.info]

    def get_stock_profit(self):
        return [element[3] for element in self.info]


def plot(data):

    # x_val = [i for i in range(len(data))]
    x_val = [element[0] for element in data]
    qty_val = [element[1] for element in data]
    cost_val = [element[2] for element in data]
    # plt.xlim(max(x_val)*1.1, min(x_val)*1.1)
    plt.ylim(max(cost_val)*1.01, min(cost_val)*0.99)
    plt.xticks([x_val[0],x_val[int(len(cost_val)/2)] ,x_val[-1]])
    plt.plot(x_val, cost_val, label="Stock cost")
    plt.legend(loc="upper left")
    # plt.locator_params(tight=True, nbins=4)
    plt.show()


if __name__ == '__main__':
    trans = get_transactions('data.xls')
    trade = calculate_cost(trans)
    plot(trade)
#     stock_1 = Stock(trans)
#     stock_1.calculation()
#     cost_val = stock_1.get_stock_cost()
#     print(cost_val)
#     plt.plot(cost_val, label="Stock cost")
#     plt.show()