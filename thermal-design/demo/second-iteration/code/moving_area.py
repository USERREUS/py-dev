"""
Тут описывается все, что связано с передвижением объектов внутри области передвижения
"""
import math
import random
import time

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter, QBrush, QPen, QColor, QPolygon
from PySide6.QtWidgets import QWidget


# Окно для размещения и перетаксивания объектов
class MovingArea(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.buttons = []  # массив всех кнопок на рабочей области
        self.pair_buttons = []
        self.logic_connected_pair = []  # FIX
        self.resize(1080, 550)
        self.hor_parts = -1
        self.vert_parts = -1
        self.partition = SpaceAccess(self.width(), self.height(), self.hor_parts, self.vert_parts)
        # self.partition.show_partition()
        # self.partition.show_busy()

    # Добавление кнопки на поле
    def add_btn(self, btn):
        if self.partition.place_button_first(btn)[0] >= 0:
            self.buttons.append(btn)
            btn.show()

    def resizing(self):
        # print("resizing", self.width(), self.height())
        self.partition = SpaceAccess(self.width(), self.height(), self.hor_parts, self.vert_parts)
        if len(self.buttons):
            for button in self.buttons:
                self.partition.place_button_resizing(button)
        self.printing()
        self.partition.show_partition()
        self.partition.show_busy()

    # Событие по захвату объекта - пока ничего не делает
    def dragEnterEvent(self, event):
        # for button in self.buttons:
        #     if button.isDown():
        #         self.partition.change_state(button.x(), button.y())
        #         self.partition.show_busy()
        # print(event.position().x(), event.position().y())
        event.accept()

    # Событие по отпусканию кнопки после переноса - изменяет координаты центра объекта
    def dropEvent(self, event):
        for button in self.buttons:
            if button.isDown():
                i, j = self.partition.button_place(event.position().x(), event.position().y(), button)
                self.partition.show_busy()

                # i, j - индексы в сетке (координаты центра кнопки)
                # button.set_coords(int(x), int(y))
                # qwe = button.get_coords()
                # print(f'Button position after moving: {qwe[0]}, {qwe[1]}')

        self.printing()
        event.accept()

    # Событие рисования связей
    def paintEvent(self, event):
        qp = QPainter()
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.begin(self)
        draw_grid(qp, self.width(), self.height(), self.hor_parts, self.vert_parts)
        if len(self.logic_connected_pair) != 0:
            for pair in self.logic_connected_pair:
                if pair.is_correct():

                    x_from, y_from, x_to, y_to = pair.get_point_coordinates_fixed()
                    pt_from = QPoint(x_from, y_from)
                    pr_to = QPoint(x_to, y_to)

                    draw_lines(qp, pt_from, pr_to, pair, self.buttons)

                    qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

                    if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
                        qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                    else:
                        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

                    draw_triangle_fixed(qp, pair.btnl)
        qp.end()
        QWidget.paintEvent(self, event)

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
                # if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
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


# Метод рисования треугольника
def draw_triangle(qp, x_from, y_from, btn):
    x_center, y_center = btn.get_center_cords()

    if x_from > x_center:
        pnt_1 = QPoint(x_center + btn.width() / 2, y_center + 5)
        pnt_2 = QPoint(x_center + btn.width() / 2, y_center - 5)
        pnt_3 = QPoint(x_center + btn.width() / 2 + 5, y_center)
    elif x_from < x_center:
        pnt_1 = QPoint(x_center - btn.width() / 2, y_center + 5)
        pnt_2 = QPoint(x_center - btn.width() / 2, y_center - 5)
        pnt_3 = QPoint(x_center - btn.width() / 2 - 5, y_center)
    else:
        if y_from > y_center:
            pnt_1 = QPoint(x_center + 5, y_center + btn.height() / 2)
            pnt_2 = QPoint(x_center - 5, y_center + btn.height() / 2)
            pnt_3 = QPoint(x_center, y_center + btn.height() / 2 + 5)
        else:
            pnt_1 = QPoint(x_center + 5, y_center - btn.height() / 2)
            pnt_2 = QPoint(x_center - 5, y_center - btn.height() / 2)
            pnt_3 = QPoint(x_center, y_center - btn.height() / 2 - 5)

    triangle = QPolygon([pnt_1, pnt_2, pnt_3])
    qp.drawPolygon(triangle)


# Метод рисования треугольника с левой стороны - выход блока
def draw_triangle_fixed(qp, btn):
    x_center, y_center = btn.get_center_cords()

    pnt_1 = QPoint(x_center + btn.width() / 2, y_center + 5)
    pnt_2 = QPoint(x_center + btn.width() / 2, y_center - 5)
    pnt_3 = QPoint(x_center + btn.width() / 2 + 5, y_center)

    triangle = QPolygon([pnt_1, pnt_2, pnt_3])
    qp.drawPolygon(triangle)


def draw_ellipse_fixed(qp, btn):
    x_center, y_center = btn.get_center_cords()
    qp.drawEllipse(x_center - btn.width() / 2 - 10, y_center - 5, 10, 10)


# Метод рисования линий
def draw_lines(qp, pt_from, pt_to, pair, buttons):
    pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
    qp.setPen(pen)

    delta_x = pt_to.x() - pt_from.x()
    delta_y = pt_to.y() - pt_from.y()

    pt_start = pt_from
    pt_end = QPoint(pt_from.x() + pair.x_offset, pt_from.y())

    qp.drawLine(pt_start.x(), pt_start.y(), pt_end.x(), pt_end.y())

    pt_start = pt_end

    if delta_y != 0:
        pt_end = QPoint(pt_end.x(), pt_end.y() + pair.y_offset * delta_y / math.fabs(delta_y))
    elif delta_x > 0:
        if pair.on_one_line(buttons):
            pt_end = QPoint(pt_end.x(), pt_end.y() - pair.y_offset)
        else:
            pt_end = QPoint(pt_end.x(), pt_end.y())
    else:
        pt_end = QPoint(pt_end.x(), pt_end.y() - pair.y_offset)

    qp.drawLine(pt_start.x(), pt_start.y(), pt_end.x(), pt_end.y())

    pt_start = pt_end

    if delta_y != 0:
        pt_end = QPoint(pt_end.x() + math.fabs(delta_x) * delta_x / math.fabs(delta_x) - 2 * pair.x_offset,
                        pt_to.y() - pair.y_offset * delta_y / math.fabs(delta_y))
    elif delta_x > 0:
        if pair.on_one_line(buttons):
            pt_end = QPoint(pt_end.x() + math.fabs(delta_x) * delta_x / math.fabs(delta_x) - 2 * pair.x_offset,
                            pt_to.y() - pair.y_offset)
        else:
            pt_end = QPoint(pt_end.x() + math.fabs(delta_x) * delta_x / math.fabs(delta_x) - 2 * pair.x_offset,
                            pt_to.y())
    else:
        pt_end = QPoint(pt_end.x() + math.fabs(delta_x) * delta_x / math.fabs(delta_x) - 2 * pair.x_offset,
                        pt_to.y() - pair.y_offset)

    qp.drawLine(pt_start.x(), pt_start.y(), pt_end.x(), pt_end.y())

    pt_start = pt_end
    pt_end = QPoint(pt_end.x(), pt_to.y())

    qp.drawLine(pt_start.x(), pt_start.y(), pt_end.x(), pt_end.y())

    pt_start = pt_end
    pt_end = pt_to

    qp.drawLine(pt_start.x(), pt_start.y(), pt_end.x(), pt_end.y())


# Отрисовка сетки расположения блоков
def draw_grid(qp, area_width, area_height, hor_parts, vert_parts):
    hor_line_x_start, hor_line_y_start = 5, 5
    hor_line_x_end, hor_line_y_end = area_width - 5, 5
    vert_line_x_start, vert_line_y_start = 5, 5
    vert_line_x_end, vert_line_y_end = 5, area_height - 5
    qp.setBrush(QtCore.Qt.NoBrush)
    pen = QPen(QColor("#90FFFFF0"), 2, QtCore.Qt.CustomDashLine)
    pen.setDashPattern([30, 5])
    qp.setPen(pen)

    if hor_parts > 1:
        for i in range(1, hor_parts):
            qp.drawLine(
                hor_line_x_start,
                hor_line_y_start + i * area_height / hor_parts - 5,
                hor_line_x_end,
                hor_line_y_end + i * area_height / hor_parts - 5
            )

    if vert_parts > 1:
        for i in range(1, vert_parts):
            qp.drawLine(
                vert_line_x_start + i * area_width / vert_parts - 5,
                vert_line_y_start,
                vert_line_x_end + i * area_width / vert_parts - 5,
                vert_line_y_end
            )


# Класс разделения поля на места для кнопок
class SpaceAccess:

    # Разбиение поля на клетки
    def __init__(self, width, height, hor_part, vert_part):
        self.width = width
        self.height = height
        self.hor_parts = hor_part
        self.vert_parts = vert_part
        self.is_busy = []  # индикатор занятости ячейки
        self.space_area = []  # массив пар координат мест
        for i in range(self.vert_parts):
            column_part = []
            column_busy = []
            for j in range(self.hor_parts):
                place = round(self.width / (2 * self.hor_parts)) + round(j / self.hor_parts * self.width), \
                        round(self.height / (2 * self.vert_parts)) + round(i / self.vert_parts * self.height)
                # print(place)
                column_part.append(place)
                column_busy.append(False)
            self.space_area.append(column_part)
            self.is_busy.append(column_busy)

    # Первое размещение кнопки на поле
    def place_button_first(self, btn):
        for i in range(self.vert_parts):
            for j in range(self.hor_parts):
                if not self.is_busy[i][j]:
                    btn.move_center(self.space_area[i][j][0], self.space_area[i][j][1])
                    self.is_busy[i][j] = True
                    # print("place_button_first", i, j)
                    btn.space_access_indexes = i, j
                    # print("space_access_indexes =", btn.space_access_indexes)
                    return i, j
        return -1, -1

    def place_button_resizing(self, btn):
        i, j = btn.space_access_indexes
        x, y = self.space_area[i][j]
        btn.move_center(x, y)
        self.is_busy[i][j] = True

    # Перемещение кнопки на новое место
    def button_place(self, move_x, move_y, btn):
        min_radius = 1e6
        indexes = -1, -1
        x_center, y_center = btn.get_center_cords()
        for i in range(self.vert_parts):
            for j in range(self.hor_parts):
                pos = self.space_area[i][j]
                radius = math.sqrt(math.pow(pos[0] - move_x, 2) + math.pow(pos[1] - move_y, 2))
                if radius < min_radius:
                    indexes = i, j
                    min_radius = radius

        i, j = indexes[0], indexes[1]
        if not self.is_busy[i][j]:
            self.is_busy[i][j] = True
            # print(self.space_area[i][j][0], self.space_area[i][j][1])
            btn.move_center(self.space_area[i][j][0], self.space_area[i][j][1])
            # self.change_state((x_center, y_center))
            self.change_state(btn.space_access_indexes)
            # return self.space_area[i][j]
            # print("button_place", i, j)
            btn.space_access_indexes = i, j
            # print("space_access_indexes =", btn.space_access_indexes)
            # print("is_busy", i, j, self.is_busy[i][j])
            return i, j

        # return self.get_indexes_by_cords(x_center, y_center)
        return btn.space_access_indexes

    # Возвращает индексы по координатам
    def get_indexes_by_cords(self, x, y):
        min_radius = 1e6
        indexes = -1, -1
        for i in range(self.vert_parts):
            for j in range(self.hor_parts):
                pos = self.space_area[i][j]
                radius = math.sqrt(math.pow(pos[0] - x, 2) + math.pow(pos[1] - y, 2))
                if radius < min_radius:
                    indexes = i, j
                    min_radius = radius
        # print("button_place", indexes[0], indexes[1])
        return indexes[0], indexes[1]

    # Смена состояния конкретного места поля (занято/свободно)
    def change_state(self, center_cords):
        # min_radius = 1e6
        indexes = center_cords
        # indexes = -1, -1
        # x_center = center_cords[0]
        # y_center = center_cords[1]
        # for i in range(self.vert_parts):
        #     for j in range(self.hor_parts):
        #         pos = self.space_area[i][j]
        #         radius = math.sqrt(math.pow(pos[0] - x_center, 2) + math.pow(pos[1] - y_center, 2))
        #         if radius < min_radius:
        #             indexes = i, j
        #             min_radius = radius
        #
        i, j = indexes[0], indexes[1]
        self.is_busy[i][j] = not self.is_busy[i][j]

    # Показать разделения поля (массив)
    def show_partition(self):
        for i in range(self.vert_parts):
            print(self.space_area[i])

    # Показать какие места заняты на поле (массив)
    def show_busy(self):
        str = ''
        for i in range(self.vert_parts):
            for j in range(self.hor_parts):
                if self.is_busy[i][j]:
                    str += 'X '
                else:
                    str += 'O '
            str += '\n'
        print(str)


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

        self.x_offset = 20
        self.y_offset = 40

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
            return center_btnl_x, center_btnl_y - (self.btnl.height() / 2), \
                   center_btnr_x, center_btnr_y + (self.btnr.height() / 2)

        elif center_btnl_y < center_btnr_y - self.btnl.height() / 2:
            return center_btnl_x, center_btnl_y + (self.btnl.height() / 2), \
                   center_btnr_x, center_btnr_y - (self.btnr.height() / 2)

        elif center_btnl_x < center_btnr_x:
            return center_btnl_x + (self.btnl.width() / 2), center_btnl_y, \
                   center_btnr_x - (self.btnr.width() / 2), center_btnr_y

        else:
            return center_btnl_x - (self.btnl.width() / 2), center_btnl_y, \
                   center_btnr_x + (self.btnr.width() / 2), center_btnr_y

    # Получить координаты точки фиксированные
    def get_point_coordinates_fixed(self):
        center_btnl_x = self.line_start_x
        center_btnl_y = self.line_start_y

        center_btnr_x = self.line_end_x
        center_btnr_y = self.line_end_y

        return center_btnl_x + (self.btnl.width() / 2), center_btnl_y, \
               center_btnr_x - (self.btnr.width() / 2), center_btnr_y

    # Проверка на коррекность пары
    def is_correct(self):
        # return not (self.btnl is None or self.btnr is None)
        return self.btnl and self.btnr

    def on_one_line(self, buttons):
        i, j = self.btnl.space_access_indexes
        if i == self.btnr.space_access_indexes[0] and \
                self.btnr.space_access_indexes[1] - j > 1:
            for button in buttons:
                if button.space_access_indexes[0] == i and \
                        j < button.space_access_indexes[1] < self.btnr.space_access_indexes[1]:
                    return True
        return False
