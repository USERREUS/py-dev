import datetime
import sys

from PySide6.QtGui import QFont, QIcon, QAction

import DB
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QMainWindow, QTableWidgetItem, \
    QMessageBox, QLabel, QHBoxLayout, QPushButton

from enclosed_dialog import CustomizeWindow


class Table(QTableWidget):
    def __init__(self, column_labels, parent=None):
        QTableWidget.__init__(self, parent)
        self.resize(700, 600)

        self.setColumnCount(len(column_labels))
        self.setRowCount(100)

        for x in range(0, self.columnCount()):
            self.setColumnWidth(x, 100)

        self.column_labels = DB.readable_labels(column_labels)
        self.setHorizontalHeaderLabels(self.column_labels)
        self.setSortingEnabled(True)
        self.verticalHeader().hide()


def prepare_one_column_data(column_name, table):
    column_container = []
    for column in range(0, table.columnCount()):
        if table.horizontalHeaderItem(column).text() == column_name:
            try:
                for row in range(0, table.rowCount()):
                    column_container.append(table.item(row, column).text())
                return column_container
            except:
                return column_container


def prepare_one_row_data(row_name, table):
    row_container = []
    for row in range(0, table.rowCount()):
        if table.verticalHeaderItem(row).text() == row_name:
            try:
                for column in range(0, table.columnCount()):
                    row_container.append(table.item(row, column).text())
                return row_container
            except:
                return row_container


def load_data_inp_table(data_table, table):
    if data_table:
        data_row_count = len(data_table)
        table_row_count = table.rowCount()
        table_column_count = table.columnCount()
        diff = 0
        if data_row_count > table_row_count:
            diff = data_row_count - table_row_count
            for row in range(0, table_row_count):
                for column in range(0, table_column_count):
                    item = QTableWidgetItem(str(data_table[row+diff][column]))
                    table.setItem(row, column, item)
        else:
            for row in range(0, data_row_count):
                for column in range(0, table_column_count):
                    item = QTableWidgetItem(str(data_table[row][column]))
                    table.setItem(row, column, item)


def load_data_out_table(data_table, table):
    # try:
    if data_table:
        data_row_count = len(data_table)
        data_column_count = len(data_table[0])
        # print(data_column_count)
        table_row_count = table.rowCount()
        table_column_count = table.columnCount()
        # print(table_column_count)
        diff = 0
        if data_row_count > table_row_count:
            diff = data_row_count - table_row_count
            for row in range(0, table_row_count):
                for column in range(0, table_column_count):
                    if data_column_count != table_column_count:
                        item = QTableWidgetItem(str(data_table[row][column + 1]))
                        if column == 0:
                            if data_table[row][0] == 0:
                                item.setBackground(QtGui.QColor(5, 176, 80))
                            if data_table[row][0] == 1:
                                item.setBackground(QtGui.QColor(148, 202, 82))
                            if data_table[row][0] == 2:
                                item.setBackground(QtGui.QColor(246, 235, 19))
                            if data_table[row][0] == 3:
                                item.setBackground(QtGui.QColor(250, 193, 18))
                            if data_table[row][0] == 4:
                                item.setBackground(QtGui.QColor(235, 35, 37))
                    else:
                        item = QTableWidgetItem(str(data_table[row][column]))
                    table.setItem(row, column, item)
        else:
            for row in range(0, data_row_count):
                for column in range(0, table_column_count):
                    if data_column_count != table_column_count:
                        item = QTableWidgetItem(str(data_table[row][column + 1]))
                        if column == 0:
                            if data_table[row][0] == 0:
                                item.setBackground(QtGui.QColor(5, 176, 80))
                            if data_table[row][0] == 1:
                                item.setBackground(QtGui.QColor(148, 202, 82))
                            if data_table[row][0] == 2:
                                item.setBackground(QtGui.QColor(246, 235, 19))
                            if data_table[row][0] == 3:
                                item.setBackground(QtGui.QColor(250, 193, 18))
                            if data_table[row][0] == 4:
                                item.setBackground(QtGui.QColor(235, 35, 37))
                    else:
                        item = QTableWidgetItem(str(data_table[row][column]))
                    table.setItem(row, column, item)

    # except Exception as exc:
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Ошибка работы с таблицей!")
    #     msg.setText(exc.__str__())
    #     msg.setIcon(QMessageBox.Critical)
    #
    #     msg.exec()
    # finally:
    #     pass


class TableWindow(CustomizeWindow):

    def __init__(self, height, width, data_inp_name, data_out_name, block_name, cmp_out_name=None, parent=None):
        CustomizeWindow.__init__(self, block_name, height, width, parent=parent)

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

        self.data_inp_name = data_inp_name
        self.data_out_name = data_out_name
        self.cmp_out_name = cmp_out_name
        self.block_name = block_name

        warning_msg = ""
        inp_table_labels = DB.get_column_names(
            DB.get_data(self.data_inp_name)
        )

        if not inp_table_labels:
            warning_msg += "Таблица входных данных не заполнена.\n"

        out_table_labels = DB.get_column_names(
            DB.get_data(self.data_out_name)
        )

        if not out_table_labels:
            warning_msg += "Таблица выходных данных не заполнена."

        if warning_msg != "":
            QMessageBox.warning(
                self,
                "Ошибка открытия таблиц",
                warning_msg,
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok
            )
            return

        # id в конец
        id_column = inp_table_labels.pop(0)
        inp_table_labels.append(id_column)

        id_column = out_table_labels.pop(0)
        out_table_labels.append(id_column)

        cmp_out_labels = []
        if cmp_out_name:
            cmp_out_labels = DB.get_column_names(
                DB.get_data(self.cmp_out_name)
            )
            cmp_out_labels.remove("row_id")
            cmp_out_labels.remove("calc_date")
            cmp_out_labels.remove("recording_date")
            cmp_out_labels.remove("state")

        out_table_labels = cmp_out_labels + out_table_labels

        # обработка заголовков
        self.process_headers()

        self.table_window_inp = Table(inp_table_labels)
        self.table_window_out = Table(out_table_labels)
        self.init_ui()

    def init_ui(self):

        inp_label = QLabel("Таблица входных данных")
        out_label = QLabel("Таблица выходных данных")
        self.comment_labels = [inp_label, out_label]

        table_inp_box = QVBoxLayout()
        table_inp_box.addWidget(inp_label)
        table_inp_box.addWidget(self.table_window_inp)

        table_out_box = QVBoxLayout()
        table_out_box.addWidget(out_label)
        table_out_box.addWidget(self.table_window_out)

        tables_box = QHBoxLayout(self.bottom)
        tables_box.addLayout(table_inp_box)
        tables_box.addLayout(table_out_box)
        tables_box.setSpacing(20)
        tables_box.setContentsMargins(20, 10, 20, 10)

        self.table_window_inp.setStyleSheet("""
            border: 2px solid #ccc;
        """)

        self.table_window_out.setStyleSheet("""
            border: 2px solid #ccc;
        """)

        self.apply_style()

    def process_headers(self):
        pass

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
