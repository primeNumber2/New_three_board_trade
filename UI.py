import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog
from calculate_hist import get_transactions, calculate_cost, plot


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.file_address = QLineEdit()
        btn_choose = QPushButton("选择文件", self)
        btn_cost = QPushButton("计算成本", self)
        grid.addWidget(self.file_address, 0, 0)
        grid.addWidget(btn_choose, 0, 1)
        grid.addWidget(btn_cost, 1, 0)

        btn_choose.clicked.connect(self.show_dialog)
        btn_cost.clicked.connect(self.show_plot, 1)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Main')
        self.show()

    def show_dialog(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if name[0]:
            self.file_address.setText(str(name[0]))

    def show_plot(self, num):
        # sender = self.sender()
        file_name = self.file_address.text()
        transactions = get_transactions(file_name)
        data = calculate_cost(transactions)
        plot(data, num)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())