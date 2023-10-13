import datetime
import math
import sys
import DB

from queue import Queue
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QMessageBox, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import date2num
from matplotlib.figure import Figure


class Table(QTableWidget):
    """
    Класс табличного отображения статистической информации
    """
    def __init__(self, q: Queue) -> None:
        """
        Инициализация
        :param q: очередь записей
        """
        super().__init__()
        self.q = q

    def fill(self) -> None:
        """
        Создания таблицы с заполнением
        """
        warning_msg: str = ""

        data_rows: [dict] = list(self.q.queue)
        data: [object] = []
        table_labels: [str] = []
        # заполнение списка данных и подписей
        if data_rows:
            for row in data_rows:
                temp = []
                for item in row:
                    temp.append(row[item])
                data.append(temp)
            for item in data_rows[0]:
                table_labels.append(item)

        if not table_labels:
            warning_msg += "Таблица входных данных не заполнена.\n"

        if warning_msg != "":
            QMessageBox.warning(
                self,
                "Ошибка открытия таблиц",
                warning_msg,
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok
            )
            return

        self.setMinimumWidth(500)

        self.setColumnCount(len(table_labels))
        self.setRowCount(len(data))

        width = int(self.width() / self.columnCount())
        for x in range(0, self.columnCount()):
            self.setColumnWidth(x, width)

        self.setHorizontalHeaderLabels(table_labels)
        self.setSortingEnabled(False)

        self.ref_index = table_labels.index('y')
        self.real_index = table_labels.index('y_real')

        self.load_data_table(data)

    def load_data_table(self, data: [object]) -> None:
        """
        Заполнение ячеек таблицы
        :param data: список данных для заполнения
        """
        for row in range(len(data)):
            for column in range(self.columnCount()):
                item = QTableWidgetItem(str(data[row][column]))
                if column == self.real_index:
                    if math.fabs(data[row][self.ref_index] - data[row][self.real_index]) > 1:
                        item.setBackground(QtCore.Qt.GlobalColor.red)
                self.setItem(row, column, item)


class PlotWidget(QWidget):
    """
    Класс для отображения графической информации
    """
    def __init__(self, q: Queue) -> None:
        """
        Инициализация
        :param q: очередь записей данных
        """
        super().__init__()  # Инициализируем экземпляр
        self.q = q
        self.init_ui()  # Строим интерфейс

    def init_ui(self) -> None:
        """
        Инициализация параметров пользовательского интерфейса
        """
        self.mainLayout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)

        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

    def plot(self) -> None:
        """
        Построение графика
        """
        data_rows = list(self.q.queue)
        x = []
        y = []
        y_real = []
        date = []
        for row in data_rows:
            x.append(row['x'])
            y.append(row['y'])
            y_real.append(row['y_real'])
            date.append(datetime.datetime.fromisoformat(row['datetime']))

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot_date([date2num(t) for t in date], y_real, '-b', label="y_real")
        ax.plot_date([date2num(t) for t in date], y, '-r', label="y")
        ax.legend(loc='upper right')
        self.figure.autofmt_xdate()
        self.canvas.draw()


class InfoWindow(QWidget):
    """
    Класс окна отображения статистической информации
    """
    def __init__(self, queue: Queue) -> None:
        """
        Инициализация
        :param queue: очередь записей данных
        """
        super().__init__()
        self.l = QVBoxLayout(self)
        self.h = QHBoxLayout(self)
        self.setWindowTitle("Статистическая информация")
        self.plotWidget = PlotWidget(queue)
        self.tableWidget = Table(queue)

        self.update_button = QPushButton('Обновить')

        self.update_button.setStyleSheet('font-size: 12pt; font-weight: 530;')

        self.h2 = QHBoxLayout(self)
        self.h2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.h2.setContentsMargins(10, 10, 10, 10)
        self.h2.setSpacing(20)
        self.h2.addWidget(self.update_button)
        self.l.addLayout(self.h2)

        self.h.addWidget(self.plotWidget)
        self.h.addWidget(self.tableWidget)
        self.l.addLayout(self.h)

        self.update_button.clicked.connect(self.on_update)

    def on_update(self) -> None:
        """
        Обработка события обновления
        """
        self.plotWidget.plot()
        self.tableWidget.fill()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    msg, json_data = DB.get_json_data('output')
    q = Queue()
    for i in range(30):
        q.put_nowait(json_data['data'][i])
    info = InfoWindow(q)
    info.show()
    sys.exit(app.exec())
    # view.show()
    # sys.exit(app.exec())