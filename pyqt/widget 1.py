import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QFrame, QProgressBar, QCalendarWidget, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, QDate
from PyQt5.QtGui import QColor


class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.stateChanged.connect(self.change_title)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()

    def change_title(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.color = QColor(0, 0, 0)

        btn_r = QPushButton("Red", self)
        btn_r.setCheckable(True)
        btn_r.move(10, 10)
        btn_r.clicked[bool].connect(self.set_color)

        btn_g = QPushButton("Green", self)
        btn_g.setCheckable(True)
        btn_g.move(10, 60)
        btn_g.clicked[bool].connect(self.set_color)

        btn_b = QPushButton("Blue", self)
        btn_b.setCheckable(True)
        btn_b.move(10, 110)
        btn_b.clicked[bool].connect(self.set_color)

        self.frm = QFrame(self)
        self.frm.setGeometry(150, 20, 100, 100)
        self.frm.setStyleSheet("QWidget {background-color: %s}" % self.color.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle("Toggle button")
        self.show()

    def set_color(self, pressed):
        source = self.sender()
        if pressed:
            val = 255
        else:
            val = 0

        if source.text() == "Red":
            self.color.setRed(val)
        elif source.text() == "Green":
            self.color.setGreen(val)
        else:
            self.color.setBlue(val)

        self.frm.setStyleSheet("QFrame {background-color: %s}" % self.color.name())


class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.p_bar = QProgressBar(self)
        self.p_bar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.do_action)

        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()

    def timerEvent(self, *args, **kwargs):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step += 1
        self.p_bar.setValue(self.step)

    def do_action(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText("Start")
        else:
            self.timer.start(1000, self)
            self.btn.setText('Stop')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.show_date)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()

    def show_date(self, date):
        self.lbl.setText(date.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())