"""
Тут описывается все, что касается внутренностей кнопок
"""
import datetime
import math
import random

import PySide6
from PySide6.QtWidgets import QPushButton, QMessageBox
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QFont
from matplotlib.dates import date2num

import DB
import Graph
import Table
import compare_model_final
import compare_model_lph
import compare_model_lph_v2
import compare_model_turbain
from moving_area import ButtonsPair

from enclosed_dialog import LPHDialog, CondDialog, WSPDialog, LPHDialogDB, CMPDialog, CondDialogDB, WSPDialogDB, \
    DialogDB

from functions import do_func_by_name

# # Откуда брать данные (Для будущих поколений)
# class CalcMod(enum):
#     DB = 0,
#     DIALOG = 1

# Расчет времени между нажатиями на кнопку
time = datetime.datetime.now()


# Класс абстрактной кнопки
class AbsMovingButton(QPushButton):
    # saving
    button_id = -1  # -#-#-
    pos_x = 0
    pos_y = 0
    button_name = 'free'
    button_type = 'Undefined'  # -#-#-
    send_flag = False
    # ------

    def __init__(self, encl_dialog, height, width, title, mc_dialog, parent=None):
        QPushButton.__init__(self, parent)
        self.moving_area = parent
        self.button_name = title
        self.enclosed_dialog = encl_dialog(self.button_name, 250, 500)  # для работы с БД
        self.manual_calc_dialog = mc_dialog(self.button_name, height, width)  # для работы вручную
        # self.cmp_dialog = cmp_dialog()
        self.info = None
        self.graph = Graph.GraphWindow(self.button_name)
        self.expr_string = None
        self.function_name = None
        self.function = None
        self.value = None
        self.number = None
        self.name_of_input_data = None  # название таблицы входных данных
        self.name_of_output_data = None  # название таблицы выходных данных
        self.last_calculated_data = []
        self.calculation_id = 0
        self.compare_model_out = None
        self.space_access_indexes = -1, -1  # !!! ИНДЕКСЫ ВНУТРИ ПОЛЯ РАЗДЕЛЕНИЯ
        self.setFixedSize(140, 50)
        self.setText(self.button_name)

        self.setFont(QFont("Courier", 10))
        self.setStyleSheet(
            "border-radius: 6px; "
            "border: 1px solid black; "
            "background-color: #fc9481; "
            "color: black; "
            "font-weight: 1000; "
        )

        # self.clicked.connect(self.open_dialog)

        self.enclosed_dialog.destroy_connect_button.clicked.connect(self.destroy_connection)
        self.enclosed_dialog.change_title_button.clicked.connect(self.change_title)  # IN ADD VALUE
        self.enclosed_dialog.close_button.clicked.connect(self.return_to_main)
        self.enclosed_dialog.delete_button.clicked.connect(self.del_object)
        self.enclosed_dialog.block_info_button.clicked.connect(self.show_info_spec)
        self.enclosed_dialog.graph_button.clicked.connect(self.show_graph)
        self.enclosed_dialog.manual_calc.clicked.connect(self.show_mc_dialog)
        # self.enclosed_dialog.open_cmp_dialog.clicked.connect(self.show_cmp_dialog)
        # self.graph.updateButton.clicked.connect(self.update_graph)

        self.manual_calc_dialog.calc_button.clicked.connect(self.calc_manual_data)
        self.manual_calc_dialog.close_button.clicked.connect(self.manual_dialog_close)

        # self.cmp_dialog.close_button.clicked.connect(self.cmp_dialog_close)
        # self.cmp_dialog.cmp_button.clicked.connect(self.cmp_with_db)

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.open_dialog()

    def move_center(self, x_center, y_center):
        move_x = x_center - self.width() / 2
        move_y = y_center - self.height() / 2
        self.move(move_x, move_y)

    def get_center_cords(self):
        return self.x() + self.width() / 2, self.y() + self.height() / 2

    # Код от старого модуля сравнения
    # def cmp_with_db(self):
    #     out_data = DB.get_data(self.name_of_output_data)
    #     self.cmp_dialog.textarea.clear()
    #
    #     flag = False
    #     for row in out_data:
    #         for column in row:
    #             if column in DB.required_data_lph:
    #                 delta = (math.fabs(float(DB.required_data_lph[column]) - float(row[column])) / float(
    #                     DB.required_data_lph[column]))
    #                 if delta > 0.05:
    #                     flag = True
    #                     self.cmp_dialog.textarea.insertHtml(
    #                         f"<font color='red' size='5'>Критическое расхождение на {out_data.index(row) + 1} наборе "
    #                         f"в {column}! "
    #                         f"[{delta}]</font><br> "
    #                     )
    #     if not flag:
    #         self.cmp_dialog.textarea.insertHtml(
    #             f"<font color='green' size='5'>Значения в пределах нормы</font><br>"
    #         )

    # def show_cmp_dialog(self):
    #     self.cmp_dialog.show()
    #
    # def cmp_dialog_close(self):
    #     self.cmp_dialog.close()

    def show_mc_dialog(self):
        self.enclosed_dialog.close()
        self.manual_calc_dialog.show()

    def calc_manual_data(self):
        self.add_value_manual()
        self.evaluate_manual()

    def manual_dialog_close(self):
        self.manual_calc_dialog.close()
        self.enclosed_dialog.show()

    def show_info_spec(self):
        self.show_info()

    # Метод вызова диалогового окна с таблицами, тянет данные с БД
    def show_info(self, inp_data_columns=None, out_data_columns=None, cmp_data_columns=None):
        self.info = Table.TableWindow(
            600,
            800,
            self.name_of_input_data,
            self.name_of_output_data,
            self.text(),
            self.compare_model_out)

        inp_data = DB.get_data(self.name_of_input_data, inp_data_columns)
        out_data = DB.get_data(self.name_of_output_data, out_data_columns)
        for record in out_data:
            print(record['row_id'])

        if not inp_data or not out_data:
            return

        inp_prepared_data = DB.parse_data(inp_data)
        out_prepared_data = DB.parse_data(out_data)

        if cmp_data_columns:
            cmp_data = DB.get_data(self.compare_model_out, cmp_data_columns)  # FIX NAME
            cmp_prepared_data = DB.parse_data(cmp_data)
            for i in range(len(cmp_prepared_data)):
                out_prepared_data[i] = cmp_prepared_data[i] + out_prepared_data[i]

        Table.load_data_inp_table(inp_prepared_data, self.info.table_window_inp)
        Table.load_data_out_table(out_prepared_data, self.info.table_window_out)

        self.info.show()

    def update_data_graph(self):
        self.graph.close()

        name_inp_data = DB.readable_to_data(self.graph.inp_combo.currentText())
        name_out_data = DB.readable_to_data(self.graph.out_combo.currentText())

        inp_arr_data = DB.get_data(self.name_of_input_data)
        out_arr_data = DB.get_data(self.name_of_output_data)
        self.graph = Graph.GraphWindow(
            self.button_name,
            inp_arr_data,
            name_inp_data,
            out_arr_data,
            name_out_data,
            self.update_data_graph,
            self.update_time_graph)

        self.graph.show()

    def update_time_graph(self):
        date_from = self.graph.date
        time_from = DB.TO_DT_DB_FORMAT(date_from.getDate())

        name_inp_data = DB.readable_to_data(self.graph.inp_combo.currentText())
        name_out_data = DB.readable_to_data(self.graph.out_combo.currentText())

        inp_arr_data = DB.get_data_timediff(
            self.name_of_input_data,
            "date",
            time_from
        )
        out_arr_data = DB.get_data_timediff(
            self.name_of_output_data,
            "recording_date",
            time_from
        )

        if not inp_arr_data or not out_arr_data:
            QMessageBox.warning(
                None,
                "Ошибка обновления графика",
                "В базе нет данных за выбранный период.",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok
            )
            return

        self.graph.close()

        self.graph = Graph.GraphWindow(
            self.button_name,
            inp_arr_data,
            name_inp_data,
            out_arr_data,
            name_out_data,
            self.update_data_graph,
            self.update_time_graph)

        self.graph.date_line_edit.setText(date_from.toString("dd-MM-yy"))

        self.graph.show()

    # Метод вызова диалогового окна с графиком, тянет данные из БД
    def show_graph(self):
        inp_arr_data = DB.get_data(self.name_of_input_data)
        out_arr_data = DB.get_data(self.name_of_output_data)
        warning_msg = ""

        if not inp_arr_data:
            warning_msg += "Нет входных данных для построения графика.\n"

        if not out_arr_data:
            warning_msg += "Нет выходных данных для построения графика."

        if warning_msg != "":
            QMessageBox.warning(
                None,
                "Ошибка открытия графика",
                warning_msg,
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok
            )
            return

        self.graph = Graph.GraphWindow(
            title=self.button_name,
            inp_data=inp_arr_data,
            name_inp_data=None,
            out_data=out_arr_data,
            name_out_data=None,
            update_data_method=self.update_data_graph,
            update_time_method=self.update_time_graph
        )

        self.graph.show()

    # Разорвать соединение с этой кнопкой
    def destroy_connection(self):
        self.moving_area.destroy_connection(self)
        self.enclosed_dialog.close()

    # Изменить заголовок кнопки
    def change_title(self):
        title = self.enclosed_dialog.change_title_edit.text()
        self.enclosed_dialog.setWindowTitle(title)
        self.setText(title)

        self.set_button_name(self.enclosed_dialog.windowTitle())

    # Открывает вложенное диалоговое окно для ввода или просмотра значения
    def open_dialog(self):
        self.enclosed_dialog.show()

    # Возврат в основное окно
    def return_to_main(self):
        self.enclosed_dialog.close()

    # Установка значения с закрытием окна
    def add_value_manual(self):
        pass

    # Удаление кнопки с разрушением связей (для общего удаления)
    def clear_object(self):
        deleted_count = 0
        for i in range(len(self.moving_area.logic_connected_pair)):
            if self.moving_area.logic_connected_pair[i - deleted_count].btnl == self or \
                    self.moving_area.logic_connected_pair[i - deleted_count].btnr == self:
                self.moving_area.logic_connected_pair.remove(self.moving_area.logic_connected_pair[i - deleted_count])
                deleted_count += 1

        self.deleteLater()
        self.enclosed_dialog.close()

        if self in self.moving_area.buttons:
            self.moving_area.buttons.remove(self)
            self.moving_area.partition.change_state(self.space_access_indexes)

    # Удаление кнопки с разрушением связей (одиночное)
    def del_object(self):
        # FIX !!! переделать цикл (хотя лучше не трогать пока работает)
        j = 0
        was_warning = False
        for i in range(len(self.moving_area.logic_connected_pair)):
            if self.moving_area.logic_connected_pair[i - j].btnl == self or \
                    self.moving_area.logic_connected_pair[i - j].btnr == self:
                if not was_warning:
                    was_warning = True
                    ackn = QMessageBox(
                        QMessageBox.Warning,
                        "Удаление блока",
                        "Данное действие приведет к разрыву всех связей с блоком. Продолжить?"
                    )

                    ackn.addButton("&НЕТ", QMessageBox.NoRole)
                    yes = ackn.addButton("&ДА", QMessageBox.YesRole)
                    ackn.setDefaultButton(yes)
                    result = ackn.exec()

                    if result != QMessageBox.Accepted:
                        return

                self.moving_area.logic_connected_pair.remove(self.moving_area.logic_connected_pair[i - j])
                j = j + 1

        self.deleteLater()
        self.enclosed_dialog.close()

        if self in self.moving_area.buttons:
            self.moving_area.buttons.remove(self)
            self.moving_area.partition.change_state(self.space_access_indexes)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mime_data = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.MoveAction)

    def mousePressEvent(self, event):
        global time
        if event.buttons() == Qt.RightButton:
            prev_time = time
            time = now_time = datetime.datetime.now()

            # Если логические пары уже есть
            if len(self.moving_area.logic_connected_pair) != 0:

                # Сброс пары, если между кликами больше 2 секунд
                if math.fabs(date2num(now_time) - date2num(prev_time)) * 100000 > 2:
                    for pair in self.moving_area.logic_connected_pair:
                        if pair.btnl and not pair.btnr:
                            self.moving_area.logic_connected_pair.remove(pair)
                            # print("flush")

                # Обработка ситуации, когда таргет является одиночной левой кнопкой в паре
                # Решение - неправильное соединение - выход
                for pair in self.moving_area.logic_connected_pair:
                    if pair.btnl == self and pair.btnr is None:
                        print("Неправильное соеднинение ret1")
                        return

                # Обработка ситуации, когда левая одиночная кнопка есть, и таргет не является левой кнопкой
                # Решение - правильное соединение - замыкание пары
                for pair in self.moving_area.logic_connected_pair:
                    if pair.btnl != self and pair.btnr is None:

                        # Обработка ситуации образования циклов
                        # Решение - запрет связи
                        marker = None

                        for pair in self.moving_area.logic_connected_pair:
                            if pair.btnr is None:
                                marker = pair.btnl
                                print("marker:", marker.text())

                        if marker:
                            target = self
                            print("target:", target.text())

                            # Обработка ситуации создания повторной связи
                            # Решение - запрет связи
                            for pair in self.moving_area.logic_connected_pair:
                                if pair.btnl == marker and pair.btnr == target:
                                    print("Запрет повторной связи ret4")
                                    return

                            i = len(self.moving_area.buttons) * (len(self.moving_area.buttons) - 1)
                            while i > 0:
                                temp_targets = [target]
                                for target in temp_targets:
                                    for pair in self.moving_area.logic_connected_pair:
                                        if pair.btnl == target:
                                            if pair.btnr not in temp_targets:
                                                temp_targets.append(pair.btnr)

                                for target in temp_targets:
                                    if target == marker:
                                        print("Запрет образования цикла ret3")
                                        return
                                i -= 1

                        pair.set_btnr(self)
                        print("Установка правой кнопки")
                        return

            # Если все пары замкнуты
            # Решение - создание новой логической пары - установка левой кнопки в пару
            # if len(self.moving_area.buttons) > len(self.moving_area.logic_connected_pair) + 1:
            pair = ButtonsPair()
            pair.set_btnl(self)
            self.moving_area.logic_connected_pair.append(pair)

        return QPushButton.mousePressEvent(self, event)

    def evaluate_manual(self) -> 'calculation result (maybe double, int, float, ect.)':
        pass

    def calculate_db(self):
        data_in = DB.parse_data(DB.get_data(self.name_of_input_data))
        data_out = DB.get_data(self.name_of_output_data)
        id_out = DB.parse_data_for_name(data_out, "row_id")

        if len(self.last_calculated_data) == 0:
            self.last_calculated_data = id_out
        else:
            for id in id_out:
                if id not in self.last_calculated_data:
                    self.last_calculated_data.append(id)

        for row in data_in:
            if row[0] not in self.last_calculated_data:
                self.add_value_db(row)
                self.evaluate_db()

    def expression_to_string(self) -> str:
        self.expr_string = self.function

        return self.expr_string

    # # Метод адаптивного изменения размера кнопки под текст (Статический размер
    # def setTextWithResize(self, new_name):
    #     coeff = len(new_name)
    #     if coeff <= 5:
    #         self.resize(60, 50)
    #     else:
    #         self.resize(coeff * 12, 50)
    #     max_width = (self.moving_area.width() / self.moving_area.hor_parts) - 10
    #     if self.width() > max_width:
    #         self.resize(max_width, 50)
    #     self.setText(new_name)

    # ----------------------------------

    def set_coords(self, x, y):  # -#-#-
        self.space_access_indexes = x, y

    def get_coords(self):
        return self.space_access_indexes[0], self.space_access_indexes[1]

    # ----------------------------------

    def set_button_name(self, name: str):
        self.button_name = name

    def get_button_name(self):
        return self.button_name

    # ----------------------------------

    def set_send_flag(self, tf: bool):
        self.send_flag = tf

    def get_send_flag(self):
        return self.send_flag

    # ----------------------------------

    # def set_send_to(self, recipient: int):
    #     lst = self.send_to
    #     lst.append(recipient)
    #     self.send_to = lst
    #     # self.send_to.append(recipient)
    #
    # def get_send_to(self):
    #     return self.send_to

    # ----------------------------------

    def set_button_type(self, btn_type: str):  # -#-#-
        self.button_type = btn_type

    def get_button_type(self):  # -#-#-
        return self.button_type

    # ----------------------------------

    def set_button_id(self, btn_id: int):  # -#-#-
        self.button_id = btn_id

    def get_button_id(self):  # -#-#-
        return self.button_id
    # ----------------------------------

    def add_value_db(self, row):
        pass

    def evaluate_db(self):
        pass


# класс конкретной кнопки для функции LPH
class LPHButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent=None):
        AbsMovingButton.__init__(self, DialogDB, 700, 600, "Подогреватель", LPHDialog, parent)
        # self.resize(80, 80)
        self.function_name = "LPH"
        self.name_of_input_data = "lph_in"
        self.name_of_output_data = "lph_out"
        self.compare_model_out = "cmp_lph_out"
        # self.info = Table.TableWindow(self.name_of_input_data, self.name_of_output_data, "Подогреватель")

        # Генерация номера объекта
        self.number = LPHButton.static_num
        if self.number != 0:
            self.setText(self.text() + f"_{self.number}")
        LPHButton.static_num += 1

        self.set_button_type(self.function_name)  # -#-#-
        self.set_button_name(self.text())  # -#-#-

    def show_info_spec(self):
        inp_colums = """
            date, 
            steam_pressure, 
            condensate_temperature, 
            condensate_flow_rate, 
            internal_diameter, 
            outer_diameter, 
            water_passes, 
            length_tube, 
            number_tubes, 
            heating_area, 
            heat_conductivity, 
            row_id
        """
        out_columns = """
            calc_date, 
            recording_date, 
            heat_transfer_coefficient, 
            underheating_condensate, 
            condensate_outlet_temperature, 
            row_id
        """
        cmp_columns = """
            state, 
            its,
            technical_condition,
            recommended_effect
        """
        self.show_info(inp_colums, out_columns, cmp_columns)

    def add_value_manual(self):
        values = [
            float(self.manual_calc_dialog.P_п_line_edit.text()),
            float(self.manual_calc_dialog.t_вх_line_edit.text()),
            float(self.manual_calc_dialog.G_к_line_edit.text()),
            float(self.manual_calc_dialog.d_вн_line_edit.text()),
            float(self.manual_calc_dialog.d_нар_line_edit.text()),
            float(self.manual_calc_dialog.z_line_edit.text()),
            float(self.manual_calc_dialog.l_line_edit.text()),
            float(self.manual_calc_dialog.N_line_edit.text()),
            float(self.manual_calc_dialog.F_line_edit.text()),
            float(self.manual_calc_dialog.lyambda_me_line_edit.text())
        ]

        self.value = values

    def add_value_db(self, row_data):
        self.calculation_id = row_data[0]

        values = [
            float(row_data[2]),
            float(row_data[3]),
            float(row_data[4]),
            float(row_data[5]),
            float(row_data[6]),
            float(row_data[7]),
            float(row_data[8]),
            float(row_data[9]),
            float(row_data[10]),
            float(row_data[11])
        ]

        self.value = values

    def evaluate_manual(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function_name, self.value)

        self.manual_calc_dialog.k_ideal_line_edit.setText(f"{result[0]:.{4}f}")
        self.manual_calc_dialog.delta_t_out_ideal_line_edit.setText(f"{result[1]}")
        self.manual_calc_dialog.t_out_line_edit.setText(f"{result[2]:.{4}f}")

        return result

    def evaluate_db(self):
        result = do_func_by_name(self.function_name, self.value)

        cmp_data = DB.get_data("cmp_lph_in", row_id=self.calculation_id)
        cmp_data_parsed = DB.parse_data(cmp_data)[0]

        cmp_data_parsed.pop(0)
        cmp_data_parsed.pop(len(cmp_data_parsed) - 1)

        cmp_prepared = compare_model_lph_v2.lph_real(cmp_data_parsed)
        cmp_result = compare_model_lph_v2.technical_condition_lph(result, cmp_prepared)

        DB.add_value_lph(self.calculation_id, result)
        DB.add_value_cmp(self.compare_model_out, self.calculation_id, cmp_result)

        return result


# Класс кнопки с функцией конденсатора
class CondButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent=None):
        AbsMovingButton.__init__(self, DialogDB, 700, 600, "Конденсатор", CondDialog, parent)
        self.function_name = "Cond_red"
        self.name_of_input_data = "condenser_in"
        self.name_of_output_data = "condenser_out"
        self.compare_model_out = "cmp_cond_out"

        # Генерация номера объекта
        self.number = CondButton.static_num
        if self.number != 0:
            self.setText(self.text() + f"_{self.number}")
        CondButton.static_num += 1

        self.set_button_type(self.function_name)  # -#-#-
        self.set_button_name(self.text())  # -#-#-

    def show_info_spec(self):
        inp_colums = """
            date, 
            consumption_steam, 
            consumption_water, 
            temperature_entry, 
            diameter_outside, 
            diameter_inside, 
            number_of_water_strokes, 
            water_speed, 
            square, 
            tube_length, 
            saturation_temperature, 
            row_id
        """
        out_columns = """
            calc_date, 
            recording_date, 
            water_temperature, 
            saturation_temperature, 
            hydraulic_resistance, 
            heat_transfer, 
            row_id
        """
        cmp_columns = """
            state, 
            its,
            technical_condition,
            recommended_effect
        """
        self.show_info(inp_colums, out_columns, cmp_columns)

    def add_value_manual(self):
        values = [
            float(self.manual_calc_dialog.Gп_line_edit.text()),
            float(self.manual_calc_dialog.Gв_line_edit.text()),
            float(self.manual_calc_dialog.t1в_line_edit.text()),
            float(self.manual_calc_dialog.dн_line_edit.text()),
            float(self.manual_calc_dialog.dвн_line_edit.text()),
            float(self.manual_calc_dialog.z_line_edit.text()),
            float(self.manual_calc_dialog.W_line_edit.text()),
            float(self.manual_calc_dialog.F_line_edit.text()),
            float(self.manual_calc_dialog.L_line_edit.text()),
            float(self.manual_calc_dialog.tk_line_edit.text())
        ]

        self.value = values

    def add_value_db(self, row_data):
        self.calculation_id = row_data[0]

        values = [
            float(row_data[2]),
            float(row_data[3]),
            float(row_data[4]),
            float(row_data[5]),
            float(row_data[6]),
            float(row_data[7]),
            float(row_data[8]),
            float(row_data[9]),
            float(row_data[10]),
            float(row_data[11])
        ]

        self.value = values

    def evaluate_manual(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function_name, self.value)

        self.manual_calc_dialog.out1_line_edit.setText(f"{result[0]:1.{3}f}")
        self.manual_calc_dialog.out2_line_edit.setText(f"{result[1]:1.{3}f}")
        self.manual_calc_dialog.out3_line_edit.setText(f"{result[2]:1.{3}f}")
        self.manual_calc_dialog.out4_line_edit.setText(f"{result[3]:1.{3}f}")

        return result

    def evaluate_db(self):
        result = do_func_by_name(self.function_name, self.value)

        cmp_data = DB.get_data("cmp_cond_in", row_id=self.calculation_id)
        cmp_data_parsed = DB.parse_data(cmp_data)[0]

        cmp_data_parsed.pop(0)
        cmp_data_parsed.pop(len(cmp_data_parsed) - 1)

        cmp_result = compare_model_final.technical_condition_cond(result, cmp_data_parsed)

        DB.add_value_cond(self.calculation_id, result)
        DB.add_value_cmp(self.compare_model_out, self.calculation_id, cmp_result)

        return result


# Класс кнопки с функцией WSP
class WSPButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent=None):
        AbsMovingButton.__init__(self, DialogDB, 700, 600, "Турбина", WSPDialog, parent)
        self.function_name = "WSP"  # -#-#-
        self.name_of_input_data = "turbine_in"
        self.name_of_output_data = "turbine_out"
        self.compare_model_out = "cmp_wsp_out"

        # Генерация номера объекта
        self.number = WSPButton.static_num
        if self.number != 0:
            self.setText(self.text() + f"_{self.number}")
        WSPButton.static_num += 1

        self.set_button_type(self.function_name)  # -#-#-
        self.set_button_name(self.text())  # -#-#-

    def show_info_spec(self):
        inp_colums = """
            date, 
            temperature_entry, 
            pressure_entry, 
            consumption_entry, 
            pressure_out, 
            efficiency, 
            number_of_selections, 
            selection_pressure, 
            sampling_flow, 
            row_id
        """
        out_columns = """
            calc_date, 
            recording_date, 
            enthalpy_before, 
            entropy_before, 
            enthalpy_after, 
            entropy_after, 
            steam_temperature, 
            enthalpy_1, 
            steam_temperature_1, 
            row_id
        """
        cmp_columns = """
            state, 
            its,
            technical_condition,
            recommended_effect
        """
        self.show_info(inp_colums, out_columns, cmp_columns)

    def add_value_manual(self):
        values = [
            float(self.manual_calc_dialog.G_вход_line_edit.text()),
            float(self.manual_calc_dialog.P_вход_цилиндра_line_edit.text()),
            float(self.manual_calc_dialog.t_вход_цилинда_line_edit.text()),
            float(self.manual_calc_dialog.P_выход_цилиндра_line_edit.text()),
            float(self.manual_calc_dialog.этта_цилиндра_line_edit.text()),
            [float(self.manual_calc_dialog.G_отбор_line_edit.text())],
            [float(self.manual_calc_dialog.P_отбор_line_edit.text())]
        ]

        self.value = values

    def add_value_db(self, row_data):
        self.calculation_id = row_data[0]

        values = [
            float(row_data[2]),
            float(row_data[3]),
            float(row_data[4]),
            float(row_data[5]),
            float(row_data[6]),
            [float(row_data[7])],
            [float(row_data[8])]
        ]

        self.value = values

    def evaluate_manual(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function_name, self.value)

        self.manual_calc_dialog.h_вход_цилинда_line_edit.setText(f"{result[0]:1.{3}f}")
        self.manual_calc_dialog.s_вход_цилинда_line_edit.setText(f"{result[1]:1.{3}f}")
        self.manual_calc_dialog.h_выход_цилинда_реал_line_edit.setText(f"{result[2]:1.{3}f}")
        self.manual_calc_dialog.s_выход_цилинда_реал_line_edit.setText(f"{result[3]:1.{3}f}")
        self.manual_calc_dialog.t_выход_цилинда_реал_line_edit.setText(f"{result[4]:1.{3}f}")
        self.manual_calc_dialog.label_2_line_edit.setText(f"{result[5][1]:1.{3}f}")
        self.manual_calc_dialog.label_3_line_edit.setText(f"{result[5][2]:1.{3}f}")

        return result

    def evaluate_db(self):
        result = do_func_by_name(self.function_name, self.value)

        cmp_data = DB.get_data("cmp_wsp_in", row_id=self.calculation_id)
        cmp_data_parsed = DB.parse_data(cmp_data)[0]

        cmp_data_parsed.pop(0)
        cmp_data_parsed.pop(len(cmp_data_parsed) - 1)

        cmp_result = compare_model_turbain.technical_condition_wsp(result[5], cmp_data_parsed)

        DB.add_value_wsp(self.calculation_id, result)
        DB.add_value_cmp(self.compare_model_out, self.calculation_id, cmp_result)

        return result


# Функция разделения строки на элементы по _,
def value_spliter(value: str):
    split_values = value.split(", ")
    return split_values
