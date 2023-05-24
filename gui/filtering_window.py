from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class FilteringWindow(QWidget):

    def __init__(self):
        super(FilteringWindow, self).__init__()

        self.setWindowTitle("Filter")
        self.setStyleSheet("background-color: darkcyan;")

        layout_main = QVBoxLayout()

        welcome_text = QLabel('Welcome to ClassMate')
        font = welcome_text.font()
        font.setPointSize(30)
        welcome_text.setFont(font)
        welcome_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        description_text = QLabel('Select filtering options or press submit to see all options')
        font = description_text.font()
        font.setPointSize(15)
        description_text.setFont(font)
        description_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        layout_main.addWidget(welcome_text)
        layout_main.addWidget(description_text)


        self.subject_area_checkbox = QComboBox(self)
        self.subject_area_checkbox.addItems(['', 'ECE', 'CS', 'CE'])

        units_layout = QHBoxLayout()
        unit_range = (0, 4)
        self.minimum_val = QSpinBox(self)
        # self.minimum_val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.minimum_val.setSingleStep(1)
        self.minimum_val.setMinimum(unit_range[0])
        self.minimum_val.setMaximum(unit_range[1])
        units_layout.addWidget(self.minimum_val)
        dash = QLabel('-')
        dash.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        units_layout.addWidget(dash)
        self.maximum_val = QSpinBox(self)
        # self.maximum_val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.maximum_val.setSingleStep(1)
        self.maximum_val.setMinimum(unit_range[0])
        self.maximum_val.setMaximum(unit_range[1])
        units_layout.addWidget(self.maximum_val)

        term_layout = QHBoxLayout()
        self.box_fall = QCheckBox('Fall')
        term_layout.addWidget(self.box_fall)
        self.box_winter = QCheckBox('Winter')
        term_layout.addWidget(self.box_winter)
        self.box_spring = QCheckBox('Spring')
        term_layout.addWidget(self.box_spring)

        level_layout = QHBoxLayout()
        self.box_lower = QCheckBox('Lower Division')
        level_layout.addWidget(self.box_lower)
        self.box_upper = QCheckBox('Upper Division')
        level_layout.addWidget(self.box_upper)
        self.box_grad = QCheckBox('Graduate')
        level_layout.addWidget(self.box_grad)

        self.requisites_checkbox = QCheckBox()

        form_layout = QFormLayout()
        form_layout.addRow(QLabel('Subject Area:'), self.subject_area_checkbox)
        form_layout.addRow(QLabel('Units:'), units_layout)
        form_layout.addRow(QLabel('Term:'), term_layout)
        form_layout.addRow(QLabel('Requisites:'), self.requisites_checkbox)
        form_layout.addRow(QLabel('Course Level:'), level_layout)
        layout_main.addLayout(form_layout)

        self.submit_button = QPushButton("Submit")

        layout_main.addWidget(self.submit_button)
        self.setLayout(layout_main)

    def on_submit_button_clicked(self):
        print('submitted')
        # Get the values of the widgets and process them
        fall_checked = self.box_fall.isChecked()
        winter_checked = self.box_winter.isChecked()
        spring_checked = self.box_spring.isChecked()
        subject_area_value = self.subject_area_checkbox.currentText()
        lower_checked = self.box_lower.isChecked()
        upper_checked = self.box_upper.isChecked()
        grad_checked = self.box_grad.isChecked()
        req_checked = self.requisites_checkbox.isChecked()
        min_unit_value = self.minimum_val.value()
        max_unit_value = self.maximum_val.value()


if __name__ == "__main__":
    app = QApplication([])
    window = FilteringWindow()
    window.show()
    app.exec_()