from filtering_window import FilteringWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.filter_window = FilteringWindow()

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.toggle_filter_window)
        l.addWidget(button1)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_filter_window(self, checked):
        if self.filter_window.isVisible():
            self.filter_window.hide()

        else:
            self.filter_window.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()