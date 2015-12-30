# 浮盈的权重和损益的权重是一样；“落袋为安”没有被优先考虑；
# 市场平均交易价格被替换成交易者的平均交易价格，因为市场交易价格只有在一天结束之后才能获得，无法实时获得；


# 第一个函数计算历史数据；
#   输入为每一次的交易数据，包含信息为“交易日期”，“买入价格”，“买入数量”
#   返回  历史买入金额和历史买入数量；后续用于计算库存成本；
#   返回  当日交易金额和当日交易数量；后续用于计算当日均价；注意：买和卖都要取绝对值，不可以正负抵消
#   返回  库存股数量；后续用于计算浮盈和新库存股

# 第二个函数计算一次交易（含一买一卖）
#   输入为第一个函数的返回，卖出价格，卖出数量，买入价格，买入数量，市场交易均价（如果为空，则由第一个函数的返回值 当日交易金额和当日交易数量，加上输入的本次交易，计算获得）
#   返回 损益、浮盈

# 第三个函数是一个模拟系统，模拟不同的价差带来 损益和浮盈的 影响； 价差以0.01元为步长，共计
#   输入为卖出数量，卖出价格，买入数量（默认和卖出数量一致）；单次价差，价差数量（如果输入0.01和100，则会模拟价差从0.01到1元的情况）
#   返回一个数列，数列由tuple组成，每个tuple包含了(价差数量，损益，浮盈， 损益+浮盈）

# 第四个函数是作图函数
#   根据第三个珊瑚的返回值，每个元素建立数组，价差数量为横坐标；损益、浮盈和损益+浮盈为纵坐标
import matplotlib.pyplot as plt
from datetime import date
import xlrd
import tkinter
from tkinter import filedialog



# TRANSACTIONS = [('2015/11/09', 50, 50000), ('2015/11/09', 5, 300), ('2015/11/09', 11, -200), ('2015/11/10', 9, 500), ('2015/11/10', 8, -100)]*100


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
    for row_num in range(worksheet.nrows-1):
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(row_num+1, 0), 0)
        transactions.append((date(year, month, day), worksheet.cell_value(row_num+1, 1), worksheet.cell_value(row_num+1, 2)))
    return transactions


def trade_history(trans):
    # 注意传入参数的分隔符和函数strftime的分割符务必一致
    # 返回买入金额，买入数量，交易金额，交易数量和库存数量
    today_data = list(filter(lambda x: x[0] == date.today().strftime('%Y/%m/%d'), trans))
    buy_data = list(filter(lambda x: x[2] > 0, trans))
    buy_amount_l = []
    buy_qty_l = []
    today_amount_l = []
    today_qty_l = []
    for index in range(len(buy_data)):
        buy_amount_l.append(buy_data[index][1] * buy_data[index][2])
        buy_qty_l.append(buy_data[index][2])
    for index in range(len(today_data)):
        today_amount_l.append(abs(today_data[index][1] * today_data[index][2]))
        today_qty_l.append(abs(today_data[index][2]))
    stock_qty_l = [element[2] for element in trans]
    print(today_qty_l, stock_qty_l)
    return sum(buy_amount_l), sum(buy_qty_l), sum(today_amount_l), sum(today_qty_l), sum(stock_qty_l)


def trade_strategy(history, sell_price, sell_qty, buy_price, buy_qty, average_price=None):
    # 根据历史数据，当前的交易价格和交易数量，得到交易损益、浮盈变化 和 总收益
    history_buy_amount, history_buy_qty, today_amount, today_qty, stock_qty = \
        history[0], history[1], history[2], history[3], history[4]
    # print(buy_qty, buy_price, sell_price, sell_qty, today_qty, today_amount)
    if average_price:
        today_price = average_price
    else:
        today_price = (today_amount + buy_qty * buy_price + abs(sell_price * sell_qty)) / (today_qty + buy_qty + abs(sell_qty))
    stock_cost_before = history_buy_amount * 1.0 / history_buy_qty
    stock_cost_current = (history_buy_amount * 1.0 + buy_qty * buy_price) / (history_buy_qty + buy_qty)
    # 计算之前的浮盈，使用当前的交易均价，而没有采用截止昨天的交易均价，是因为即使没有进行买卖，市场价格仍然在变化，/
    #   这部分浮盈的变化并不是由于交易员的操作所引起的;
    # 如果交易员对单支股票的操作影响超过了50%，则此处会产生较大的误差；
    stock_profit_before = (today_price - stock_cost_before) * stock_qty
    stock_profit_current = (today_price - stock_cost_current) * (stock_qty + buy_qty - abs(sell_qty))
    trade_profit = (sell_price - stock_cost_current) * abs(sell_qty)
    return trade_profit, stock_profit_current - stock_profit_before, trade_profit + stock_profit_current - stock_profit_before


def trade_simulate(sell_price, sell_qty, buy_qty, price_diff,  nums):
    # 模拟交易
    history_info = trade_history(choose_file())
    # history_info = choose_file()
    trades = [(sell_price, sell_qty, sell_price-price_diff*(num+1), buy_qty) for num in range(nums)]
    simulate_result = []
    for num in range(len(trades)):
        simulate_result.append(trade_strategy(history_info, trades[num][0], trades[num][1],trades[num][2],trades[num][3]))
    return simulate_result


def plot(info):
    x_val = range(len(info))
    y_trade_profit = [value[0] for value in info]
    y_stock_profit = [value[1] for value in info]
    y_total_profit = [value[2] for value in info]
    plt.plot(x_val, y_total_profit, label="total profit")
    # plt.plot(x_val, y_trade_profit, label="trade profit")
    # plt.plot(x_val, y_stock_profit, label="stock profit")
    plt.legend(loc="upper left")
    plt.show()


trade_trans = trade_simulate(4.55, 50000, 5000, 0.01, 100)
plot(trade_trans)


