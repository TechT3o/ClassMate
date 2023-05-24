from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class TimeSlotCalendar(QTableWidget):

    def __init__(self, widget_list):
        super().__init__(5, len(widget_list))
        self.setHorizontalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.setVerticalHeaderLabels(widget_list)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.populate_calendar(widget_list)

    def populate_calendar(self, widget_list):
        for col, widget in enumerate(widget_list):
            # time_periods = widget.get_time_periods()
            time_periods = widget
            for row, time_period in enumerate(time_periods):
                item = QTableWidgetItem(time_period)
                self.setItem(col, row, item)


class CustomWidget:
    def __init__(self, time_periods):
        self.time_periods = time_periods

    def get_time_periods(self):
        return self.time_periods


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.widget_list = [
        #     CustomWidget(["9:00 - 10:00", "13:00 - 14:00", "15:00 - 16:00"]),
        #     CustomWidget(["10:00 - 11:00", "14:00 - 15:00", "16:00 - 17:00"]),
        #     CustomWidget(["11:00 - 12:00", "15:00 - 16:00", "17:00 - 18:00"])
        # ]
        self.widget_list = ['1', '2', '3', '4', '5']
        self.calendar = TimeSlotCalendar(self.widget_list)
        self.setCentralWidget(self.calendar)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
