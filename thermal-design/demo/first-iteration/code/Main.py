"""
Пока что не структуризированный код
"""
import json
import threading
import time

import DB
import sys

from PySide6 import QtCore
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QMainWindow, QMessageBox, QFileDialog

from buttons import LPHButton, CondButton, SquareXFunction, WSPButton
from moving_area import MovingArea

selected_file = ''  # текущий файл
treading_live = False


def set_selected_file(file_name: str):
    global selected_file
    selected_file = file_name


def get_selected_file():
    global selected_file
    return selected_file


# Метод добавления объектов на область движения
def action_add_function(moving_area: MovingArea, button_function):
    moving_area.buttons.append(button_function)
    button_function.show()


# # Метод добавления функции возведения в квадрат
# def action_func_square(moving_area: MovingArea):
#     func_square_button = SquareXFunction(moving_area)
#     func_square_button.enclosed_dialog.setWindowTitle(func_square_button.text())
#     func_square_button.set_button_name(func_square_button.enclosed_dialog.windowTitle())  #
#     action_add_function(moving_area, func_square_button)


# Метод доббавления функции LPH
def action_func_lph(moving_area: MovingArea):
    func_lph_button = LPHButton(moving_area)
    func_lph_button.set_button_name(func_lph_button.enclosed_dialog.windowTitle())  #
    action_add_function(moving_area, func_lph_button)


# Метод доббавления функции Cond
def action_func_cond(moving_area: MovingArea):
    func_cond_button = CondButton(moving_area)
    func_cond_button.set_button_name(func_cond_button.enclosed_dialog.windowTitle())  #
    action_add_function(moving_area, func_cond_button)


# Метод доббавления функции WSP
def action_func_wsp(moving_area: MovingArea):
    func_wsp_button = WSPButton(moving_area)
    func_wsp_button.set_button_name(func_wsp_button.enclosed_dialog.windowTitle())  #
    action_add_function(moving_area, func_wsp_button)


# Окно, которое включает в себя область движения
class MovingController(QMainWindow):

    def __init__(self):
        super(MovingController, self).__init__()

        self.setWindowTitle('Новый проект')
        self.setFixedSize(1080, 570)

        pal = self.palette()
        pal.setColor(QPalette.All, QPalette.Window, QColor(240, 240, 240))
        self.setPalette(pal)
        # self.setStyleSheet('background-color: #C7EFDECD;')

        self.moving_area = MovingArea()
        # self.moving_area.setStyleSheet('background-color: #FFFFFF;')
        self.setCentralWidget(self.moving_area)

        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet('background-color: #C7EFDECD;')
        self.create_menu_bar()

    # Метод создания главного меню
    def create_menu_bar(self):
        self.setMenuBar(self.menu_bar)

        functions_menu = QMenu("&Функции", self)
        self.menu_bar.addMenu(functions_menu)
        self.menu_bar.addAction("&Расчет", threading_run_start)
        self.menu_bar.addAction("&Стоп", threading_run_stop)
        self.menu_bar.actions()[2].setEnabled(False)  # Костыль
        self.menu_bar.addAction("&Очистить", clear_action_clicked)

        # functions_menu.addAction("&x^2", self.action_clicked)
        functions_menu.addAction("&Подогреватель", self.action_clicked)
        functions_menu.addAction("&Конденсатор", self.action_clicked)
        functions_menu.addAction("&Турбина", self.action_clicked)

        self.menu_bar.addAction("&Сохранить", save)  #
        self.menu_bar.addAction("&Сохранить как...", save_as)  #

        self.menu_bar.addAction("&Загрузить", load)  #

    # Обработчик события выбора пункта меню (конкретно вызываемой функции)
    @QtCore.Slot()
    def action_clicked(self):
        action = self.sender()

        # if action.text() == "&x^2":
        #     print("Action : " + action.text())
        #     action_func_square(moving_controller.moving_area)

        if action.text() == "&Подогреватель":
            print("Action : " + action.text())
            action_func_lph(moving_controller.moving_area)

        elif action.text() == "&Конденсатор":
            print("Action : " + action.text())
            action_func_cond(moving_controller.moving_area)

        elif action.text() == "&Турбина":
            print("Action : " + action.text())
            action_func_wsp(moving_controller.moving_area)


def threading_run():
    global treading_live
    while True:
        time.sleep(3)
        if treading_live:
            run()
        else:
            print("wait")


# Метод очистки рабочей области
def clear_action_clicked():
    moving_controller.moving_area.destroy()
    moving_controller.moving_area = MovingArea()
    moving_controller.setCentralWidget(moving_controller.moving_area)


# Подсчет глубины связей кнопок
def depth_of_connection():
    max_depth = 0
    top = None
    flag = False

    for pair in moving_controller.moving_area.logic_connected_pair:
        depth = 0
        if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
            top = pair.btnr
            flag = True
            depth += 1

        while flag:
            flag = False
            for _pair in moving_controller.moving_area.logic_connected_pair:
                if _pair.btnl == top and _pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
                    depth += 1
                    top = _pair.btnr
                    flag = True

        if depth > max_depth:
            max_depth = depth

    return max_depth


def threading_run_start():
    global treading_live
    treading_live = True
    for action in moving_controller.menu_bar.actions():
        if action.text() == "&Стоп":
            action.setEnabled(True)
        else:
            action.setEnabled(False)


def threading_run_stop():
    global treading_live
    treading_live = False
    for action in moving_controller.menu_bar.actions():
        if action.text() == "&Стоп":
            action.setEnabled(False)
        else:
            action.setEnabled(True)


# Старт вычислений
def run():
    print("START method: run() _______________________")  # отладочная информация
    print("Connecton depth: ", depth_of_connection())

    try:
        for button in moving_controller.moving_area.buttons:
            if not moving_controller.moving_area.is_in_logic_cp(button):
                print("alone button: ", button.text())
                button.calculate_db()

        list_temp = []  # решение проблемы повторного расчета
        noc = depth_of_connection()
        while True:
            flag = False
            for pair in moving_controller.moving_area.logic_connected_pair:
                print("Calc pair", pair.btnl.text(), pair.btnr.text())
                if pair.btnl.value is not None:
                    if pair.btnl in list_temp:
                        list_temp.remove(pair.btnl)
                    pair.btnl.add_value_db()
                    result = pair.btnl.evaluate_db()
                    if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
                        pair.btnr.value = result
                        list_temp.append(pair.btnr)
                else:
                    flag = True
            noc -= 1
            if not flag or noc <= 0:
                for btn in list_temp:
                    btn.add_value_db()
                    btn.evaluate_db()
                break

    except Exception as exc:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка расчета!")
        msg.setText(exc.__str__())
        msg.setIcon(QMessageBox.Critical)

        msg.exec()

    finally:
        print("END method: run() _______________________")


# ------------------------------
def save_as():
    file_name = QFileDialog.getSaveFileName(moving_controller.moving_area, 'Save project', '/PyCharm/pythonProject2',
                                            filter='*.json')[0]
    if file_name == '':
        return 0

    set_selected_file(file_name)

    i = 1
    with open(file_name, 'w+', encoding='utf-8') as first_try:
        first_try.write('{\n "data": [\n')

        for button in moving_controller.moving_area.buttons:
            json.dump({
                "button": f"{button.get_button_name()}",
                "position": [
                    {
                        "pos_x": f"{button.get_coords()[0]}",
                        "pos_y": f"{button.get_coords()[1]}"
                    }
                ]  # ,
                # "send_flag": f"{button.get_send_flag()}",
                # "send_to": f"{button.get_send_to()}"
            }
                , first_try, indent=4)

            i += 1
            if len(moving_controller.moving_area.buttons) >= i:
                first_try.write(',\n')

            print(f'Имя кнопки: {button.get_button_name()}')

        first_try.write('\n ]\n}')

    first_try.close()
    moving_controller.setWindowTitle(
        file_name[((file_name.rfind('/')) + 1):])  # меняем заголовок окна на название нашего файла
    print('in saving: ', moving_controller.moving_area.buttons)
    print("Saved us")


def save():
    file_name = get_selected_file()

    if file_name == '':
        save_as()
    else:
        i = 1
        with open(file_name, 'w+', encoding='utf-8') as first_try:
            first_try.write('{\n "data": [\n')

            for button in moving_controller.moving_area.buttons:
                json.dump({
                    "button": f"{button.get_button_name()}",
                    "position": [
                        {
                            "pos_x": f"{button.get_coords()[0]}",
                            "pos_y": f"{button.get_coords()[1]}"
                        }
                    ]# ,
                    # "send_flag": f"{button.get_send_flag()}",
                    # "send_to": f"{button.get_send_to()}"
                }
                    , first_try, indent=4)

                i += 1
                if len(moving_controller.moving_area.buttons) >= i:
                    first_try.write(',\n')

                print(f'Имя кнопки: {button.get_button_name()}')

            first_try.write('\n ]\n}')

        first_try.close()
        print('in saving: ', moving_controller.moving_area.buttons)
        print("Saved")


def load():
    save_msg = QMessageBox()  # предложение сохранить текущий проект
    save_msg.setWindowTitle('Внимание')
    save_msg.setText('Сохранить текущий проект?')
    save_msg.setInformativeText('Проект будет сохранен в текущий файл')
    save_msg.setIcon(QMessageBox.Question)

    save_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    save_msg.setDefaultButton(QMessageBox.Ok)
    save_msg.setButtonText(QMessageBox.Ok, 'Сохранить')
    save_msg.setButtonText(QMessageBox.Cancel, 'Отмена')

    nbtn = save_msg.exec()  # номер нажатой кнопки

    print('number of pressed button: ', nbtn)

    if nbtn == QMessageBox.Ok:
        print('ok was pressed')
        save()

    elif nbtn == QMessageBox.Cancel:  # крестик тоже считается как кнопка отмены
        print('cancel was pressed')

    try:
        file_name = QFileDialog.getOpenFileName(moving_controller.moving_area, 'Open project',
                                                '/PyCharm/pythonProject2', filter='JSON-файлы(*.json)')[0]

        with open(file_name, 'r') as read_file:
            something = json.load(read_file)

    except FileNotFoundError:
        err_msg = QMessageBox()  # сообщение об ошибке
        err_msg.setWindowTitle('Ошибка')
        err_msg.setText('Файл не выбран')
        err_msg.setInformativeText('Выберете существующий файл')
        err_msg.setIcon(QMessageBox.Warning)

        err_msg.setStandardButtons(QMessageBox.Cancel)
        err_msg.setDefaultButton(QMessageBox.Cancel)
        err_msg.setButtonText(QMessageBox.Cancel, 'Закрыть')

        err_msg.exec()  # номер нажатой кнопки
        return 0

    else:
        set_selected_file(file_name)

    clear_action_clicked()

    send_flag = False

    for i in range(len(something['data'])):

        button_text = something['data'][i]['button']

        func_button = SquareXFunction(moving_controller.moving_area)
        func_button.enclosed_dialog.setWindowTitle(button_text)
        func_button.setText(button_text)
        # print(button_text)
        func_button.set_button_name(func_button.enclosed_dialog.windowTitle())

        action_add_function(moving_controller.moving_area, func_button)
        print('in loadig: ', moving_controller.moving_area.buttons)

        move_x = int(something['data'][i]['position'][0]['pos_x'])
        move_y = int(something['data'][i]['position'][0]['pos_y'])
        moving_controller.moving_area.buttons[i].move(move_x, move_y)
        func_button.set_coords(move_x, move_y)

    #     str_send_flag = something['data'][i]['send_flag']
    #     if str_send_flag == 'True':
    #         send_flag = True
    #
    # if send_flag:
    #     i = 0
    #     for button in moving_controller.moving_area.buttons:
    #         str_send_flag = something['data'][i]['send_flag']
    #         print('type of flag: ', type(str_send_flag), str_send_flag)
    #         if str_send_flag == 'True':
    #             button.enclosed_dialog.value_sending_flag.setChecked(True)
    #             recipient = something['data'][i]['send_to']
    #             button.enclosed_dialog.value_sending_block.setText(recipient)
    #
    #             button.click()
    #             button.enclosed_dialog.confirm_button.click()
    #
    #         i += 1

    read_file.close()
    moving_controller.setWindowTitle(
        file_name[((file_name.rfind('/')) + 1):])  # меняем заголовок окна на название нашего файла
    print("Load successful")


# Запуск программы
DB.create_table()
threading.Thread(target=threading_run, daemon=True).start()
app = QApplication(sys.argv)
moving_controller = MovingController()
moving_controller.show()
sys.exit(app.exec())
