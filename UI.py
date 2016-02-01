# -*- coding: utf-8 -*-
# 在simulate的基础上增加了UI界面，让用户选择导入的数据文件，并输入各项参数；
# 此页面可以实现以下几种功能
#   1、根据提供的交易明细及市场成交均价，计算 库存成本、库存股数量、公允价值变动损益、累计交易损益等指标
#   2、用户输入n个交易日之后的目标价位，目标数量，买卖价差，每日交易数量，系统模拟计算 各项指标的 变动情况;
#         为了增加策略的复杂度，可以将策略分为最多3个阶段，每个阶段分别定义 目标数量，买卖价差，每日交易数量，
#   3、用户定义多个策略，并且保存策略，系统对多策略进行对比；并以图形展示

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QCheckBox
from calculate_hist import get_transactions, calculate_cost, plot, get_market_average_prices
from simulate import generate_simulation_data


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # 建立数据集，作图时的对比数据从data_set中读取
        self.data_set = []
        # 使用Grid布局，整个页面分为3大部分，第一部分为导入文件， 第二部分为模拟的策略，第三部分为 对比
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        # 第一部分的布局，用户导入文件 交易数据和市场交易均价； 计算得到各项指标
        # 创建各个对象
        self.tran = QLineEdit()
        self.market_average_price = QLineEdit()
        btn_tran = QPushButton("交易数据", self)
        btn_tran.setObjectName("btn_tran")
        btn_market_average_price = QPushButton("市场交易均价", self)
        btn_market_average_price.setObjectName("btn_market_average_price")
        btn_calculation = QPushButton("计算", self)
        btn_calculation.setObjectName("btn_calculation")
        # 页面布局
        self.grid.addWidget(self.tran, 0, 0)
        self.grid.addWidget(btn_tran, 0, 1)
        self.grid.addWidget(self.market_average_price, 0, 2)
        self.grid.addWidget(btn_market_average_price, 0, 3)
        self.grid.addWidget(btn_calculation, 0, 5)
        # 绑定事件
        btn_tran.clicked.connect(self.show_dialog)
        btn_market_average_price.clicked.connect(self.show_dialog)
        btn_calculation.clicked.connect(self.show_plot)
        # 第二部分的布局，在第一部分的基础上，模拟最多3个阶段的交易策略，因为不同阶段（phase）的界面布局，对象属性是相同的，
        #   所以建立一个集合phases，包括了所有的阶段；
        self.phases = []
        self.phase_num = 3
        for num in range(self.phase_num):
            phase = {"lbl_phase": QLabel("阶段%s: " % (num + 1)), "checkbox": QCheckBox("启用该阶段"),
                     "lbl_price_diff": QLabel("价差 买入价/卖出价"), "price_diff": QLineEdit("0.98"),
                     "lbl_target_qty": QLabel("目标数量"), "target_qty": QLineEdit(),
                     "lbl_target_price": QLabel("目标价格"), "target_price": QLineEdit(),
                     "lbl_trade_qty": QLabel("每日交易数量/库存股"), "trade_qty": QLineEdit("0.01"),
                     "lbl_days": QLabel("持续时间"), "days": QLineEdit("90")}
            for values in phase.values():
                if isinstance(values, QLineEdit):
                    values.setReadOnly(True)
                    values.setStyleSheet("background-color: gray")
                elif isinstance(values, QCheckBox):
                    values.setObjectName("CheckBox%d" % num)
                    values.stateChanged.connect(self.enable_phase)
            self.phases.append(phase)
        # 对阶段内的所有对象进行布局，前3行留给第一部分，从第4行开始，每个阶段占3行，总共占9行
        for num in range(self.phase_num):
            self.grid.addWidget(self.phases[num]["lbl_phase"], 3 * (num + 1), 0)
            self.grid.addWidget(self.phases[num]["checkbox"], 3 * (num + 1), 1)
            self.grid.addWidget(self.phases[num]["lbl_price_diff"], 3 * (num + 1) + 1, 0)
            self.grid.addWidget(self.phases[num]["price_diff"], 3 * (num + 1) + 1, 1)
            self.grid.addWidget(self.phases[num]["lbl_target_qty"], 3 * (num + 1) + 1, 2)
            self.grid.addWidget(self.phases[num]["target_qty"], 3 * (num + 1) + 1, 3)
            self.grid.addWidget(self.phases[num]["lbl_target_price"], 3 * (num + 1) + 1, 4)
            self.grid.addWidget(self.phases[num]["target_price"], 3 * (num + 1) + 1, 5)
            self.grid.addWidget(self.phases[num]["lbl_trade_qty"], 3 * (num + 1) + 2, 0)
            self.grid.addWidget(self.phases[num]["trade_qty"], 3 * (num + 1) + 2, 1)
            self.grid.addWidget(self.phases[num]["lbl_days"], 3 * (num + 1) + 2, 2)
            self.grid.addWidget(self.phases[num]["days"], 3 * (num + 1) + 2, 3)
        # 布局的第三部分，保存策略并对比
        btn_save_strategy = QPushButton("保存策略", self)
        btn_save_strategy.setObjectName("btn_save_strategy")
        btn_del_strategy = QPushButton("删除策略", self)
        btn_del_strategy.setObjectName("btn_del_strategy")
        self.lbl_num = QLabel("策略数量: 0")

        btn_contrast = QPushButton("对比", self)
        btn_contrast.setObjectName("btn_contrast")

        self.grid.addWidget(btn_save_strategy, 14, 0)
        self.grid.addWidget(self.lbl_num, 14, 1)
        self.grid.addWidget(btn_del_strategy, 14, 2)
        self.grid.addWidget(btn_contrast, 14, 5)


        btn_save_strategy.clicked.connect(self.update_strategy)
        btn_del_strategy.clicked.connect(self.update_strategy)
        btn_contrast.clicked.connect(self.show_plot)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Main')
        self.show()

    def enable_phase(self):
        # 如果复选框被选中，则QLineEdit可以输入数据，且背景为白色，否则为黑色
        sender = self.sender()
        num = sender.objectName()[-1]
        for element in self.phases[int(num)].values():
            if isinstance(element, QLineEdit) and sender.isChecked():
                element.setReadOnly(False)
                element.setStyleSheet("background-color: white")
            elif isinstance(element, QLineEdit) and not sender.isChecked():
                element.setReadOnly(True)
                element.setStyleSheet("background-color: grey")

    def show_dialog(self):
        # 弹出选择文件的对话框，根据sender的objectName，判断返回的文件名更新哪个QLineEdit
        sender = self.sender()
        name = QFileDialog.getOpenFileName(self, 'Open file', r'D:\sync\Projects\pycharmProjects\StockProfit')
        if name[0] and sender.objectName() == "btn_tran":
            self.tran.setText(str(name[0]))
        elif name[0] and sender.objectName() == "btn_market_average_price":
            self.market_average_price.setText(str(name[0]))

    def calculation(self):
        transactions = get_transactions(self.tran.text())
        market_average_prices = get_market_average_prices(self.market_average_price.text())
        for num in range(self.phase_num):
            if self.phases[num]["checkbox"].isChecked():
                stock_ratio = float(self.phases[num]["trade_qty"].text())
                days = int(self.phases[num]["days"].text())
                target_price = float(self.phases[num]["target_price"].text())
                target_qty = float(self.phases[num]["target_qty"].text())
                price_diff = float(self.phases[num]["price_diff"].text())
                transactions, market_average_prices = generate_simulation_data(hist_tran=transactions,
                                                                               market_average_prices=market_average_prices,
                                                                               target_price=target_price,
                                                                               target_qty=target_qty,
                                                                               stock_ratio=stock_ratio,
                                                                               price_diff_ratio=price_diff,
                                                                               days=days)
        data = calculate_cost(transactions, market_average_prices, value=[])
        return data

    def show_plot(self):
        sender = self.sender()
        if sender.objectName() == "btn_calculation":
            data = self.calculation()
            plot(data)
        elif sender.objectName() == "btn_contrast":
            plot(*self.data_set)

    def update_strategy(self):
        sender = self.sender()
        if sender.objectName() == "btn_save_strategy":
            data = self.calculation()
            self.data_set.append(data)
        elif sender.objectName() == "btn_del_strategy":
            self.data_set.pop()
        self.lbl_num.setText("策略数量： %s" % len(self.data_set))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())