import math
import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QMainWindow, QVBoxLayout, QSizePolicy, QApplication
from PyQt5.QtCore import Qt


class Color(QWidget):
    """
    class that changes the palette color of a widget
    """

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class ClassBox(QWidget):
    """
    Custom Qt Widget to display the class in a box with a minus/ plus sign
    depending on use and a label to indicate match percentage
    """
    buttonClicked = QtCore.pyqtSignal(QWidget)
    classClicked = QtCore.pyqtSignal(QWidget)

    def __init__(self, class_name: str, class_details: dict, parent: QMainWindow = None):
        super(ClassBox, self).__init__()

        self.setParent(parent)
        self.class_details = class_details
        self.course_name = class_name

        self.rgb_color = self.class_details['Color']

        self.plus = True
        self.ai_toggle = True
        self.score = 0

        # Creates widget layout
        # self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        self.lbl = self.name_label()
        self.lbl.clicked.connect(self.onLabelClicked)

        self.btn = self.button()
        self.match_lbl = self.match_percent()
        layout.addWidget(self.lbl)
        self.setLayout(layout)

    from PyQt5.QtWidgets import QPushButton
    from PyQt5.QtCore import Qt
    import random

    from PyQt5.QtWidgets import QPushButton
    from PyQt5.QtCore import Qt
    import random

    def name_label(self):
        """
        Creates label (actually button) that has the name of the course
        :return: parent button that has course name
        """
        label = QPushButton(self.class_name, self)
        label.setCheckable(False)
        label.setAutoDefault(False)
        label

        generated_colors = set()  # To store the generated colors

        if "EC" in self.class_name:
            while True:
                self.rgb_color[0] = r = random.randint(50, 125)  # no red component
                self.rgb_color[1] = g = random.randint(100, 200)  # Green component (100-200 for just a little green
                # tone)
                self.rgb_color[2] = b = random.randint(150, 255)  # Blue component (150-255 for medium-light shades)

                # Generate CSS color string
                color = f"rgb({self.rgb_color[0]}, {self.rgb_color[1]}, {self.rgb_color[2]})"

                # Check if the generated color is significantly different from any previously generated color
                # still need to experiment with values
                # cr, cg, cb are the previously generated colors
                if not any(color_distance((r, g, b), (cr, cg, cb)) < 100 for cr, cg, cb in generated_colors):
                    generated_colors.add((r, g, b))
                    label.setStyleSheet(f'''border-radius: 5px;
                                             border: 2px solid black;
                                             background-color: {color};''')
                    break
        elif "COM" in self.class_name:  # pinkish colors for CS classes
            while True:
                self.rgb_color[0] = r = random.randint(200, 255)  # no red component
                self.rgb_color[1] = g = random.randint(100, 150)  # Green component (100-200 for just a little green
                # tone)
                self.rgb_color[2] = b = random.randint(180, 220)  # Blue component (150-255 for medium-light shades)

                # Generate CSS color string
                color = f"rgb({self.rgb_color[0]}, {self.rgb_color[1]}, {self.rgb_color[2]})"

                # checks the values of the color to make sure there is a difference of at most 100 between them
                if not any(
                        abs(r - cr) < 100 and abs(g - cg) < 100 and abs(b - cb) < 100 for cr, cg, cb in
                        generated_colors):
                    generated_colors.add((r, g, b))
                    label.setStyleSheet(f'''border-radius: 5px;
                                                        border: 2px solid black;
                                                        background-color: {color};''')

        # Fixes text and geometry of the button (NEEDS FIXING)
        font = label.font()
        font.setPointSize(6)  # was 5
        label.setGeometry(0, 0, 145, 80)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        label.setMinimumSize(80, 80)
        label.setMaximumSize(250, 80) # was 170
        label.setFont(font)
        #label.setStyleSheet("font-weight: bold; ")  # This makes the words bold but removes the color from the
        # background of the label except the score portion. Might be a nice potential styling option

        return label

    def button(self) -> QPushButton:
        """
        Creates plus or minus icon button
        :return: plus/ minus icon button
        """

        # creating a push button
        button = QPushButton('', self.lbl)

        if self.plus:
            button.setIcon(QtGui.QIcon('plus-circle.png'))
        else:
            button.setIcon(QtGui.QIcon('minus-circle.png'))

        # Fixes size and position of button (NEEDS FIXING)
        button.setIconSize(QtCore.QSize(20, 20))
        # button.setGeometry(QtCore.QRect(50, 25, 100, 50))
        # button.setFixedSize(20, 20)
        btn_pos = self.lbl.geometry().topRight()
        button.move(btn_pos)

        button.clicked.connect(self.onButtonClicked)

        return button

    def match_percent(self) -> QLabel:
        """
        Label that displays how closely a course option matches the user
        :return: label containing score
        """
        label = QLabel(f'score: {self.score}', self.lbl)
        label.setStyleSheet('''border-radius : 1px;
                                        border: 1px solid black''')
        font = label.font()
        font.setPointSize(5)
        label.resize(50, 20)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        percentage_lbl_pos_x = self.lbl.geometry().center() + QtCore.QPoint(-label.geometry().right() // 4,
                                                                            self.lbl.geometry().bottom() // 2
                                                                            - label.geometry().bottom())
        label.move(percentage_lbl_pos_x)
        label.setVisible(self.ai_toggle)

        return label

    def onButtonClicked(self) -> None:
        """
        Emits signal on buttonpress so that the event can be intercepted by parent window
        :return: None
        """
        self.buttonClicked.emit(self)

    def change_button(self) -> None:
        """
        Changes button between plus/minus icons
        :return: None
        """
        self.plus = not self.plus
        if self.plus:
            self.btn.setIcon(QtGui.QIcon('plus-circle.png'))
        else:
            self.btn.setIcon(QtGui.QIcon('minus-circle.png'))

    def set_score(self, score: int) -> None:
        """
        Sets new score to the label of the widget
        :param score: new score
        :return: None
        """
        self.score = score
        self.match_lbl.setText(f'score: {self.score}')

    def onLabelClicked(self) -> None:
        """
        Opens the hyperlink of the class website on click on the label of the course
        :return: None
        """
        # chr_options = Options()
        # chr_options.add_experimental_option("detach", True)
        # driver = webdriver.Chrome(options=chr_options)
        # driver.get(self.class_details['href'])

        self.classClicked.emit(self)

    @property
    def color(self):
        return self.rgb_color  # rgb_color

    @property
    def class_name(self):
        return self.course_name


def color_distance(color1, color2):
    """
    Calculates the Euclidean distance between two RGB colors.
    :param color1: First RGB color (r, g, b)
    :param color2: Second RGB color (r, g, b)
    :return: Euclidean distance between the two colors
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


if __name__ == "__main__":
    app = QApplication([])
    volume = ClassBox('GG', {})
    volume.show()
    app.exec_()
