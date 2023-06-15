import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

app = QApplication(sys.argv)
w = MainWindow()
app.exec()
