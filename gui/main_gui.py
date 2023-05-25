from class_widget import ClassBox
from constraint_filtering import ConstraintBasedFilter
from calendar_widget import CalendarWidget
from start_window import StartWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore
import sys
from statics import load_dict_from_json
import os
from text_filter import TextFilter


class MainWindow(QMainWindow):
    """
    Main window that has the recommendation results of the AI, and enable addition of classes to interactive calendar
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # creates Start window that welcome user (User login in that page in the future)
        self.start_window = StartWindow()
        self.setWindowTitle("ClassMate")
        self.setVisible(False)
        self.start_window.filter_window.submit_button.clicked.connect(self.load_main_window)

        self.course_dict = {}
        self.load_course_dict()
        self.course_widgets = []

        self.calendar_widget = CalendarWidget(self)
        self.recommendations_widget = QTableWidget(3, 1 + len(self.course_dict) // 3)

        self.create_menu()

        self.text_filter = TextFilter()

    def load_course_dict(self) -> None:
        """
        Loads class details from teh course_data.json generated from the webscrapping script
        :return: None
        """
        self.course_dict = load_dict_from_json(os.path.join(os.pardir, "course_data.json"))

    def _hide_other_windows(self) -> None:
        """
        Hides the starting and filtering windows
        :return: None
        """
        if self.start_window.isVisible():
            self.start_window.hide()
        if self.start_window.filter_window.isVisible():
            self.start_window.filter_window.hide()

    def load_main_window(self):
        """
        Gets the results of the filtering window, creates the constraint based filtering
         and loads the class and calendar widgets
        :return: None
        """

        main_layout = QVBoxLayout()

        # gets constraints from filtering window
        constraints = self.start_window.filter_window.on_submit_button_clicked()
        constraint_based_filter = ConstraintBasedFilter(constraints)

        i = 0
        class_names = list(self.course_dict.keys())

        # Filter widgets
        class_widgets = []
        for class_name in class_names:
            class_box_widget = ClassBox(class_name, self.course_dict[class_name], self)
            if constraint_based_filter.filter_course(class_box_widget.class_details):
                class_box_widget.buttonClicked.connect(self.onClassButtonClicked)
                class_widgets.append(class_box_widget)
        
        # Text Filtering
        text_filtered_widgets = []
        for filtered_class in class_widgets:
            if self.text_filter.rank_classes(filtered_class):
                text_filtered_widgets.append(filtered_class)

        # Place class widgets in recommendation table
        for col in range(self.recommendations_widget.columnCount()):
            for row in range(self.recommendations_widget.rowCount()):
                if i >= len(text_filtered_widgets):
                    break
                table_item = QTableWidgetItem()
                self.recommendations_widget.setCellWidget(row, col, text_filtered_widgets[i])
                self.recommendations_widget.setItem(row, col, table_item)
                self.recommendations_widget.setColumnWidth(col, 300)
                self.recommendations_widget.setRowHeight(row, 150)
                i += 1

        # Add widgets to layout
        main_layout.addWidget(self.recommendations_widget)
        main_layout.addWidget(self.calendar_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setVisible(True)
        self.showFullScreen()
        self._hide_other_windows()

    def onClassButtonClicked(self, class_box_widget: ClassBox) -> None:
        """
        Adds class to calendar view when the plus button is presses and removes it when minus button is clicked.
        It also changes between minus/ plus icons
        :param class_box_widget: classbox widget for which the action happens
        :return: None
        """

        if class_box_widget.plus:
            self.calendar_widget.courses.append(class_box_widget)
            self.calendar_widget.populate_calendar()
        else:
            self.calendar_widget.courses.remove(class_box_widget)
            self.calendar_widget.clear()
            self.calendar_widget.draw_empty_table()
            self.calendar_widget.populate_calendar()
        class_box_widget.change_button()

    def create_menu(self) -> None:
        """
        Creates menu bar with Quit option to quit the full-screen application
        :return: None
        """
        # Create a menu bar
        menubar = self.menuBar()

        # Create a "File" menu
        file_menu = menubar.addMenu("&Quit ClassMate")

        # Create a "Quit" action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(QApplication.quit)

        # Add the "Quit" action to the "File" menu
        file_menu.addAction(quit_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
