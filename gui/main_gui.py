from gui import ClassBox
from gui import CalendarWidget
from gui import StartWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton, QTableWidget, QLabel, QPlainTextEdit,\
    QStatusBar, QWidget, QAction, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
from text_filter import TextFilter
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
        self.webview_layout = QVBoxLayout()
        self.recommendation_layout = QVBoxLayout()

        # Main page widgets
        self.calendar_widget = CalendarWidget(self)
        self.text_box = QPlainTextEdit(self)
        self.text_display = QPlainTextEdit(self)

        self.prompt_enter_btn = QPushButton('Submit')
        self.prompt_enter_btn.setStatusTip("Click to re-score courses based on prompt")
        self.prompt_enter_btn.clicked.connect(self.input_prompt)

        self.webview = QWebEngineView(self)
        self.webview.setFixedSize(1050, 600)

        self.recommendations_widget = QTableWidget(3, 50)
        # self.recommendations_widget.setGeometry(50, 200, self.calendar_widget.width(), self.calendar_widget.height())

        # Filtering objects
        self.text_filter = TextFilter()
        self.constraint_based_filter = ConstraintBasedFilter()

        self.setStatusBar(QStatusBar(self))
        self.form_window_layout()

    def load_courses(self) -> None:
        """
        Loads the courses to be displayed in the course widgets list and assigns the ClassBox widget signals
        :return: None
        """
        self.displayed_class_index.sort(reverse=True, key=lambda x: x[0])
        for score, index in self.displayed_class_index[:20]:
            class_widget = ClassBox(self.class_names[index], self.course_dict[self.class_names[index]])
            class_widget.set_score(score)
            class_widget.btn.setStatusTip("Click to add/remove class from calendar")
            class_widget.lbl.setStatusTip("Click to see class webpage")
            class_widget.buttonClicked.connect(self.onClassButtonClicked)
            class_widget.classClicked.connect(self.update_webview)
            self.course_widgets.append(class_widget)

    def load_course_dict(self) -> None:
        """
        Loads class details from the enriched_course_data.json generated from the web scrapping and enrichment scripts
        :return: None
        """
        self.course_dict = load_dict_from_json("enriched_course_data.json")
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

    def _show_other_windows(self) -> None:
        """
        Shows the starting and filtering windows
        :return: None
        """
        if not self.start_window.filter_window.isVisible():
            self.start_window.filter_window.show()

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
        # self.form_window_layout()

        self.setVisible(True)
        self.showFullScreen()

        self.calendar_widget.clear()
        self.calendar_widget.draw_empty_table()
        self.calendar_widget.courses = []

        # Hide start and filter windows
        self._hide_other_windows()

    def form_window_layout(self) -> None:
        """
        Forms the main page by adding the widgets to the layouts
        :return: None
        """

        # Prompt and LLM conversation
        self.text_box.setGeometry(25, 25, 50, 150)
        self.text_box.setPlaceholderText("Search for course here:")
        self.text_box.setStatusTip("Type what kind of course you would like")

        self.text_display.setGeometry(50, 50, 100, 150)
        self.text_display.setPlainText("Previous search history:\n")
        self.text_display.setReadOnly(True)
        self.text_display.setCenterOnScroll(True)

        llm_layout = QVBoxLayout()
        llm_layout.addWidget(self.text_display)  # , alignment=Qt.AlignCenter)
        llm_layout.addWidget(self.text_box)  # , alignment=Qt.AlignCenter)
        llm_layout.addWidget(self.prompt_enter_btn)  # , alignment=Qt.AlignCenter)

        # Bottom layout
        self.bottom_layout.addWidget(self.calendar_widget) # , alignment=Qt.AlignCenter)
        # self.bottom_layout.addWidget(self.text_box) #, alignment=Qt.AlignCenter)
        # self.bottom_layout.addWidget(self.text_display) #, alignment=Qt.AlignCenter)
        # self.bottom_layout.addWidget(self.prompt_enter_btn) #, alignment=Qt.AlignCenter)
        self.bottom_layout.addLayout(llm_layout)

        # Top layout

        self.recommendation_layout.addWidget(QLabel('Recommendation table scroll to see sorted classes'))
        self.recommendation_layout.addWidget(self.recommendations_widget)
        self.top_layout.addLayout(self.recommendation_layout) #, alignment=Qt.AlignCenter)

        self.webview_layout.addWidget(QLabel('Webview, click on a class name to load class webpage'))
        self.webview_layout.addWidget(self.webview)
        self.top_layout.addLayout(self.webview_layout) #, alignment=Qt.AlignCenter)

        # Main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        widget = QWidget(self)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

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
        quit_menu = menubar.addMenu("&Quit")
        back_menu = menubar.addMenu("&Back")
        help_menu = menubar.addMenu("&Help")

        # Create a "Quit" action
        quit_action = QAction("Quit Classmate", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.setStatusTip("Click to quit Classmate.")
        quit_action.triggered.connect(QApplication.quit)

        # Create a "Back" action
        back_action = QAction("Go back to filtering", self)
        # back_action.setShortcut('Ctrl')
        back_action.triggered.connect(self._show_other_windows)
        back_action.setStatusTip("Click to go back to filtering window.")

        # Create a "Quit" action
        help_action = QAction("Help", self)
        # help_action.setShortcut(QKeySequence.Quit)
        help_action.triggered.connect(self.help_dialog)
        help_action.setStatusTip("Click to see Classmate tutorial.")

        # Add the "Quit" action to the "File" menu
        quit_menu.addAction(quit_action)
        back_menu.addAction(back_action)
        help_menu.addAction(help_action)

    def input_prompt(self) -> None:
        """
        Function that gets called when the LLM button is pressed. It displays the conversation of the user and the AI
        and calls the functions that update the scores of the classes and redraw the recommended class widget
        :return: None
        """
        self.text_display.appendPlainText('You searched for: \n' + self.text_box.toPlainText())
        # self.text_display.appendPlainText('AI replied: \n' + '' + '\n')
        self.text_display.ensureCursorVisible()

        self.text_filter_courses(self.text_box.toPlainText())
        self.text_box.clear()
        self.load_courses()
        self.top_layout.removeWidget(self.recommendations_widget)
        self.recommendations_widget.deleteLater()
        self.recommendations_widget = QTableWidget(3, 50)
        self.recommendation_layout.insertWidget(1, self.recommendations_widget) # , alignment=Qt.AlignHCenter)
        self.calendar_widget.clear()
        self.calendar_widget.draw_empty_table()
        self.calendar_widget.courses = []

        self.fill_recommended_classes()

    def constraint_filter_courses(self) -> None:
        """
        Filters the class indexes based on the constraints given in the filtering window
        :return: None
        """
        self.displayed_class_index = []
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

                if [score, class_index] in self.displayed_class_index:
                    self.displayed_class_index[self.displayed_class_index.index([score, class_index])][0]\
                        = self.text_filter.scores[class_index]

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

    def help_dialog(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Tutorial")
        text = """
        In the upper left corner, a display of the classes that best fit you depending on the filters used or your
        input in the text prompt. For each class, the + button allows you to add the class in the plan in the calendar
        in the bottom right corner. Similarly, once the class is added, the - button allows you to remove it.
        Clicking on the class name opens the class details in the top right corner.

        In the bottom left corner, the calendar with the added classes is displayed.

        In the bottom right corner, a text prompt allows you to input your preferences as a text input and our AI agent
        will find the classes that best suit you based on your preferences. 
        """
        dlg.setText(text)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
