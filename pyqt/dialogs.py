import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFrame, QColorDialog, \
    QVBoxLayout, QSizePolicy, QFontDialog, QLabel, QTextEdit, QMainWindow, QAction, QFileDialog

from PyQt5.QtGui import QColor, QIcon


class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        self.btn = QPushButton("Dialog", self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input dialog', 'Enter your name:')
        if ok:
            self.le.setText(str(text))


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.show_dialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget {background-color: %s}" % col.name())

        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color Dialog')
        self.show()

    def show_dialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget {background-color: %s}" % col.name())


class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        v_box = QVBoxLayout()

        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.move(20, 20)
        v_box.addWidget(btn)

        btn.clicked.connect(self.show_dialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        v_box.addWidget(self.lbl)
        self.setLayout(v_box)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Font dialog')
        self.show()

    def show_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.statusBar()

        open_file = QAction(QIcon('web.jpg'), 'Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new file')
        open_file.triggered.connect(self.show_dialog)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_file)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def show_dialog(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if name[0]:
            f = open(name[0], 'r')
            with f:
                data = f.read()
                self.text_edit.setText(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())