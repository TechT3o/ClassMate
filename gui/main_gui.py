from class_widget import ClassBox
from calendar_widget import CalendarWidget
from start_window import StartWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os
from text_filter import TextFilter
from PyQt5.QtCore import Qt


from constraint_filtering import ConstraintBasedFilter
from statics import load_dict_from_json

class MainWindow(QMainWindow):
    """
    Main window that has the recommendation results of the AI, enables addition of classes to interactive calendar,
    has webview of class details and the prompt to communicate with the language model
    """

    def __init__(self):
        super(MainWindow, self).__init__(None)

        # creates Start window that welcome user (User login in that page in the future)
        self.start_window = StartWindow()
        self.setWindowTitle("ClassMate")
        self.setVisible(False)
        self.start_window.filter_window.submit_button.clicked.connect(self.load_main_window)

        self.create_menu()

        # Define class attributes
        self.course_dict = {}
        self.class_names = []
        self.course_widgets = []
        self.displayed_class_index = []

        # Page layout objects
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # Main page widgets
        self.calendar_widget = CalendarWidget(self)
        self.text_box = QPlainTextEdit(self)
        self.text_display = QPlainTextEdit(self)

        self.prompt_enter_btn = QPushButton('Enter text')
        self.prompt_enter_btn.clicked.connect(self.input_prompt)

        self.webview = QWebEngineView(self)
        self.webview.setFixedSize(1050, 600)

        self.recommendations_widget = QTableWidget(3, 50)
        # self.recommendations_widget.setGeometry(50, 200, self.calendar_widget.width(), self.calendar_widget.height())

        # Filtering objects
        self.text_filter = TextFilter()
        self.constraint_based_filter = ConstraintBasedFilter()

    def load_courses(self) -> None:
        """
        Loads the courses to be displayed in the course widgets list and assigns the ClassBox widget signals
        :return: None
        """
        self.displayed_class_index.sort(reverse=True, key=lambda x: x[0])
        for score, index in self.displayed_class_index[:20]:
            class_widget = ClassBox(self.class_names[index], self.course_dict[self.class_names[index]])
            class_widget.set_score(score)
            class_widget.buttonClicked.connect(self.onClassButtonClicked)
            class_widget.classClicked.connect(self.update_webview)
            self.course_widgets.append(class_widget)

    def load_course_dict(self) -> None:
        """
        Loads class details from the enriched_course_data.json generated from the web scrapping and enrichment scripts
        :return: None
        """
        self.course_dict = load_dict_from_json(os.path.join(os.pardir, "enriched_course_data.json"))
        self.class_names = list(self.course_dict.keys())

    def _hide_other_windows(self) -> None:
        """
        Hides the starting and filtering windows
        :return: None
        """
        if self.start_window.isVisible():
            self.start_window.hide()
        if self.start_window.filter_window.isVisible():
            self.start_window.filter_window.hide()

    def load_main_window(self) -> None:
        """
        Gets the results of the filtering window, creates the constraint based filtering
         and loads main page widgets
        :return: None
        """

        # gets constraints from filtering window
        constraints = self.start_window.filter_window.on_submit_button_clicked()
        self.constraint_based_filter.update_constraints(constraints)

        self.load_course_dict()
        self.constraint_filter_courses()
        self.load_courses()
        self.fill_recommended_classes()
        self.form_window_layout()

    def form_window_layout(self) -> None:
        """
        Forms the main page by adding the widgets to the layouts
        :return: None
        """

        # Prompt and LLM conversation
        self.text_box.setGeometry(50, 50, 100, 150)
        self.text_box.setPlaceholderText("Enter your prompt here:")

        self.text_display.setGeometry(50, 50, 100, 150)
        self.text_display.setPlainText("LLM conversation:\n")
        self.text_display.setReadOnly(True)
        self.text_display.setCenterOnScroll(True)

        # Bottom layout
        self.bottom_layout.addWidget(self.calendar_widget) # , alignment=Qt.AlignCenter)
        self.bottom_layout.addWidget(self.text_box) #, alignment=Qt.AlignCenter)
        self.bottom_layout.addWidget(self.text_display) #, alignment=Qt.AlignCenter)
        self.bottom_layout.addWidget(self.prompt_enter_btn) #, alignment=Qt.AlignCenter)

        # Top layout
        self.top_layout.addWidget(self.recommendations_widget) #, alignment=Qt.AlignCenter)
        self.top_layout.addWidget(self.webview) #, alignment=Qt.AlignCenter)

        # Main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        widget = QWidget(self)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.setVisible(True)
        self.showFullScreen()

        # Hide start and filter windows
        self._hide_other_windows()

    def onClassButtonClicked(self, class_box_widget: ClassBox) -> None:
        """
        Adds class to calendar view when the plus button is presses and removes it when minus button is clicked.
        It also changes between minus/ plus icons
        :param class_box_widget: class box widget for which the action happens
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

    def input_prompt(self) -> None:
        """
        Function that gets called when the LLM button is pressed. It displays the conversation of the user and the AI
        and calls the functions that update the scores of the classes and redraw the recommended class widget
        :return: None
        """
        self.text_display.appendPlainText('You said: \n' + self.text_box.toPlainText())
        self.text_display.appendPlainText('AI replied: \n' + '' + '\n')
        self.text_display.ensureCursorVisible()

        self.text_filter_courses(self.text_box.toPlainText())
        self.text_box.clear()
        self.load_courses()
        self.top_layout.removeWidget(self.recommendations_widget)
        self.recommendations_widget.deleteLater()
        self.recommendations_widget = QTableWidget(3, 50)
        self.top_layout.insertWidget(0, self.recommendations_widget)# , alignment=Qt.AlignHCenter)
        self.fill_recommended_classes()

    def constraint_filter_courses(self) -> None:
        """
        Filters the class indexes based on the constraints given in the filtering window
        :return: None
        """
        for index, class_name in enumerate(self.class_names):
            class_info = self.course_dict[class_name]
            if self.constraint_based_filter.filter_course(class_info):
                self.displayed_class_index.append([0, index])

    def text_filter_courses(self, text_prompt: str) -> None:
        """
        Filters the courses based on the text prompt of the user
        :param text_prompt: prompt inserted in AI-user chat
        :return: None
        """

        # Text Filtering if prompt inserted
        if text_prompt != '' and text_prompt != 'Enter your prompt here:':
            self.text_filter.generate_scores(text_prompt)
            for score, class_index in self.displayed_class_index:
                self.displayed_class_index[class_index][0] = self.text_filter.scores[class_index]

    def fill_recommended_classes(self) -> None:
        """
        Fills the recommendation widget with the Class box widgets
        :return: None
        """
        i = 0
        for col in range(self.recommendations_widget.columnCount()):
            for row in range(self.recommendations_widget.rowCount()):
                if i >= len(self.course_widgets):
                    break
                table_item = QTableWidgetItem()
                self.recommendations_widget.setCellWidget(row, col, self.course_widgets[i])
                self.recommendations_widget.setItem(row, col, table_item)
                self.recommendations_widget.setColumnWidth(col, 300)
                self.recommendations_widget.setRowHeight(row, 150)
                i += 1

        # Reset course widgets list
        self.course_widgets = []

    def update_webview(self, class_box_widget: ClassBox) -> None:
        """
        Loads course details website on the webview widget based on the course details dict href URL
        :param class_box_widget: Class box widget whose link we are getting
        :return: None
        """
        # Load a website
        self.webview.setUrl(QUrl(class_box_widget.class_details['href']))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
