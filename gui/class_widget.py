from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import random as rng


class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class ClassBox(QtWidgets.QWidget):
    """
    Custom Qt Widget to display the class in a box with a minus/ plus sign
    depending on use and a label to indicate match percentage
    """

    def __init__(self, class_name: str, class_details: dict):
        super(ClassBox, self).__init__()

        self.class_details = class_details
        self.class_name = class_name
        self.setFixedSize(200, 100)
        layout = QtWidgets.QVBoxLayout()

        self.plus = True
        self.ai_toggle = True

        self.lbl = self.course_name()
        self.button()
        self.match_percent()
        layout.addWidget(self.lbl)

        self.setLayout(layout)

    def course_name(self):

        label = QtWidgets.QLabel(self.class_name)

        label.setStyleSheet(f'''border-radius : 5px;
                                border: 2px solid black;
                                background-color:rgb({rng.randint(0,255)},{rng.randint(0,255)},{rng.randint(0,255)})''')
        font = label.font()
        font.setPointSize(5)
        label.setGeometry(0, 0, 150, 70)
        # label.resize(150, 90)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        return label

    def button(self):
        # creating a push button
        button = QtWidgets.QPushButton('', self.lbl)

        if self.plus:
            button.setIcon(QtGui.QIcon('plus-circle.png'))
        else:
            button.setIcon(QtGui.QIcon('minus-circle.png'))

        button.setIconSize(QtCore.QSize(20, 20))
        btn_pos = self.lbl.geometry().topRight()
        button.move(btn_pos)
        button.clicked.connect(self.clickme)

        return button

    def match_percent(self, percentage: int = 0):
        label = QtWidgets.QLabel(f'{percentage}% match', self.lbl)
        label.setStyleSheet('''border-radius : 1px;
                                        border: 1px solid black''')
        font = label.font()
        font.setPointSize(5)
        label.resize(50, 20)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        percentage_lbl_pos_x = self.lbl.geometry().center() + QtCore.QPoint(-label.geometry().right()//4, self.lbl.geometry().bottom()//2 - label.geometry().bottom())
        label.move(percentage_lbl_pos_x)
        label.setVisible(self.ai_toggle)

    def clickme(self):
        # printing pressed
        print("pressed")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    volume = ClassBox('peaki', {})
    volume.show()
    app.exec_()