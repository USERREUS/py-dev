"""
Тут описывается все, что связано с передвижением объектов внутри области передвижения
"""
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter, QBrush, QPen
from PySide6.QtWidgets import QWidget


# Окно для размещения и перетаксивания объектов
class MovingArea(QWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.buttons = []  # массив всех кнопок на рабочей области
        self.pair_buttons = []
        self.logic_connected_pair = []  # FIX

    # Событие по захвату объекта - пока ничего не делает
    def dragEnterEvent(self, event):
        event.accept()

    # Событие по отпусканию кнопки после переноса - изменяет координаты центра объекта
    def dropEvent(self, event):
        for button in self.buttons:
            if button.isDown():
                move_x = event.position().x() - button.width() / 2
                move_y = event.position().y() - button.height() / 2

                if event.position().x() + button.width() / 2 > self.width():
                    move_x = self.width() - 2 * button.width() / 2

                if event.position().y() + button.height() / 2 > self.height():
                    move_y = self.height() - 2 * button.height() / 2

                if event.position().x() - button.width() / 2 < 0:
                    move_x = 0

                if event.position().y() - button.height() / 2 < 0:
                    move_y = 0

                button.move(move_x, move_y)

                button.set_coords(int(move_x), int(move_y))
                qwe = button.get_coords()
                print(f'Button position after moving: {qwe[0]}, {qwe[1]}')

        self.printing()
        event.accept()

    # Событие рисования связей
    def paintEvent(self, event):
        if len(self.logic_connected_pair) != 0:
            for pair in self.logic_connected_pair:
                if pair.is_correct():
                    qp = QPainter()
                    qp.begin(self)
                    pt_from = QPoint(pair.line_start_x, pair.line_start_y)

                    x, y = pair.get_point_coordinates()
                    pr_to = QPoint(x, y)

                    draw_lines(qp, pt_from, pr_to)

                    point_x, point_y = pair.get_point_coordinates()

                    qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

                    if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
                        qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))

                    else:
                        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

                    qp.drawEllipse(int(point_x) - 5, int(point_y) - 5, 10, 10)
                    qp.end()

    # Метод рисования с пересчетом координат
    def printing(self):
        if len(self.logic_connected_pair) != 0:

            for pair in self.logic_connected_pair:

                if pair.is_correct():

                    pair.recalculate_coordinates()

        self.update()

    # Метод проверки на наличие кнопки в массиве пар
    def is_in_logic_cp(self, button):
        for pair in self.logic_connected_pair:
            if pair.btnl == button or pair.btnr == button:
                if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
                    return True

        return False

    # Метод удаления всех связей с данной кнопкой
    def destroy_connection(self, button):
        # print("START Method: destroy_connection_____________________")
        # FIX !!! переделать цикл (хотя лучше не трогать пока работает)
        j = 0
        for i in range(len(self.logic_connected_pair)):
            if self.logic_connected_pair[i - j].btnl == button or self.logic_connected_pair[i - j].btnr == button:
                self.logic_connected_pair.remove(self.logic_connected_pair[i - j])
                j = j + 1
        # print("END Method: destroy_connection_____________________")


# Метод рисования линий
def draw_lines(qp, pt_form, pt_to):
    pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
    pen.setStyle(Qt.DotLine)
    qp.setPen(pen)
    qp.drawLine(pt_form.x(), pt_form.y(), pt_to.x(), pt_to.y())


# Класс логической пары кнопок
class ButtonsPair:

    def __init__(self):
        self.btnl = None
        self.btnr = None

        self.line_start_x = 0
        self.line_start_y = 0

        self.line_end_x = 0
        self.line_end_y = 0

        self.point_x = 0
        self.point_y = 0

    # Установить левую кнопку в паре
    def set_btnl(self, btnl):
        self.btnl = btnl

    # Установить правую кнопку в паре
    def set_btnr(self, btnr):
        self.btnr = btnr
        self.btnr.sender = self.btnl

        self.recalculate_coordinates()

        self.btnr.moving_area.update()

    # Пересчитать координаты
    def recalculate_coordinates(self):
        self.line_start_x = self.btnl.x() + self.btnl.width() / 2
        self.line_start_y = self.btnl.y() + self.btnl.height() / 2

        self.line_end_x = self.btnr.x() + self.btnr.width() / 2
        self.line_end_y = self.btnr.y() + self.btnr.height() / 2

    # Получить координаты точки
    def get_point_coordinates(self):
        center_btnl_x = self.line_start_x
        center_btnl_y = self.line_start_y

        center_btnr_x = self.line_end_x
        center_btnr_y = self.line_end_y

        if center_btnl_y > center_btnr_y + self.btnl.height() / 2:
            return center_btnr_x, center_btnr_y + (self.btnl.height() / 2) + 5

        elif center_btnl_y < center_btnr_y - self.btnl.height() / 2 - 5:
            return center_btnr_x, center_btnr_y - (self.btnl.height() / 2) - 5

        elif center_btnl_x < center_btnr_x:
            return center_btnr_x - (self.btnr.width() / 2) - 5, center_btnr_y

        else:
            return center_btnr_x + (self.btnr.width() / 2) + 5, center_btnr_y

    # Проверка на коррекность пары
    def is_correct(self):
        return not (self.btnl is None or self.btnr is None)
