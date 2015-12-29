import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        QToolTip.setFont(QFont("SansSerif", 10))
        self.setToolTip('This is a <b>widget</b>')

        btn = QPushButton('Click', self)
        btn.setToolTip("This is a <b>button</b>")
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        btn_quit = QPushButton('Quit', self)
        btn_quit.clicked.connect(QCoreApplication.instance().quit)
        btn_quit.resize(btn_quit.sizeHint())
        btn_quit.move(150, 50)

        # self.setGeometry(300, 300, 300, 100)
        self.resize(300, 100)
        self.center()
        self.setWindowTitle("Have Icon")
        self.setWindowIcon(QIcon('web.jpg'))
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
