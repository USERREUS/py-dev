"""
Тут описывается все, что касается внутренностей кнопок
"""
import datetime
import math

from PySide6.QtWidgets import QPushButton, QMessageBox
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QFont

import DB
import Graph
import QTableWidgetExample
from graph_table_widgets import LPHTableWindow, GraphWindow
from moving_area import ButtonsPair

from enclosed_dialog import TESTDialog, LPHDialog, CondDialog, WSPDialog, LPHDialogDB, CMPDialog

from functions import do_func_by_name


# # Откуда брать данные (Для будущих поколений)
# class CalcMod(enum):
#     DB = 0,
#     DIALOG = 1


# Класс абстрактной кнопки
class AbsMovingButton(QPushButton):
    # saving
    pos_x = 0
    pos_y = 0
    button_name = 'free'
    send_flag = False
    send_to = 'None'
    # ------

    def __init__(self, parent, encl_dialog, mc_dialog, cmp_dialog):
        super().__init__(parent)

        self.moving_area = parent
        self.enclosed_dialog = encl_dialog()  # для работы с БД
        self.manual_calc_dialog = mc_dialog()  # для работы вручную
        self.cmp_dialog = cmp_dialog()
        self.info = LPHTableWindow()
        self.graph = GraphWindow()
        self.expr_string = None
        self.function_name = None
        self.function = None
        self.value = None
        self.number = None
        self.name_of_input_data = None  # название таблицы входных данных
        self.name_of_output_data = None  # название таблицы выходных данных
        self.last_calculated_data = 0

        self.setFont(QFont("Courier", 12))
        self.setStyleSheet("border-radius: 6px; background-color: #fc9481; color: black; font-weight: 1000;")

        self.clicked.connect(self.open_dialog)

        self.enclosed_dialog.destroy_connect_button.clicked.connect(self.destroy_connection)
        self.enclosed_dialog.change_title_button.clicked.connect(self.change_title)  # IN ADD VALUE
        self.enclosed_dialog.close_button.clicked.connect(self.return_to_main)
        self.enclosed_dialog.delete_button.clicked.connect(self.del_object)
        self.enclosed_dialog.block_info_button.clicked.connect(self.show_info)
        self.enclosed_dialog.graph_button.clicked.connect(self.show_graph)
        self.enclosed_dialog.manual_calc.clicked.connect(self.show_mc_dialog)
        self.enclosed_dialog.open_cmp_dialog.clicked.connect(self.show_cmp_dialog)
        # self.graph.updateButton.clicked.connect(self.update_graph)

        self.manual_calc_dialog.calc_button.clicked.connect(self.calc_manual_data)
        self.manual_calc_dialog.close_button.clicked.connect(self.manual_dialog_close)

        self.cmp_dialog.close_button.clicked.connect(self.cmp_dialog_close)
        self.cmp_dialog.cmp_button.clicked.connect(self.cmp_with_db)

    def cmp_with_db(self):
        out_data = DB.get_data(self.name_of_output_data)
        self.cmp_dialog.textarea.clear()

        flag = False
        for row in out_data:
            for column in row:
                if column in DB.required_data_lph:
                    delta = (math.fabs(float(DB.required_data_lph[column]) - float(row[column])) / float(DB.required_data_lph[column]))
                    if delta > 0.05:
                        flag = True
                        self.cmp_dialog.textarea.insertHtml(
                            f"<font color='red' size='5'>Критическое расхождение на {out_data.index(row) + 1} наборе "
                            f"в {column}! "
                            f"[{delta}]</font><br> "
                        )
        if not flag:
            self.cmp_dialog.textarea.insertHtml(
                f"<font color='green' size='5'>Значения в пределах нормы</font><br>"
            )

    def show_cmp_dialog(self):
        self.cmp_dialog.show()

    def cmp_dialog_close(self):
        self.cmp_dialog.close()

    def show_mc_dialog(self):
        self.enclosed_dialog.close()
        self.manual_calc_dialog.show()

    def calc_manual_data(self):
        self.add_value_manual()
        self.evaluate_manual()

    def manual_dialog_close(self):
        self.manual_calc_dialog.close()
        self.enclosed_dialog.show()

    # Метод вызова диалогового окна с таблицами, тянет данные с БД
    def show_info(self):
        inp_data = DB.get_data(self.name_of_input_data)
        out_data = DB.get_data(self.name_of_output_data)

        inp_prepared_data = DB.parse_data(inp_data)
        out_prepared_data = DB.parse_data(out_data)

        self.info.table_window_inp.TableWidget.clearContents()
        self.info.table_window_out.TableWidget.clearContents()

        QTableWidgetExample.load_data_table(inp_prepared_data, self.info.table_window_inp.TableWidget)
        QTableWidgetExample.load_data_table(out_prepared_data, self.info.table_window_out.TableWidget)

        self.info.show()

    def update_graph(self):
        self.graph.close()

        name_inp_data = DB.readable_to_data(self.graph.inp_combo.currentText())
        name_out_data = DB.readable_to_data(self.graph.out_combo.currentText())

        inp_arr_data = DB.get_data(self.name_of_input_data)
        out_arr_data = DB.get_data(self.name_of_output_data)
        self.graph = GraphWindow(inp_arr_data, name_inp_data, out_arr_data, name_out_data, self.update_graph)

        self.graph.show()

    # Метод вызова диалогового окна с графиком, тянет данные из БД
    def show_graph(self):
        inp_arr_data = DB.get_data(self.name_of_input_data)
        out_arr_data = DB.get_data(self.name_of_output_data)
        self.graph = GraphWindow(
            inp_data=inp_arr_data,
            name_inp_data=None,
            out_data=out_arr_data,
            name_out_data=None,
            update_method=self.update_graph
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
        self.setTextWithResize(title)

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

    # Удаление кнопки с разрушением связей
    def del_object(self):
        # FIX !!! переделать цикл (хотя лучше не трогать пока работает)
        j = 0
        for i in range(len(self.moving_area.logic_connected_pair)):
            if self.moving_area.logic_connected_pair[i - j].btnl == self or \
                    self.moving_area.logic_connected_pair[i - j].btnr == self:
                self.moving_area.logic_connected_pair.remove(self.moving_area.logic_connected_pair[i - j])
                j = j + 1

        self.deleteLater()
        self.enclosed_dialog.close()

        if self in self.moving_area.buttons:
            self.moving_area.buttons.remove(self)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mime_data = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.MoveAction)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            if len(self.moving_area.logic_connected_pair) != 0:
                for pair in self.moving_area.logic_connected_pair:
                    if pair.btnl == self and pair.btnr is None:
                        return

                for pair in self.moving_area.logic_connected_pair:
                    if pair.btnl != self and pair.btnr is None:
                        for pair_in in self.moving_area.logic_connected_pair:
                            if pair_in.btnl == self:
                                return

                        pair.set_btnr(self)
                        return

            if len(self.moving_area.buttons) > len(self.moving_area.logic_connected_pair) + 1:
                pair = ButtonsPair()
                pair.set_btnl(self)
                self.moving_area.logic_connected_pair.append(pair)

        return QPushButton.mousePressEvent(self, event)

    def evaluate_manual(self) -> 'calculation result (maybe double, int, float, ect.)':
        pass

    def expression_to_string(self) -> str:
        pass

    # Метод адаптивного изменения размера кнопки под текст
    def setTextWithResize(self, new_name):
        coeff = len(new_name)
        if coeff <= 5:
            self.resize(60, 50)
        elif coeff > 20:
            self.resize(240, 80)
        else:
            self.resize(coeff * 12, 80)
        self.setText(new_name)

    # ----------------------------------

    def set_coords(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_coords(self):
        return self.pos_x, self.pos_y  # SELF

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

    def set_send_to(self, recipient: str):
        self.send_to = recipient

    def get_send_to(self):
        return self.send_to


# Класс кнопки возведения в квадрат (НЕ РАБОТАЕТ)
class SquareXFunction(AbsMovingButton):
    static_num = 0

    def __init__(self, parent):
        super().__init__(parent, TESTDialog)
        self.resize(80, 80)
        self.setFont(QFont("Times", 16, QFont.Bold))
        self.function_name = "Возведение в квадрат"
        self.function = "square"
        self.enclosed_dialog.function_text_edit.setText(self.function_name)
        self.setText("X^2")
        self.name_of_data = 'time_calculation'

        # Генерация номера объекта
        self.number = SquareXFunction.static_num
        if self.number != 0:
            self.setTextWithResize(self.text() + f"_{self.number}")
        SquareXFunction.static_num += 1

    def add_value(self):
        # print(f"START method: add value of {self.text()}_____________________")
        try:
            self.value = [float(self.enclosed_dialog.variable_text_edit.text())]
            self.enclosed_dialog.close()

        except Exception:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка записи данных!")
            msg.setText("Введенные данные не могут быть интерпретированы")
            msg.setIcon(QMessageBox.Warning)

            msg.exec_()

        # finally:
        # print(f"END method: add value of {self.text()}_____________________")

    def evaluate(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function, self.value)
        print(self.value, result)
        self.enclosed_dialog.result_text_edit.setText(f"{result[0]}")  #:.{4}f}")

        calc_dt = datetime.datetime.now().isoformat()

        # for i in range(50):
        DB.add_value(self.text(), self.function_name, calc_dt, self.value[0], result[0])

        return result

    def expression_to_string(self) -> str:
        self.enclosed_dialog.variable_text_edit.setText(f"{self.value[0]}")
        self.expr_string = self.function + f"({self.value})"

        return self.expr_string


# класс конкретной кнопки для функции LPH
class LPHButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent):
        super().__init__(parent, LPHDialogDB, LPHDialog, CMPDialog)
        # self.resize(80, 80)
        self.function_name = "LPH"
        self.setTextWithResize("Подогреватель")
        self.name_of_input_data = "lph_inp_data"
        self.name_of_output_data = "lph_out_data"

        # Генерация номера объекта
        self.number = LPHButton.static_num
        if self.number != 0:
            self.setTextWithResize(self.text() + f"_{self.number}")
        LPHButton.static_num += 1

    def add_value_manual(self):
        values = [
            float(self.manual_calc_dialog.P_p_line_edit.text()),
            float(self.manual_calc_dialog.t_p_line_edit.text()),
            float(self.manual_calc_dialog.t_n_line_edit.text()),
            float(self.manual_calc_dialog.p_k_line_edit.text()),
            float(self.manual_calc_dialog.t_vx_line_edit.text()),
            float(self.manual_calc_dialog.G_k_line_edit.text()),
            float(self.manual_calc_dialog.etta_p_line_edit.text())
        ]

        self.value = values

    def add_value_db(self, row_data):

        values = [
            float(row_data[1]),
            float(row_data[2]),
            float(row_data[3]),
            float(row_data[4]),
            float(row_data[5]),
            float(row_data[6]),
            float(row_data[7])
        ]

        self.value = values

    def evaluate_manual(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function_name, self.value)

        self.manual_calc_dialog.D_p_line_edit.setText(f"{result[0]:.{4}f}")
        self.manual_calc_dialog.z_1_line_edit.setText(f"{result[1]}")
        self.manual_calc_dialog.k_line_edit.setText(f"{result[2]:.{4}f}")

        return result

    def evaluate_db(self):
        result = do_func_by_name(self.function_name, self.value)

        print(f"{result[0]:.{4}f}")
        print(f"{result[1]}")
        print(f"{result[2]:.{4}f}")

        DB.add_value_lph(result, self.name_of_output_data)

        return result

    def calculate_db(self):
        data = DB.get_data(self.name_of_input_data)
        data_out = DB.get_data(self.name_of_output_data)
        parsed_data = DB.parse_data(data)

        if len(data_out) == 0:
            self.last_calculated_data = 0
        else:
            parsed_out_data = DB.parse_data(data_out)
            self.last_calculated_data = parsed_out_data[len(parsed_out_data) - 1][0]

        if self.last_calculated_data >= parsed_data[len(parsed_data) - 1][0]:
            return

        for row in parsed_data:
            if row[0] > self.last_calculated_data:
                self.add_value_db(row)
                self.evaluate_db()

    def expression_to_string(self) -> str:
        self.expr_string = self.function

        return self.expr_string


# Класс кнопки с функцией конденсатора (НЕ РАБОТАЕТ)
class CondButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent):
        super().__init__(parent, CondDialog)

        self.resize(80, 80)
        self.setFont(QFont("Times", 16, QFont.Bold))
        self.function = "Cond"
        self.setTextWithResize("Конденсатор")

        # Генерация номера объекта
        self.number = CondButton.static_num
        if self.number != 0:
            self.setTextWithResize(self.text() + f"_{self.number}")
        CondButton.static_num += 1

    def add_value(self):
        values = [
            float(self.enclosed_dialog.Gп_line_edit.text()),
            float(self.enclosed_dialog.Gв_line_edit.text()),
            float(self.enclosed_dialog.t1в_line_edit.text()),
            float(self.enclosed_dialog.dн_line_edit.text()),
            float(self.enclosed_dialog.dвн_line_edit.text()),
            float(self.enclosed_dialog.z_line_edit.text()),
            float(self.enclosed_dialog.W_line_edit.text()),
            float(self.enclosed_dialog.F_line_edit.text()),
            float(self.enclosed_dialog.N_line_edit.text())
        ]

        self.value = values
        self.enclosed_dialog.close()

    def evaluate(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function, self.value)

        self.enclosed_dialog.out1_line_edit.setText(f"{result[0]:1.{3}f}")
        self.enclosed_dialog.out2_line_edit.setText(f"{result[1]:1.{3}f}")
        self.enclosed_dialog.out3_line_edit.setText(f"{result[2]:1.{3}f}")

        calc_dt = datetime.datetime.now().isoformat()

        # DB.condenser_out_add_value(calc_dt, calc_dt, result[0], result[1], result[2])

        return result

    def expression_to_string(self) -> str:
        self.expr_string = self.function

        return self.expr_string


# Класс кнопки с функцией WSP (НЕ РАБОТАЕТ)
class WSPButton(AbsMovingButton):
    static_num = 0

    def __init__(self, parent):
        super().__init__(parent, WSPDialog)

        self.resize(80, 80)
        self.setFont(QFont("Times", 16, QFont.Bold))
        self.function = "wsp"
        self.setTextWithResize("Турбина")

        # Генерация номера объекта
        self.number = WSPButton.static_num
        if self.number != 0:
            self.setTextWithResize(self.text() + f"_{self.number}")
        WSPButton.static_num += 1

    def add_value(self):
        # values = [
        #     float(self.enclosed_dialog.G_вход_line_edit.text()),
        #     float(self.enclosed_dialog.P_вход_цилиндра_line_edit.text()),
        #     float(self.enclosed_dialog.t_вход_цилинда_line_edit.text()),
        #     float(self.enclosed_dialog.P_выход_цилиндра_line_edit.text()),
        #     float(self.enclosed_dialog.этта_цилиндра_line_edit.text()),
        #     [float(self.enclosed_dialog.G_отбор_line_edit.text())],
        #     [float(self.enclosed_dialog.P_отбор_line_edit.text())]
        # ]
        #
        # print(values)
        #
        # self.value = values
        self.enclosed_dialog.close()

    def evaluate(self) -> 'calculation result (maybe list, double, int, float, ect.)':
        result = do_func_by_name(self.function, self.value)

        # self.enclosed_dialog.h_вход_цилинда_line_edit.setText(f"{result[0]:1.{3}f}")
        # self.enclosed_dialog.s_вход_цилинда_line_edit.setText(f"{result[1]:1.{3}f}")
        # self.enclosed_dialog.h_выход_цилинда_реал_line_edit.setText(f"{result[2]:1.{3}f}")
        # self.enclosed_dialog.s_выход_цилинда_реал_line_edit.setText(f"{result[3]:1.{3}f}")
        # self.enclosed_dialog.t_выход_цилинда_реал_line_edit.setText(f"{result[4]:1.{3}f}")
        # self.enclosed_dialog.label_2_line_edit.setText(f"{result[5][1]:1.{3}f}")
        # self.enclosed_dialog.label_3_line_edit.setText(f"{result[5][2]:1.{3}f}")

        calc_dt = datetime.datetime.now().isoformat()

        # DB.turbine_out_add_value(calc_dt, calc_dt, result[0], result[1], result[2], result[3], result[4])

        return result

    def expression_to_string(self) -> str:
        self.expr_string = self.function

        return self.expr_string


# Функция разделения строки на элементы по _,
def value_spliter(value: str):
    split_values = value.split(", ")
    return split_values
