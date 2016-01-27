# -*- coding: utf-8 -*-
# 在simulate的基础上增加了UI界面，让用户选择导入的数据文件，并输入各项参数；

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QCheckBox
from calculate_hist import get_transactions, calculate_cost, plot
from simulate import generate_simulation_trades


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.file_address = QLineEdit()
        # 不同阶段phase的界面布局，元素属性是相同的，所以建立一个集合phases，每个阶段append进集合中；
        self.phases = []
        self.phase_num = 3
        for num in range(self.phase_num):
            phase = {"lbl_phase": QLabel("阶段%s: "%(num+1)), "checkbox": QCheckBox("启用该阶段"),
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

        for num in range(self.phase_num):
            self.grid.addWidget(self.phases[num]["lbl_phase"], 3*num, 0)
            self.grid.addWidget(self.phases[num]["checkbox"], 3*num, 1)
            self.grid.addWidget(self.phases[num]["lbl_price_diff"], 3*num+1, 0)
            self.grid.addWidget(self.phases[num]["price_diff"], 3*num+1, 1)
            self.grid.addWidget(self.phases[num]["lbl_target_qty"], 3*num+1, 2)
            self.grid.addWidget(self.phases[num]["target_qty"], 3*num+1, 3)
            self.grid.addWidget(self.phases[num]["lbl_target_price"], 3*num+1, 4)
            self.grid.addWidget(self.phases[num]["target_price"], 3*num+1, 5)
            self.grid.addWidget(self.phases[num]["lbl_trade_qty"], 3*num+2, 0)
            self.grid.addWidget(self.phases[num]["trade_qty"], 3*num+2, 1)
            self.grid.addWidget(self.phases[num]["lbl_days"], 3*num+2, 2)
            self.grid.addWidget(self.phases[num]["days"], 3*num+2, 3)
        
        btn_choose = QPushButton("选择文件", self)
        btn_cost = QPushButton("计算历史成本", self)
        btn_simulation = QPushButton("模拟计算", self)

        self.grid.addWidget(self.file_address, 10, 0)
        self.grid.addWidget(btn_choose, 10, 1)

        self.grid.addWidget(btn_cost, 11, 4)
        self.grid.addWidget(btn_simulation, 11, 5)

        btn_choose.clicked.connect(self.show_dialog)
        btn_cost.clicked.connect(self.hist_plot)
        btn_simulation.clicked.connect(self.simulate_plot)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Main')
        self.show()

    def enable_phase(self):
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
        name = QFileDialog.getOpenFileName(self, 'Open file', r'D:\sync\Projects\pycharmProjects\StockProfit')
        if name[0]:
            self.file_address.setText(str(name[0]))

    def hist_plot(self):
        file_name = self.file_address.text()
        transactions = get_transactions(file_name)
        data = calculate_cost(transactions, value=[])
        plot(data)

    def simulate_plot(self):
        file_name = self.file_address.text()
        hist_tran = get_transactions(file_name)
        for num in range(self.phase_num):
            if self.phases[num]["checkbox"].isChecked():
                stock_ratio = float(self.phases[num]["trade_qty"].text())
                days = int(self.phases[num]["days"].text())
                target_price = float(self.phases[num]["target_price"].text())
                target_qty = float(self.phases[num]["target_qty"].text())
                price_diff = float(self.phases[num]["price_diff"].text())
                simulation_tran = generate_simulation_trades(hist_tran=hist_tran, target_price=target_price, target_qty=target_qty,
                                                             stock_ratio=stock_ratio, buying_price_diff=price_diff, days=days)
                hist_tran += simulation_tran
        value = calculate_cost(hist_tran, value=[])
        plot(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())