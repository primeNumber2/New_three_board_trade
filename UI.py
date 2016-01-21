# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel
from calculate_hist import get_transactions, calculate_cost, plot
from simulate import generate_simulation_data, calculate_profit

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.file_address = QLineEdit()
        self.stock_ratio = QLineEdit("0.01")
        self.selling_price_diff = QLineEdit("1.0")
        self.buying_price_diff = QLineEdit("0.98")
        self.days = QLineEdit("90")


        btn_choose = QPushButton("选择文件", self)
        btn_cost = QPushButton("计算历史成本", self)
        btn_simulation = QPushButton("模拟计算", self)

        lbl_stock = QLabel(self)
        lbl_stock.setText("库存股比例")
        lbl_selling_price = QLabel(self)
        lbl_selling_price.setText("卖价/收盘价 比例")
        lbl_buying_price = QLabel(self)
        lbl_buying_price.setText("买入价/卖出价 比例")
        lbl_days = QLabel(self)
        lbl_days.setText("策略持续时间")

        grid.addWidget(lbl_stock, 1, 0)
        grid.addWidget(self.stock_ratio, 1, 1)
        grid.addWidget(lbl_selling_price, 2, 0)
        grid.addWidget(self.selling_price_diff, 2, 1)
        grid.addWidget(lbl_buying_price, 3, 0)
        grid.addWidget(self.buying_price_diff, 3, 1)
        grid.addWidget(lbl_days, 4, 0)
        grid.addWidget(self.days, 4, 1)

        grid.addWidget(self.file_address, 5, 0)
        grid.addWidget(btn_choose, 5, 1)

        grid.addWidget(btn_cost, 6, 0)
        grid.addWidget(btn_simulation, 6, 1)


        btn_choose.clicked.connect(self.show_dialog)
        btn_cost.clicked.connect(self.show_plot)
        btn_simulation.clicked.connect(self.simulate)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Main')
        self.show()

    def show_dialog(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if name[0]:
            self.file_address.setText(str(name[0]))

    def show_plot(self):
        # sender = self.sender()
        file_name = self.file_address.text()
        transactions = get_transactions(file_name)
        data = calculate_cost(transactions, value=[])
        plot(data)

    def simulate(self):
        file_name = self.file_address.text()
        stock_ratio = float(self.stock_ratio.text())
        selling_price_diff = float(self.selling_price_diff.text())
        buying_price_diff = float(self.buying_price_diff.text())
        days = int(self.days.text())
        simulation_tran = generate_simulation_data(file_name=file_name, stock_ratio=stock_ratio,
                                                   selling_price_diff=selling_price_diff,
                                                   buying_price_diff=buying_price_diff, days=days)
        calculate_profit(file_name=file_name, simulation_tran=simulation_tran, ratio=1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())