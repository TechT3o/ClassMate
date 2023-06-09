from gui.filtering_window import FilteringWindow
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import sys
import os


class StartWindow(QWidget):
    """
    Starting window that welcomes user and opens the filtering window
    """

    def __init__(self):
        super().__init__()

        # Create filtering window
        self.filter_window = FilteringWindow()
        self.setWindowTitle("ClassMate")
        self.setStyleSheet("background-color: azure;")  # previous color: darkcyan
        layout = QHBoxLayout()

        layout_v = QVBoxLayout()
        lbl = QLabel('Welcome to Classmate')
        lbl.setFont(QFont('Bodoni MT', 55))
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        button1 = QPushButton("Get Started")
        button1.setStyleSheet("background-color: dodgerblue; color: white; font-weight: bold; ")
        button1.setFont(QFont('Bodoni MT', 15))  # set font family and size
        button1.clicked.connect(self.toggle_filter_window)
        layout_v.addWidget(lbl)
        layout_v.addWidget(button1, alignment=Qt.AlignTop)

        pic = QLabel()
        image = QPixmap(os.path.join(os.pardir, 'Ucla_Pic.jpg'))
        pixmap_resized = image.scaled(512, 512, Qt.KeepAspectRatio)
        pic.setPixmap(pixmap_resized)

        layout.addLayout(layout_v)
        layout.addWidget(pic, alignment=Qt.AlignHCenter)

        self.setLayout(layout)
        self.show()
        self.showFullScreen()

    def toggle_filter_window(self) -> None:
        """
        Toggles filtering window if it is not visible
        :return: None
        """
        if self.filter_window.isVisible():
            self.filter_window.hide()
        else:
            self.filter_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StartWindow()
    w.show()
    app.exec()
