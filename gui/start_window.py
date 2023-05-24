from filtering_window import FilteringWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.filter_window = FilteringWindow()
        self.setWindowTitle("ClassMate")
        self.setStyleSheet("background-color: darkcyan;")
        layout = QHBoxLayout()

        l = QVBoxLayout()
        label = QLabel('Welcome to Classmate')
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        button1 = QPushButton("Get Started")
        button1.clicked.connect(self.toggle_filter_window)
        l.addWidget(label)
        l.addWidget(button1, alignment=Qt.AlignTop)

        pic = QLabel()
        image = QPixmap('C:\\Users\\thpap\\PycharmProjects\\ClassMate\\Ucla_Pic.jpg')
        pixmap_resized = image.scaled(512, 512, Qt.KeepAspectRatio)
        pic.setPixmap(pixmap_resized)

        # pic.setScaledContents(True)
        layout.addLayout(l)
        layout.addWidget(pic)

        self.setLayout(layout)
        self.show()
        self.showFullScreen()
    def toggle_filter_window(self, checked):
        if self.filter_window.isVisible():
            self.filter_window.hide()

        else:
            self.filter_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StartWindow()
    w.show()
    app.exec()