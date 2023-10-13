import datetime
import sys
import DB
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QMainWindow, QTableWidgetItem, \
    QMessageBox


class Ui_QTableWidgetWindow(object):
    def setup_ui(self, MainWindow, column_labels):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 650)

        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.resize(700, 600)
        vbox = QVBoxLayout(self.centralWidget)

        self.TableWidget = QTableWidget()
        vbox.addWidget(self.TableWidget)
        self.TableWidget.setColumnCount(len(column_labels))
        self.TableWidget.setRowCount(100)

        for x in range(0, self.TableWidget.columnCount()):
            self.TableWidget.setColumnWidth(x, 200)

        # a = QTableWidgetItem(str(100))
        # c = QTableWidgetItem('FFF')

        # self.TableWidget.setItem(0, 0, a)
        # self.TableWidget.setItem(2, 2, c)

        # DB.create_table()
        # DB.add_value("T", "F", datetime.datetime.now(), 5, 25)
        # DB.add_value("T", "F", datetime.datetime.now(), 6, 36)
        # data_table = DB.parse_data(DB.get_data())
        # load_data_table(data_table, self.TableWidget)

        self.column_label = column_labels
        self.TableWidget.setHorizontalHeaderLabels(self.column_label)
        self.TableWidget.setSortingEnabled(True)

        # self.TableWidget.clear()
        # self.TableWidget.clearContents()

        # print(prepare_one_column_data('A', self.TableWidget))
        # print(prepare_one_row_data('1', self.TableWidget))


class MainWindow(QMainWindow, Ui_QTableWidgetWindow):
    def __init__(self, clolumn_labels, parent=None):
        QMainWindow.__init__(self)
        self.setup_ui(self, clolumn_labels)


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


def load_data_table(data_table, table):
    # try:
    if data_table:
        data_row_count = len(data_table)
        # print(data_row_count)
        # data_column_count = len(data_table[0])
        table_row_count = table.rowCount()
        # print(table_row_count)
        table_column_count = table.columnCount()
        diff = 0
        if data_row_count > table_row_count:
            diff = data_row_count - table_row_count
            # print(diff)
            for row in range(0, table_row_count):
                for column in range(0, table_column_count):
                    item = QTableWidgetItem(str(data_table[row+diff][column]))
                    table.setItem(row, column, item)
        else:
            for row in range(0, data_row_count):
                for column in range(0, table_column_count):
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


# app = QApplication(sys.argv)
# ex = MainWindow()
# ex.show()
# sys.exit(app.exec())
