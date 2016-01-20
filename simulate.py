# 逻辑简述：新三板市场中，由于单个做市商交易量占总交易的权重很大，所以做市商交易本身会很大的影响市场交易均价；
# 所以做市商市场交易带来两方面的影响，一是影响库存股浮盈，二是直接带来交易的损益（买卖价差导致赚钱或者亏损）
# 当市场价格处在上涨过程中，买卖交易提高了市场平均交易均价，带来了正的库存股浮盈，因此，即使高买低卖，也可能带来总收益（库存股浮盈+交易损益）的增加；
# 而当市场处在下跌过程中，买卖交易降低了市场平均交易均价，造成了库存股浮盈的减少，因此，即使低卖高买，也可能导致总收益（库存股浮盈+交易损益）的减少；
# 本页脚本通过模拟买卖价格，得到不通买卖价格下，对库存股浮盈和交易损益的影响

# 输入数据："是否本人交易"（默认为1，表示本人交易），“交易日期”（默认历史数据的最后一天）, 交易数量（默认最近一个交易日的交易数量），交易单价（规则如下）
# 模拟时改变交易单价，建立6组数据集合；在每组数据集合内，卖出价格不变，买入价格从卖出价格的95%逐渐增加到105%，每次浮动1分钱；
# 6组数据集合，有6个不同的卖出价格，分别为上一个交易日的收盘价，上下浮动+1%, +2%, 3%，-1%, -2%，-3%；
# 最终6组数据集合，形成6张图，每张图的横坐标是买入价格，纵坐标是 库存浮盈 + 交易损益


from calculate_hist import get_transactions, calculate_cost
import numpy
import matplotlib.pyplot as plt


FILE_NAME = 'sample_data.xls'
HISTORICAL_TRANSACTIONS = get_transactions(FILE_NAME)
HISTORICAL_VALUE = calculate_cost(HISTORICAL_TRANSACTIONS)

SELLING_PRICE_RATE = 0.03
SUBPLOTS = 6
PRICE_DIFF = 0.01
BUYING_PRICE_LIMIT = 0.05


# 建立一个数组，这个数组由SUBPLOTS个数组构成，每个子数组包含多组tuple数据，每个tuple含有2个元素，分别表示买入价格和卖出价格
def get_simulation_data(historical_value):
    closing_price = historical_value[-1][5]
    # 下面模拟6(SUBPLOTS)种卖出价格，分别为 前一个交易日的收盘价 上下浮动 一定的比率，目前设置为上下浮动最大值为3%，分为6种情况；即分别为±1%.±2%,±3%
    selling_price_coll = numpy.linspace(closing_price*(1-SELLING_PRICE_RATE),
                                        closing_price*(1+SELLING_PRICE_RATE), SUBPLOTS)
    # 针对每一种卖出价格，计算相应的买入价格，买入价格从卖出价格的95%逐渐增加到105%，每次浮动1分钱
    trade = [[]]
    for dummy_i in range(SUBPLOTS - 1):
        trade += [[]]
    for index in range(SUBPLOTS):
        buying_price_coll = numpy.arange(selling_price_coll[index]*(1-BUYING_PRICE_LIMIT), selling_price_coll[index]*(1+BUYING_PRICE_LIMIT), 0.01)
        for buying_price in buying_price_coll:
            trade[index].append((buying_price, selling_price_coll[index]))
    return trade

# 模拟时现将截止上一个交易日的各项数据返回并保存，然后加上模拟交易数据计算各项指标（库存成本，库存浮盈的变化，交易损益，已经库存浮盈的变化 + 交易损益）
# 截止上一个交易日的数据包括 是否为本人交易、交易日期、交易数量、交易单价；


def calculate_profit(buying_price, selling_price, if_self=1, trade_date=None, trade_qty=0):
    # 根据输入的买入价格及卖出价格，计算 库存浮盈的变动 + 交易损益
    # 首先根据历史数据，返回截至目前为止的交易数据
    if not trade_date:
        trade_date = HISTORICAL_VALUE[-1][0]
    if not trade_qty:
        days = -1
        while HISTORICAL_VALUE[days][1] - HISTORICAL_VALUE[days-1][1] == 0:
            days += 1
        trade_qty = abs(HISTORICAL_VALUE[days][1] - HISTORICAL_VALUE[days-1][1])
    # 增加交易数据，是否为本人交易、交易日期、交易数量、交易单价(买入价和卖出价)，得到新的transactions
    transactions = HISTORICAL_TRANSACTIONS + [(if_self, trade_date, trade_qty, buying_price)] \
                   + [(if_self, trade_date, -trade_qty, selling_price)]
    # 将transactions, stock_qty, stock_price, trade_date, end_date, value, trade_profit, stock_profit, closing_price
    #   参数传入calculate_cost函数，计算得到新的数据
    # 将交易日期、库存股数量、库存股成本、库存股浮盈、累计交易损益、每日收盘价 加入数组；
    stock_qty = HISTORICAL_VALUE[-2][1]
    stock_price = HISTORICAL_VALUE[-2][2]
    end_date = trade_date
    value = HISTORICAL_VALUE
    trade_profit = HISTORICAL_VALUE[-2][3]
    stock_profit = HISTORICAL_VALUE[-2][4]
    closing_price = HISTORICAL_VALUE[-2][5]
    new_value = calculate_cost(transactions, stock_qty, stock_price, trade_date, end_date, value[:-1],
                               trade_profit, stock_profit, closing_price)
    #交易后的 库存浮盈加累计损益 减去 交易前的 库存浮盈加累计损益 ，就是我们要得到的值
    simulation_profit = new_value[-1][3] + new_value[-1][4] - HISTORICAL_VALUE[-1][3] - HISTORICAL_VALUE[-1][4]
    return simulation_profit


if __name__ == "__main__":
    simulation_trades = get_simulation_data(HISTORICAL_VALUE)

    def plot(index):
        trades = simulation_trades[index]
        return_value = []
        for each_trade in trades:
            profit = calculate_profit(each_trade[0], each_trade[1], trade_qty=1000)
            return_value.append((each_trade[0], each_trade[1], profit))
        buy_val = [element[0] for element in return_value]
        profit_val = [element[2] for element in return_value]
        sell_val = return_value[0][1]
        plt.plot(buy_val, profit_val, label="sell price is %s" % sell_val)
        plt.legend(loc=0)
    for index in range(SUBPLOTS):
        plot(index)
    plt.show()