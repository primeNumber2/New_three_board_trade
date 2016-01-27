# -*- coding: utf-8 -*-
# 在simulate的基础上增加了UI界面，让用户选择导入的数据文件，并输入各项参数；

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QCheckBox
from calculate_hist import get_transactions, calculate_cost, plot
from simulate import generate_simulation_trades, calculate_profit


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.file_address = QLineEdit()

        lbl_phase1 = QLabel("阶段一: ")
        lbl_price_diff1 = QLabel("价差 买入价/卖出价")
        lbl_target_qty1 = QLabel("目标数量")
        lbl_target_price1 = QLabel("目标价格")
        lbl_trade_qty1 = QLabel("每日交易数量")
        lbl_days1 = QLabel("持续时间")

        lbl_phase2 = QLabel("阶段二: ")
        lbl_price_diff2 = QLabel("价差 买入价/卖出价")
        lbl_target_qty2 = QLabel("目标数量")
        lbl_target_price2 = QLabel("目标价格")
        lbl_trade_qty2 = QLabel("每日交易数量")
        lbl_days2 = QLabel("持续时间")


        lbl_phase3 = QLabel("阶段三: ")
        lbl_price_diff3 = QLabel("价差 买入价/卖出价")
        lbl_target_qty3 = QLabel("目标数量")
        lbl_target_price3 = QLabel("目标价格")
        lbl_trade_qty3 = QLabel("每日交易数量")
        lbl_days3 = QLabel("持续时间")

        self.trade_qty1 = QLineEdit("0.01")
        self.price_diff1 = QLineEdit("0.98")
        self.target_qty1 = QLineEdit()
        self.target_price1 = QLineEdit()
        self.days1 = QLineEdit("90")
        self.check1 = QCheckBox("启用该阶段", checked=True)

        self.check2 = QCheckBox("启用该阶段")
        self.check2.stateChanged.connect(self.enable_phase2)
        self.trade_qty2 = QLineEdit()
        self.trade_qty2.setReadOnly(True)
        self.trade_qty2.setStyleSheet("background-color: grey")
        self.price_diff2 = QLineEdit()
        self.price_diff2.setReadOnly(True)
        self.price_diff2.setStyleSheet("background-color: grey")
        self.target_qty2 = QLineEdit()
        self.target_qty2.setReadOnly(True)
        self.target_qty2.setStyleSheet("background-color: grey")
        self.target_price2 = QLineEdit()
        self.target_price2.setReadOnly(True)
        self.target_price2.setStyleSheet("background-color: grey")
        self.days2 = QLineEdit()
        self.days2.setReadOnly(True)
        self.days2.setStyleSheet("background-color: grey")

        self.trade_qty3 = QLineEdit()
        self.price_diff3 = QLineEdit()
        self.target_qty3 = QLineEdit()
        self.target_price3 = QLineEdit()
        self.days3 = QLineEdit()
        self.check3 = QCheckBox("启用该阶段")
        
        btn_choose = QPushButton("选择文件", self)
        btn_cost = QPushButton("计算历史成本", self)
        btn_simulation = QPushButton("模拟计算", self)

        self.grid.addWidget(lbl_phase1, 0, 0)
        self.grid.addWidget(self.check1, 0, 1)
        self.grid.addWidget(lbl_price_diff1, 1, 0)
        self.grid.addWidget(self.price_diff1, 1, 1)
        self.grid.addWidget(lbl_target_qty1, 1, 2)
        self.grid.addWidget(self.target_qty1, 1, 3)
        self.grid.addWidget(lbl_target_price1, 1, 4)
        self.grid.addWidget(self.target_price1, 1, 5)
        self.grid.addWidget(lbl_trade_qty1, 2, 0)
        self.grid.addWidget(self.trade_qty1, 2, 1)
        self.grid.addWidget(lbl_days1, 2, 2)
        self.grid.addWidget(self.days1, 2, 3)

        self.grid.addWidget(lbl_phase2, 3, 0)
        self.grid.addWidget(self.check2, 3, 1)
        self.grid.addWidget(lbl_price_diff2, 4, 0)
        self.grid.addWidget(self.price_diff2, 4, 1)
        self.grid.addWidget(lbl_target_qty2, 4, 2)
        self.grid.addWidget(self.target_qty2, 4, 3)
        self.grid.addWidget(lbl_target_price2, 4, 4)
        self.grid.addWidget(self.target_price2, 4, 5)
        self.grid.addWidget(lbl_trade_qty2, 5, 0)
        self.grid.addWidget(self.trade_qty2, 5, 1)
        self.grid.addWidget(lbl_days2, 5, 2)
        self.grid.addWidget(self.days2, 5, 3)

        self.grid.addWidget(lbl_phase3, 6, 0)
        self.grid.addWidget(self.check3, 6, 1)
        self.grid.addWidget(lbl_price_diff3, 7, 0)
        self.grid.addWidget(self.price_diff3, 7, 1)
        self.grid.addWidget(lbl_target_qty3, 7, 3)
        self.grid.addWidget(self.target_qty3, 7, 3)
        self.grid.addWidget(lbl_target_price3, 7, 4)
        self.grid.addWidget(self.target_price3, 7, 5)
        self.grid.addWidget(lbl_trade_qty3, 8, 0)
        self.grid.addWidget(self.trade_qty3, 8, 1)
        self.grid.addWidget(lbl_days3, 8, 2)
        self.grid.addWidget(self.days3, 8, 3)

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

    def enable_phase2(self):
        if self.check2.isChecked():
            self.trade_qty2.setReadOnly(False)
            self.trade_qty2.setStyleSheet("background-color: white")
            self.price_diff2.setReadOnly(False)
            self.price_diff2.setStyleSheet("background-color: white")
            self.target_qty2.setReadOnly(False)
            self.target_qty2.setStyleSheet("background-color: white")
            self.target_price2.setReadOnly(False)
            self.target_price2.setStyleSheet("background-color: white")
            self.days2.setReadOnly(False)
            self.days2.setStyleSheet("background-color: white")
        else:
            self.trade_qty2.setReadOnly(True)
            self.trade_qty2.setStyleSheet("background-color: grey")
            self.price_diff2.setReadOnly(True)
            self.price_diff2.setStyleSheet("background-color: grey")
            self.target_qty2.setReadOnly(True)
            self.target_qty2.setStyleSheet("background-color: grey")
            self.target_price2.setReadOnly(True)
            self.target_price2.setStyleSheet("background-color: grey")
            self.days2.setReadOnly(True)
            self.days2.setStyleSheet("background-color: grey")
        # self.trade_qty2.setReadOnly(False)
        # self.trade_qty2.setStyleSheet("background-color: white")

    def show_dialog(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if name[0]:
            self.file_address.setText(str(name[0]))

    def hist_plot(self):
        file_name = self.file_address.text()
        transactions = get_transactions(file_name)
        data = calculate_cost(transactions, value=[])
        plot(data)


    def simulate_plot(self):
        file_name = self.file_address.text()
        stock_ratio = float(self.stock_ratio.text())
        buying_price_diff = float(self.buying_price_diff.text())
        days = int(self.days.text())
        target_price = float(self.target_price.text())
        simulation_tran = generate_simulation_trades(file_name=file_name, target_price=target_price,
                                                     stock_ratio=stock_ratio, buying_price_diff=buying_price_diff, days=days)
        calculate_profit(file_name=file_name, simulation_tran=simulation_tran, ratio=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())