import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        self.statusBar().showMessage("Ready")

        self.setWindowTitle('Status bar')
        self.setGeometry(300, 300, 300, 100)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())