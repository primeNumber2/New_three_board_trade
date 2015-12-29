import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        lbl1 = QLabel('first component label', self)
        lbl1.move(15, 10)
        lbl2 = QLabel('second component', self)
        lbl2.move(35, 40)
        lbl3 = QLabel('third component', self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')

        self.show()


class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        ok_btn = QPushButton("ok")
        cancel_btn = QPushButton("cancel")

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(ok_btn)
        h_box.addWidget(cancel_btn)

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Buttons")
        self.show()


class Example0(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        btn1 = QPushButton('OK')
        btn2 = QPushButton('Cancel')
        grid.addWidget(btn1, 0, 0)
        grid.addWidget(btn2, 1, 0)

        self.move(300, 150)
        self.setWindowTitle("Calculator")
        self.show()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        title_edit = QLineEdit()
        author_edit = QLineEdit()
        review_edit = QTextEdit()

        grid = QGridLayout()

        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(review_edit, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Review")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
