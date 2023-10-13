import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fC
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as nT

import DB


class MyMplCanvas(fC):
    def __init__(self, fig, parent=None):
        self.fig = fig
        fC.__init__(self, self.fig)
        fC.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        fC.updateGeometry(self)


class Ui_QGraphWidgetWindow(object):
    def setup_ui(self, MainWindow, fig):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 550)

        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.resize(1100, 500)
        vbox = QVBoxLayout(self.centralWidget)

        self.fig = fig
        self.canvas = MyMplCanvas(self.fig)
        vbox.addWidget(self.canvas)
        self.toolbar = nT(self.canvas, self)
        vbox.addWidget(self.toolbar)


class GraphMainWindow(QMainWindow, Ui_QGraphWidgetWindow):
    def __init__(self, fig, parent=None):
        QMainWindow.__init__(self)
        self.setup_ui(self, fig)


def create_graph(inp_data_arr, name_inp_data, out_data_arr, name_out_data):
    inp_name = name_inp_data
    len_inp = len(inp_data_arr)
    x_inp_list = DB.parse_data_for_name(inp_data_arr, 'id')
    y_inp_list = DB.parse_data_for_name(inp_data_arr, inp_name)

    out_name = name_out_data
    len_out = len(out_data_arr)
    x_out_list = DB.parse_data_for_name(out_data_arr, 'id')
    y_out_list = DB.parse_data_for_name(out_data_arr, out_name)

    graph = plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('Входные данные')
    plt.xlabel('id')
    plt.ylabel(DB.to_readable_data(inp_name)[1])
    plt.plot(x_inp_list, y_inp_list, label=DB.to_readable_data(inp_name)[0], marker="o")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Выходные данные')
    plt.xlabel('id')
    plt.ylabel(DB.to_readable_data(out_name)[1])
    plt.plot(x_out_list, y_out_list, label=DB.to_readable_data(out_name)[0], marker="x")
    plt.legend()

    return graph


def example_create_graph():
    width = 0.4
    x_list = list(range(0, 5))
    y1_list = [22, 17, 81, 41, 25]
    y2_list = [62, 37, 39, 36, 49]
    x_indexes = np.arange(len(x_list))

    graph = plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('Salary Graph')
    plt.xticks(x_list, ['A', 'B', 'C', 'D', 'E'])
    plt.xlabel('days')
    plt.ylabel('salary, $')
    plt.plot(x_list, y1_list, label="Mark", marker="o")
    plt.plot(x_list, y2_list, label="Steven", marker="^")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Salary Bars')
    plt.xticks(x_indexes, ['A', 'B', 'C', 'D', 'E'])
    plt.xlabel('days')
    plt.ylabel('salary, $')
    plt.bar(x_indexes - (width/2), y1_list, label="Mark", width=width)
    plt.bar(x_indexes + (width/2), y2_list, label="Steven", width=width)
    plt.legend()

    return graph


# app = QApplication(sys.argv)
# ex = MainWindow()
# ex.show()
# sys.exit(app.exec())
