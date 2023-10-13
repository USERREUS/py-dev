import matplotlib.pyplot as plt
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox, \
    QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fC
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as nT
from matplotlib.dates import date2num

import DB
from calendar_widget import CalendarDT
from enclosed_dialog import CustomizeWindow


class MyMplCanvas(fC):
    def __init__(self, fig, parent=None):
        self.fig = fig
        fC.__init__(self, self.fig)
        fC.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        fC.updateGeometry(self)


class Graph(QWidget):
    def __init__(self, fig, parent=None):
        QWidget.__init__(self, parent)

        self.fig = fig
        self.canvas = MyMplCanvas(fig)
        self.toolbar = nT(self.canvas, self)
        self.resize(1150, 550)


def create_graph(inp_data_arr, name_inp_data, out_data_arr, name_out_data):
    inp_name = name_inp_data
    # len_inp = len(inp_data_arr)
    x_inp_list = DB.parse_data_for_name(inp_data_arr, 'date')
    y_inp_list = DB.parse_data_for_name(inp_data_arr, inp_name)

    out_name = name_out_data
    # len_out = len(out_data_arr)
    x_out_list = DB.parse_data_for_name(out_data_arr, 'calc_date')
    y_out_list = DB.parse_data_for_name(out_data_arr, out_name)

    graph = plt.figure()

    plt.subplot(1, 2, 1)
    plt.title('Входные данные')
    plt.xlabel('Дата загрузки')
    plt.ylabel(DB.to_readable_data(inp_name)[0] + DB.to_readable_data(inp_name)[1])
    dates = [date2num(t) for t in x_inp_list]
    plt.plot_date(dates, y_inp_list, 'bo-')

    plt.subplot(1, 2, 2)
    plt.title('Выходные данные')
    plt.xlabel('Дата расчета')
    plt.ylabel(DB.to_readable_data(out_name)[0] + DB.to_readable_data(out_name)[1])
    dates = [date2num(t) for t in x_out_list]
    plt.plot_date(dates, y_out_list, 'ro-')

    graph.autofmt_xdate()

    return graph


class GraphWindow(CustomizeWindow):

    def __init__(
            self,
            title,
            inp_data=None,
            name_inp_data=None,
            out_data=None,
            name_out_data=None,
            update_data_method=None,
            update_time_method=None,
            parent=None
    ):
        CustomizeWindow.__init__(
            self,
            title,
            600,
            1150,
            parent=parent
        )

        self.block_name = title
        # self.cancelButton = QPushButton("Закрыть")
        # self.cancelButton.setStyleSheet("background-color: #bd4f3a;")

        self.updateDataButton = QPushButton("Обновить")
        self.base_buttons.append(self.updateDataButton)
        # self.updateDataButton.setStyleSheet("background-color: #FFFFFF;")
        self.updateDataButton.clicked.connect(update_data_method)

        self.updateTimeButton = QPushButton("Обновить")
        self.base_buttons.append(self.updateTimeButton)
        # self.updateTimeButton.setStyleSheet("background-color: #FFFFFF;")
        self.updateTimeButton.clicked.connect(update_time_method)

        self.select_date_button = QPushButton("Выбрать дату")
        self.base_buttons.append(self.select_date_button)
        self.select_date_button.clicked.connect(self.open_calendar)

        self.calendar = CalendarDT(self)
        self.date = self.calendar.date

        self.date_label = QLabel("отобразить с:")
        self.labels = [self.date_label]

        self.date_line_edit = QLineEdit(self.date.toString("dd.MM.yy"))
        self.input_line_edits = [self.date_line_edit]
        self.date_line_edit.setReadOnly(True)

        self.inp_combo = QComboBox()
        self.inp_combo.setMaxVisibleItems(5)
        self.inp_combo.setMinimumContentsLength(10)
        # self.inp_combo.setStyleSheet("background-color: #FFFFFF;")

        self.out_combo = QComboBox()
        self.out_combo.setMaxVisibleItems(5)
        self.out_combo.setMinimumContentsLength(10)
        # self.out_combo.setStyleSheet("background-color: #FFFFFF;")

        if inp_data and out_data:
            inp_column_names = DB.get_column_names(inp_data)
            inp_column_names.remove("row_id")
            inp_column_names.remove("date")
            for i in range(len(inp_column_names)):
                self.inp_combo.addItem(DB.to_readable_data(inp_column_names[i])[0])

            out_column_names = DB.get_column_names(out_data)
            out_column_names.remove("row_id")
            out_column_names.remove("calc_date")
            out_column_names.remove("recording_date")
            for i in range(len(out_column_names)):
                self.out_combo.addItem(DB.to_readable_data(out_column_names[i])[0])

            if name_inp_data and name_out_data:
                index = self.inp_combo.findText(DB.to_readable_data(name_inp_data)[0], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.inp_combo.setCurrentIndex(index)
                index = self.out_combo.findText(DB.to_readable_data(name_out_data)[0], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.out_combo.setCurrentIndex(index)
                fig = create_graph(
                    inp_data,
                    name_inp_data,
                    out_data,
                    name_out_data
                )
            else:
                fig = create_graph(
                    inp_data,
                    DB.readable_to_data(self.inp_combo.currentText()),
                    out_data,
                    DB.readable_to_data(self.out_combo.currentText())
                )
        else:
            fig = None

        self.graph_window = Graph(fig)

        comment_in_label = QLabel("Входные данные:")
        comment_out_label = QLabel("Выходные данные:")

        self.labels.append(comment_in_label)
        self.labels.append(comment_out_label)

        hbox = QHBoxLayout()

        hbox.addWidget(self.date_label)
        hbox.addWidget(self.date_line_edit)
        hbox.addWidget(self.select_date_button)
        hbox.addWidget(self.updateTimeButton)

        hbox.addWidget(comment_in_label)
        hbox.addWidget(self.inp_combo)
        hbox.addWidget(comment_out_label)
        hbox.addWidget(self.out_combo)
        hbox.addWidget(self.updateDataButton)
        hbox.addStretch(1)

        self.common_actions.clear()

        icon_close = QIcon("images/close.xpm")
        self.common_actions.addAction("X", self.close)
        self.common_actions.actions()[0].setIcon(icon_close)

        icon_full = QIcon("images/full.xpm")
        self.common_actions.addAction("[< >]", self.full_screen)
        self.common_actions.actions()[1].setIcon(icon_full)

        icon_hide = QIcon("images/hide.xpm")
        self.common_actions.addAction("__", self.showMinimized)
        self.common_actions.actions()[2].setIcon(icon_hide)

        vbox = QVBoxLayout(self.bottom)
        vbox.addLayout(hbox)

        sub_vbox = QVBoxLayout()
        sub_vbox.addWidget(self.graph_window)
        sub_vbox.addWidget(self.graph_window.canvas)
        sub_vbox.addWidget(self.graph_window.toolbar)

        vbox.addLayout(sub_vbox)
        vbox.setSpacing(20)
        vbox.setContentsMargins(20, 10, 20, 10)

        self.apply_style()

    def open_calendar(self):
        self.calendar.show()

    def full_screen(self):
        for action in self.common_actions.actions():
            if action.text() == "[< >]":
                action.setText("[> <]")
                action.setIcon(QIcon("images/minimize.xpm"))
                self.showFullScreen()
                self.label_title.setFixedSize(self.width(), 30)
                self.lefttop.setFixedSize(int(self.width() / 2), 30)
                self.righttop.setFixedSize(int(self.width() / 2), 30)
                self.bottom.setFixedSize(self.width(), self.height() - 30)
                self.common_actions.setFixedSize(int(self.width() / 2), 30)
            elif action.text() == "[> <]":
                action.setText("[< >]")
                action.setIcon(QIcon("images/full.xpm"))
                self.showNormal()
                self.label_title.setFixedSize(self.width(), 30)
                self.lefttop.setFixedSize(int(self.width() / 2), 30)
                self.righttop.setFixedSize(int(self.width() / 2), 30)
                self.bottom.setFixedSize(self.width(), self.height() - 30)
                self.common_actions.setFixedSize(int(self.width() / 2), 30)


# def example_create_graph():
#     width = 0.4
#     x_list = list(range(0, 5))
#     y1_list = [22, 17, 81, 41, 25]
#     y2_list = [62, 37, 39, 36, 49]
#     x_indexes = np.arange(len(x_list))
#
#     graph = plt.figure()
#     plt.subplot(1, 2, 1)
#     plt.title('Salary Graph')
#     plt.xticks(x_list, ['A', 'B', 'C', 'D', 'E'])
#     plt.xlabel('days')
#     plt.ylabel('salary, $')
#     plt.plot(x_list, y1_list, label="Mark", marker="o")
#     plt.plot(x_list, y2_list, label="Steven", marker="^")
#     plt.legend()
#
#     plt.subplot(1, 2, 2)
#     plt.title('Salary Bars')
#     plt.xticks(x_indexes, ['A', 'B', 'C', 'D', 'E'])
#     plt.xlabel('days')
#     plt.ylabel('salary, $')
#     plt.bar(x_indexes - (width/2), y1_list, label="Mark", width=width)
#     plt.bar(x_indexes + (width/2), y2_list, label="Steven", width=width)
#     plt.legend()
#
#     return graph
