from class_widget import ClassBox
from start_window import StartWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from statics import load_dict_from_json
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.start_window = StartWindow()
        self.setWindowTitle("ClassMate")
        self.setVisible(False)
        self.start_window.filter_window.submit_button.clicked.connect(self.load_main_window)

        self.course_dict = {}
        self.load_course_dict()

    def load_course_dict(self):
        self.course_dict = load_dict_from_json(os.path.join(os.pardir, "course_data.json"))

    def _hide_other_windows(self):
        if self.start_window.isVisible():
            self.start_window.hide()
        if self.start_window.filter_window.isVisible():
            self.start_window.filter_window.hide()

    def load_main_window(self):
        print('Entered')

        self.start_window.filter_window.on_submit_button_clicked()

        main_layout = QVBoxLayout()

        working_layout = QHBoxLayout()
        working_layout.addWidget(QLabel('Working'))
        recommendation_widget = QFormLayout()

        calendar_widget = QLabel('Calendar')
        #
        # for class_name in list(self.course_dict.keys())[:5]:
        #     class_box_widget = ClassBox(class_name, self.course_dict[class_name])
        #     recommendation_widget.addRow(class_box_widget)

        # class_box_widget = ClassBox('peos', self.course_dict[list(self.course_dict.keys())[0]])

        table_widget = QTableWidget(3, 1+len(self.course_dict)//3)
        i = 0
        class_names = list(self.course_dict.keys())
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                if i >= len(class_names):
                    break
                class_box_widget = ClassBox(class_names[i], self.course_dict[class_names[i]])
                i += 1
                table_item = QTableWidgetItem()
                table_widget.setCellWidget(row, col, class_box_widget)
                table_widget.setItem(row, col, table_item)
                table_widget.setColumnWidth(col, 300)
                table_widget.setRowHeight(row, 150)

        main_layout.addLayout(working_layout)
        main_layout.addWidget(table_widget)
        main_layout.addWidget(calendar_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.setVisible(True)
        self.show()
        self.showFullScreen()
        print('Shown')
        self._hide_other_windows()
    #
    # def populate_recommendations(self):
    #     for row in range(self.table_widget.rowCount()):
    #         for col in range(self.table_widget.columnCount()):
    #             custom_widget = CustomWidget(f"Widget {row}-{col}")
    #             table_item = QTableWidgetItem()
    #             self.table_widget.setCellWidget(row, col, custom_widget)
    #             self.table_widget.setItem(row, col, table_item)


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
