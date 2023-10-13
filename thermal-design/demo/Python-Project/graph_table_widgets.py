import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox

import DB
import Graph
from QTableWidgetExample import MainWindow
from Graph import GraphMainWindow


class LPHTableWindow(QWidget):

    def __init__(self):
        super(LPHTableWindow, self).__init__()
        self.cancelButton = QPushButton("Закрыть")
        self.cancelButton.setStyleSheet("background-color: #FFFF76;")

        """
            P_п = float(input('Введите давление греющего пара, МПа: '))
            t_п = float(input('Введите температуру греющего пара, °С: '))
            t_н = float(input('Введите температуру насыщения в подогревателе, °С: '))
            p_к = float(input('Введите давление нагреваемого конденсата, МПа: '))
            t_вх = float(input('Введите температуру конденсата на входе в подогреватель, °С: '))
            G_к = float(input('Введите расход конденсата через подогреватель, кг/с: '))
            etta_п = float(input('Введите коэффициент полезного действия подогреватель (КПД), в долях: '))
        """
        self.inp_table_labels = ['id', 'P_п, МПа', 't_п, °С', 't_н, °С', 'p_к, МПа', 't_вх, °С', 'G_к, кг/с', 'etta_п']

        """
            print(f'\nВыходные данные программы:\n\nРасход пара на подогреватель: {D_п} кг/с\n'
              f'Число параллеьных труб по ходу воды: {z_1}\n'
              f'Коэффициент теплоотдачи: {k} Вт/(м^2*K)')
        """
        self.out_table_labels = ['id', 'D_п, кг/с', 'z_1', 'k, Вт/(м^2*K)']

        self.table_window_inp = MainWindow(self.inp_table_labels)
        self.table_window_out = MainWindow(self.out_table_labels)
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.cancelButton)

        inp_label = QLabel("Таблица входных данных")
        inp_label.setFont(QFont("Times", 12, QFont.Bold))

        out_label = QLabel("Таблица выходных данных")
        out_label.setFont(QFont("Times", 12, QFont.Bold))

        table_int_box = QVBoxLayout()
        table_int_box.addWidget(inp_label)
        table_int_box.addWidget(self.table_window_inp)

        table_out_box = QVBoxLayout()
        table_out_box.addWidget(out_label)
        table_out_box.addWidget(self.table_window_out)

        tables_box = QHBoxLayout()
        tables_box.addLayout(table_int_box)
        tables_box.addLayout(table_out_box)

        vbox = QVBoxLayout()
        vbox.addLayout(tables_box)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.resize(1500, 700)
        self.setWindowTitle('Таблицы данных для подогревателя')
        self.cancelButton.clicked.connect(self.close)  ###


class GraphWindow(QWidget):

    def __init__(self, inp_data=None, name_inp_data=None, out_data=None, name_out_data=None, update_method=None):
        super(GraphWindow, self).__init__()

        self.cancelButton = QPushButton("Закрыть")
        self.cancelButton.setStyleSheet("background-color: #FFFF76;")

        self.updateButton = QPushButton("Обновить")
        self.updateButton.setStyleSheet("background-color: #FFFFFF;")
        self.updateButton.clicked.connect(update_method)

        self.inp_combo = QComboBox()
        self.inp_combo.setStyleSheet("background-color: #FFFFFF;")

        self.out_combo = QComboBox()
        self.out_combo.setStyleSheet("background-color: #FFFFFF;")

        if inp_data and out_data:
            inp_column_names = DB.get_column_names(inp_data)
            for i in range(1, len(inp_column_names)):
                self.inp_combo.addItem(DB.to_readable_data(inp_column_names[i])[0])

            out_column_names = DB.get_column_names(out_data)
            for i in range(1, len(out_column_names)):
                self.out_combo.addItem(DB.to_readable_data(out_column_names[i])[0])

            if name_inp_data and name_out_data:
                fig = Graph.create_graph(inp_data, name_inp_data, out_data, name_out_data)
            else:
                fig = Graph.create_graph(
                    inp_data,
                    DB.readable_to_data(self.inp_combo.currentText()),
                    out_data,
                    DB.readable_to_data(self.out_combo.currentText())
                )
        else:
            fig = None

        self.graph_window = GraphMainWindow(fig)
        # print(self.graph_window)
        self.init_ui()

    def init_ui(self):
        self.setup_graph()
        self.resize(1150, 550)
        self.setWindowTitle('График')
        self.cancelButton.clicked.connect(self.close)  ###
        # self.last_min.clicked.connect(self.get_last_min)  ###

    # def get_last_min(self):
    #     arr_data = DB.get_data_timediff(DB.LAST_MINUTE())
    #     fig = Graph.create_graph(arr_data)
    #     self.graph_window = GraphMainWindow(fig)
    #     # print(self.graph_window)
    #     self.setup_graph()

    def setup_graph(self):
        comment_in_label = QLabel("Входные данные:")
        comment_out_label = QLabel("Выходные данные:")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(comment_in_label)
        hbox.addWidget(self.inp_combo)
        hbox.addWidget(comment_out_label)
        hbox.addWidget(self.out_combo)
        hbox.addWidget(self.updateButton)
        hbox.addWidget(self.cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.graph_window)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


# app = QApplication(sys.argv)
# ex = Example()
# ex.show()
# sys.exit(app.exec())
