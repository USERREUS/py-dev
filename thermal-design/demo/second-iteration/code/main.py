"""
Пока что не структуризированный код
"""

import json
import threading
import time

import PySide6.QtCore

import DB
import sys

from PySide6.QtCore import Qt, QMimeData
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette, QColor, QAction, QIcon, Qt, QDrag, QPixmap
from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QMainWindow, QMessageBox, QFileDialog, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QStyleFactory, QLabel

from area_size import OnLoadSetuper
from buttons import LPHButton, CondButton, WSPButton
from moving_area import MovingArea, SpaceAccess, ButtonsPair  # -#-#-


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
    moving_area.add_btn(button_function)


# Окно, которое включает в себя область движения
class MovingController(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.is_proj_created = False
        self.setFixedSize(1080, 590)

        pal = self.palette()
        # pal.setColor(QPalette.All, QPalette.Window, QColor(240, 240, 240))
        self.setPalette(pal)

        # self.on_load_setuper = OnLoadSetuper()
        # self.on_load_setuper.btn_close.clicked.connect(self.on_load_setuper_close)
        # self.on_load_setuper.btn_ok.clicked.connect(self.setup_division)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("border: 1px solid black; ")

        self.hbox = QHBoxLayout(self)
        self.vbox = QVBoxLayout(self)

        self.header = QFrame(self)
        self.lefttop = QFrame(self)
        self.righttop = QFrame(self)
        # self.window_icon = QFrame(self)
        self.righttop.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        # self.window_icon.setFrameShape(QFrame.StyledPanel)
        # self.window_icon.setStyleSheet("border: none;")
        # self.window_icon.setFrameShadow(QFrame.Raised)
        # self.window_icon.setFixedSize(40, 30)

        # pixmap = QPixmap("images/block.xpm")
        # self.label_icon = QLabel(self.window_icon)
        # self.label_icon.setPixmap(pixmap)
        # self.label_icon.setFixedSize(40, 30)

        # self.window_icon.setStyleSheet(
        #     'background-color: #C7EFDECD; '
        #     'border: 1px solid black; '
        #     'border-right: none; '
        #     'border-bottom: none;'
        #     'padding-right: 5px; '
        #     'padding-left: 5px; '
        # )

        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setStyleSheet("border: none;")
        self.header.setFrameShadow(QFrame.Raised)
        self.header.setFixedSize(self.width(), 30)

        self.lefttop.setFrameShape(QFrame.StyledPanel)
        self.lefttop.setStyleSheet("border: none;")
        self.lefttop.setFrameShadow(QFrame.Raised)
        self.lefttop.setFixedSize(int(self.width() / 2), 30)

        self.righttop.setFrameShape(QFrame.StyledPanel)
        self.righttop.setStyleSheet("border: none;")
        self.righttop.setFrameShadow(QFrame.Raised)
        self.righttop.setFixedSize(int(self.width() / 2), 30)

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setStyleSheet("border: none;")
        self.bottom.setFrameShadow(QFrame.Raised)

        # label_window_hbox = QHBoxLayout(self.header)

        self.label_window_title = QLabel(self.header)
        self.label_window_title.setFixedSize(self.width(), 30)
        self.label_window_title.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 5px; '
            'padding-left: 10px; '
            'font-weight: 600; '
            'font-size: 12px; '
            'border: 1px solid black; '
            'border-top: none; '
            # 'border-right: none; '
        )

        self.set_window_title("Создайте новый или откройте существующий проект в меню 'Файл'")

        # self.set_project_state("")

        # self.label_window_state = QLabel("ожидание...")
        # self.label_window_state.setFixedSize(self.width() - self.lwt_len, 30)
        # self.label_window_state.setStyleSheet(
        #     'background-color: #C7EFDECD; '
        #     'padding: 5px; '
        #     'font: 12px; '
        #     'border: 1px solid black; '
        #     'border-top: none;'
        #     'border-left: none;'
        # )

        # label_window_hbox.setContentsMargins(0, 0, 0, 0)
        # label_window_hbox.setSpacing(0)
        # label_window_hbox.addWidget(self.label_window_title)
        # label_window_hbox.addWidget(self.label_window_state)
        # label_window_hbox.addStretch(1)

        self.menu_bar = QMenuBar(self.lefttop)
        self.create_menu_bar()
        self.menu_bar.setFixedSize(int(self.width() / 2), 30)
        self.menu_bar.mousePressEvent = self.mouse_press
        self.menu_bar.mouseMoveEvent = self.mouse_move

        self.common_actions = QMenuBar(self.righttop)
        self.common_actions.mousePressEvent = self.mouse_press
        self.common_actions.mouseMoveEvent = self.mouse_move

        icon_close = QIcon("images/close.xpm")
        self.common_actions.addAction("X", self.close)
        self.common_actions.actions()[0].setIcon(icon_close)

        icon_full = QIcon("images/full.xpm")
        self.common_actions.addAction("[< >]", self.full_screen)
        self.common_actions.actions()[1].setIcon(icon_full)

        icon_hide = QIcon("images/hide.xpm")
        self.common_actions.addAction("__", self.showMinimized)
        self.common_actions.actions()[2].setIcon(icon_hide)

        self.common_actions.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 5px; '
            'border: 1px solid black; '
            'border-left: none;'
            'border-bottom: none;'
        )

        self.common_actions.setFixedSize(int(self.width() / 2), 30)

        # self.hbox.addWidget(self.window_icon)
        self.hbox.addWidget(self.lefttop)
        self.hbox.addWidget(self.righttop)

        self.moving_area = MovingArea(self.bottom)
        self.moving_area.setDisabled(True)
        self.bottom.setStyleSheet("background-color: #dbd7d3; border-top: none;")
        self.bottom.setFixedSize(self.width(), self.height() - 60)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.header)
        self.vbox.addWidget(self.bottom)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.main_widget.setLayout(self.vbox)

        # QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setWindowFlags(PySide6.QtCore.Qt.FramelessWindowHint)
        # self.setStyleSheet("border: 1px solid black;")


    # def mousePressEvent(self, event:PySide6.QtGui.QMouseEvent) -> None:
    #     print(event.scenePosition().toPoint())

    # def on_load_setuper_close(self):
    #     self.on_load_setuper.close()
    #     self.show()

    def set_project_state(self, state):
        self.label_window_title.setText(f"{self.windowTitle()}: {state}")

    def set_window_title(self, title):
        self.setWindowTitle(title)
        self.label_window_title.setText(self.windowTitle())

    def mouse_press(self, event):
        if self.width() / 2 - 150 < event.scenePosition().x() < self.width() / 2 + 150:
            self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mousePressEvent(self.common_actions, event)
        else:
            QMenuBar.mousePressEvent(self.menu_bar, event)

    def mouse_move(self, event):
        if not self.isFullScreen():
            if self.width() / 2 - 150 < event.scenePosition().x() < self.width() / 2 + 150:
                if event.buttons() == Qt.LeftButton:
                    new_pos = self.pos() + event.globalPosition().toPoint() - self.click_position
                    self.move(new_pos)
                    self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mouseMoveEvent(self.common_actions, event)
        else:
            QMenuBar.mouseMoveEvent(self.menu_bar, event)

    def setup_division(self):
        self.moving_area.partition = SpaceAccess(self.moving_area.width(), self.moving_area.height(), 5, 5)
        self.moving_area.vert_parts = self.moving_area.hor_parts = 5

    def closeEvent(self, event):

        ackn = QMessageBox(
            QMessageBox.Question,
            "Подтверждение закрытия окна",
            "Вы действительно хотите закрыть рабочее окно?"
        )

        ackn.addButton("&НЕТ", QMessageBox.NoRole)
        yes = ackn.addButton("&ДА", QMessageBox.YesRole)
        ackn.setDefaultButton(yes)
        result = ackn.exec()

        if result == QMessageBox.Accepted:
            for button in self.moving_area.buttons:
                button.enclosed_dialog.close()
                button.manual_calc_dialog.close()
                # button.cmp_dialog.close()
                if button.info:
                    button.info.close()
                button.graph.close()
            # self.on_load_setuper.close()
            event.accept()
            QWidget.closeEvent(self, event)
        else:
            event.ignore()

    # Метод создания главного меню
    def create_menu_bar(self):
        self.functions_menu = QMenu("Функции", self)
        self.file_menu = QMenu("Файл", self)
        self.debug_menu = QMenu("Отладка", self)
        # self.size_menu = QMenu("Размер", self)

        self.menu_bar.addMenu(self.file_menu)
        # self.menu_bar.addMenu(self.size_menu)
        self.menu_bar.addMenu(self.functions_menu)
        self.menu_bar.addMenu(self.debug_menu)

        self.menu_bar.addAction("Расчет", try_threading_run)
        # self.menu_bar.actions()[3].setIcon(QIcon("images/run.xpm"))
        self.menu_bar.addAction("Стоп", threading_run_stop)
        # self.menu_bar.actions()[4].setIcon(QIcon("images/stop.xpm"))
        self.menu_bar.actions()[4].setVisible(False)

        for action in self.menu_bar.actions():
            if action.text() != "Файл":
                action.setEnabled(False)

        self.functions_menu.addAction("Подогреватель", self.lph_clicked)
        self.functions_menu.addAction("Конденсатор", self.cond_clicked)
        self.functions_menu.addAction("Турбина", self.wsp_clicked)

        self.file_menu.addAction("Открыть", load)  #
        self.file_menu.addAction("Создать", self.create_new_proj)  #
        self.file_menu.addAction("Сохранить", save)  #
        self.file_menu.addAction("Сохранить как...", save_as)  #
        self.file_menu.addAction("Очистить", clear_action_clicked)

        for action in self.file_menu.actions():
            if action.text() != "Открыть" and action.text() != "Создать":
                action.setEnabled(False)

        self.debug_menu.addAction("Добавить запись в БД", DB.insert_random_data)
        self.debug_menu.addAction("Очистить БД", self.clear_db_action)

        # self.size_menu.addAction("2 x 2", self.set_new_size)
        # self.size_menu.addAction("3 x 3", self.set_new_size)
        # self.size_menu.addAction("4 x 4", self.set_new_size)
        # self.size_menu.addAction("5 x 5", self.set_new_size)
        # self.size_menu.addAction("6 x 6", self.set_new_size)

        # for action in self.size_menu.actions():
        #     action.setIcon(QIcon("images/ok.xpm"))
        #     action.setIconVisibleInMenu(False)

        self.menu_bar.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 5px; '
            'border: 1px solid black; '
            'border-bottom: none;'
            'border-right: none; '
        )

    # # Установка текущего размера в заголовке
    # def set_active_size(self):
    #     i = self.moving_area.vert_parts - 2
    #     for j in range(len(self.size_menu.actions())):
    #         if i == j:
    #             self.size_menu.actions()[j].setIconVisibleInMenu(True)
    #         else:
    #             self.size_menu.actions()[j].setIconVisibleInMenu(False)

    def clear_db_action(self):
        ackn = QMessageBox(
            QMessageBox.Warning,
            "Очистка базы данных",
            "Данное действие приведет к удалению всех записей в базе данных. Продолжить?"
        )
        ackn.setInformativeText("Не рекомендуется выполнять без необходимости.")

        no = ackn.addButton("&НЕТ", QMessageBox.NoRole)
        ackn.addButton("&ДА", QMessageBox.YesRole)
        ackn.setDefaultButton(no)
        result = ackn.exec()

        if result == QMessageBox.Accepted:
            DB.clear_all_data()

    # # Обработчик события выбора пункта меню (конкретно вызываемой функции)
    # @QtCore.Slot()
    # def action_clicked(self):
    #     action = self.sender()
    #     # print(action)
    #
    #     if action.text() == "&Подогреватель":
    #         print("Action : " + action.text())
    #         action_func_lph(moving_controller.moving_area)
    #
    #     elif action.text() == "&Конденсатор":
    #         print("Action : " + action.text())
    #         action_func_cond(moving_controller.moving_area)
    #
    #     elif action.text() == "&Турбина":
    #         print("Action : " + action.text())
    #         action_func_wsp(moving_controller.moving_area)

    # def set_new_size(self):
    #     action = self.sender()
    #     size = int(action.text()[0])
    #     max_size = 0
    #     for button in self.moving_area.buttons:
    #         i, j = button.space_access_indexes
    #         x = max(i + 1, j + 1)
    #         if x > max_size:
    #             max_size = x
    #     if size >= max_size:
    #         self.moving_area.hor_parts = self.moving_area.vert_parts = size
    #         self.set_active_size()
    #         self.moving_area.resizing()
    #     else:
    #         QMessageBox.information(
    #             self,
    #             "Измерение размерности поля",
    #             "Для изменения необходимо привести схему к матричному виду требуемой размерности "
    #             "(переместить или удалить блок(и)).",
    #             buttons=QMessageBox.Ok,
    #             defaultButton=QMessageBox.Ok)

    def full_screen(self):
        for action in self.common_actions.actions():
            if action.text() == "[< >]":
                action.setText("[> <]")
                action.setIcon(QIcon("images/minimize.xpm"))
                self.showFullScreen()
                # self.label_window_state.setFixedSize(self.width(), 30)
                self.label_window_title.setFixedSize(self.width(), 30)
                self.header.setFixedSize(self.width(), 30)
                self.lefttop.setFixedSize(int(self.width() / 2), 30)
                self.righttop.setFixedSize(int(self.width() / 2), 30)
                self.bottom.setFixedSize(self.width(), self.height() - 60)
                self.menu_bar.setFixedSize(int(self.width() / 2), 30)
                self.common_actions.setFixedSize(int(self.width() / 2), 30)
                self.moving_area.resize(self.width(), self.height() - 60)
                self.moving_area.resizing()
            elif action.text() == "[> <]":
                action.setText("[< >]")
                action.setIcon(QIcon("images/full.xpm"))
                self.showNormal()
                # self.label_window_state.setFixedSize(self.width(), 30)
                self.label_window_title.setFixedSize(self.width(), 30)
                self.header.setFixedSize(self.width(), 30)
                self.lefttop.setFixedSize(int(self.width() / 2), 30)
                self.righttop.setFixedSize(int(self.width() / 2), 30)
                self.bottom.setFixedSize(self.width(), self.height() - 60)
                self.menu_bar.setFixedSize(int(self.width() / 2), 30)
                self.common_actions.setFixedSize(int(self.width() / 2), 30)
                self.moving_area.resize(self.width(), self.height() - 60)
                self.moving_area.resizing()

    def create_new_proj(self):
        if moving_controller.is_proj_created:
            ackn = QMessageBox(
                QMessageBox.Question,
                "Подтверждение создания нового проекта",
                "Несохраненные данные будут утрачены. Хотите сохранить текущий проект?"
            )

            ackn.addButton(QMessageBox.Cancel)
            ackn.addButton(QMessageBox.No)
            yes = ackn.addButton(QMessageBox.Yes)
            ackn.setDefaultButton(yes)

            ackn.buttons()[2].setText("НЕТ")
            ackn.buttons()[1].setText("ДА")
            ackn.buttons()[0].setText("НАЗАД")

            result = ackn.exec()

            if result == QMessageBox.Cancel:
                return

            if result == QMessageBox.Yes:
                save()  # -#-#-

        self.moving_area.setEnabled(True)
        self.bottom.setStyleSheet("background-color: #ebe7e3; border-top: none;")

        for action in self.menu_bar.actions():
            if action.text() != "Стоп":
                action.setEnabled(True)

        for action in self.file_menu.actions():
            action.setEnabled(True)

        deleted_buttons = 0
        for i in range(len(moving_controller.moving_area.buttons)):
            moving_controller.moving_area.buttons[i - deleted_buttons].clear_object()
            deleted_buttons += 1
        LPHButton.static_num = WSPButton.static_num = CondButton.static_num = 0
        self.setup_division()
        self.set_window_title("Новый проект")
        self.set_project_state("режим редактирования")
        self.is_proj_created = True
        moving_controller.moving_area.printing()

    def lph_clicked(self):  # -#-#-
        # if not self.moving_area.isEnabled():
        #     self.check_area_enable()
        # else:
        func_lph_button = LPHButton(self.moving_area)
        action_add_function(self.moving_area, func_lph_button)

    def cond_clicked(self):  # -#-#-
        # if not self.moving_area.isEnabled():
        #     self.check_area_enable()
        # else:
        func_cond_button = CondButton(self.moving_area)
        action_add_function(self.moving_area, func_cond_button)

    def wsp_clicked(self):  # -#-#-
        # if not self.moving_area.isEnabled():
        #     self.check_area_enable()
        # else:
        func_wsp_button = WSPButton(self.moving_area)
        action_add_function(self.moving_area, func_wsp_button)

    # def check_area_enable(self):
    #     ackn = QMessageBox(
    #         QMessageBox.Information,
    #         "Создание нового проекта",
    #         "Для вызова функций необходимо создать новый проект."
    #     )
    #
    #     ackn.addButton("&Назад", QMessageBox.NoRole)
    #     yes = ackn.addButton("&Создать", QMessageBox.YesRole)
    #     ackn.setDefaultButton(yes)
    #     result = ackn.exec()
    #
    #     if result == QMessageBox.Accepted:
    #         self.create_new_proj()


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
    ackn = QMessageBox(
        QMessageBox.Question,
        "Подтверждение очистки рабочей области",
        "Вы действительно хотите очистить рабочую область?"
    )
    ackn.setInformativeText("Все объекты рабочей области будут удалены")

    ackn.addButton("&НЕТ", QMessageBox.NoRole)
    yes = ackn.addButton("&ДА", QMessageBox.YesRole)
    ackn.setDefaultButton(yes)
    result = ackn.exec()

    if result == QMessageBox.Accepted:
        deleted_buttons = 0
        for i in range(len(moving_controller.moving_area.buttons)):
            moving_controller.moving_area.buttons[i - deleted_buttons].clear_object()
            deleted_buttons += 1
        LPHButton.static_num = WSPButton.static_num = CondButton.static_num = 0
        moving_controller.moving_area.printing()


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


def try_threading_run():
    if len(moving_controller.moving_area.buttons) == 0:
        QMessageBox.warning(
            None,
            "Ошибка расчета",
            "Нечего считать. Расположите блоки на рабочей области.",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok
        )
        return
    for button in moving_controller.moving_area.buttons:
        if button.enclosed_dialog.value_sending_flag.isChecked():
            QMessageBox.warning(
                None,
                "Ошибка расчета",
                "В данных момент расчет с передачей данных между блоками недоступен. =(",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok
            )
            return
    moving_controller.menu_bar.actions()[3].setVisible(False)
    moving_controller.menu_bar.actions()[4].setVisible(True)
    moving_controller.set_project_state("расчет схемы")
    threading_run_start()


def threading_run_start():
    global treading_live
    treading_live = True
    for action in moving_controller.menu_bar.actions():
        if action.text() == "Стоп":
            action.setEnabled(True)
        elif action.text() != "Отладка":
            action.setEnabled(False)
    moving_controller.moving_area.setAcceptDrops(False)


def threading_run_stop():
    global treading_live
    treading_live = False
    for action in moving_controller.menu_bar.actions():
        if action.text() == "Стоп":
            action.setEnabled(False)
        else:
            action.setEnabled(True)
    moving_controller.menu_bar.actions()[3].setVisible(True)
    moving_controller.menu_bar.actions()[4].setVisible(False)
    moving_controller.set_project_state("режим редактирования")
    moving_controller.moving_area.setAcceptDrops(True)


# Старт вычислений
def run():
    print("START method: run() _______________________")  # отладочная информация
    # print("Connecton depth: ", depth_of_connection())

    # try:
    for button in moving_controller.moving_area.buttons:
        # if not moving_controller.moving_area.is_in_logic_cp(button):
        print("Calculation button: ", button.text())
        button.calculate_db()

    # list_temp = []  # решение проблемы повторного расчета
    # noc = depth_of_connection()
    # while True:
    #     flag = False
    #     for pair in moving_controller.moving_area.logic_connected_pair:
    #         print("Calc pair", pair.btnl.text(), pair.btnr.text())
    #         if pair.btnl.value is not None:
    #             if pair.btnl in list_temp:
    #                 list_temp.remove(pair.btnl)
    #             pair.btnl.calculate_db()
    #             # result = pair.btnl.evaluate_db()
    #             if pair.btnl.enclosed_dialog.value_sending_flag.isChecked():
    #                 # pair.btnr.value = result
    #                 # list_temp.append(pair.btnr)
    #                 pass
    #         else:
    #             flag = True
    #     noc -= 1
    #     if not flag or noc <= 0:
    #         for btn in list_temp:
    #             # btn.add_value_db()
    #             # btn.evaluate_db()
    #             btn.calculate_db()
    #         break

    # except Exception as exc:
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Ошибка расчета!")
    #     msg.setText(exc.__str__())
    #     msg.setIcon(QMessageBox.Critical)
    #
    #     msg.exec()
    #
    # finally:
    print("END method: run() _______________________")


# -#-#-
# ------------------------------
# сохранить как
def save_as():
    file_name = \
    QFileDialog.getSaveFileName(moving_controller.moving_area, 'Сохранить проект', '/PyCharm/pythonProject2',
                                filter='*.json')[0]
    if file_name == '':
        return 0

    set_selected_file(file_name)

    common_save(file_name)

    moving_controller.set_window_title(
        file_name[((file_name.rfind('/')) + 1):])  # меняем заголовок окна на название нашего файла
    moving_controller.set_project_state("режим редактирования")
    print('in saving: ', moving_controller.moving_area.buttons)
    print("Saved us")


# сохранить
def save():
    file_name = get_selected_file()

    if file_name == '':
        save_as()
    else:
        common_save(file_name)

        print('in saving: ', moving_controller.moving_area.buttons)
        print("Saved")


# -#-#-
# общая функция загрузки
def common_save(file_name: str):
    m = 1
    with open(file_name, 'w+', encoding='utf-8') as first_try:
        first_try.write(f'{{\n  "hor_parts": "5",\n'
                        f'  "vert_parts": "5",\n')

        # first_try.write(f'{{\n  "hor_parts": "{moving_controller.moving_area.hor_parts}",\n'
        #                 f'  "vert_parts": "{moving_controller.moving_area.vert_parts}",\n')

        left_list = []
        right_list = []
        if len(moving_controller.moving_area.logic_connected_pair) != 0:
            # print('length of logic_connected_pair: ', len(moving_controller.moving_area.logic_connected_pair))
            for pair in moving_controller.moving_area.logic_connected_pair:
                right_button_index = moving_controller.moving_area.buttons.index(pair.btnr)
                right_list.append(right_button_index)
                print('index of right button: ', right_button_index)

                left_button_index = moving_controller.moving_area.buttons.index(pair.btnl)
                left_list.append(left_button_index)
                print('index of left button: ', left_button_index)

        print('left_list: ', left_list)
        print('right_list: ', right_list)

        # сохраняем список левых кнопок в парах
        k = 1
        first_try.write(f'  "left_list": [\n')
        for i in range(len(left_list)):
            first_try.write(f'    "{left_list[i]}"')
            k += 1
            if len(left_list) >= k:
                first_try.write(',\n')
        first_try.write(f'  ],\n')

        # сохраняем список правых кнопок в парах
        k = 1
        first_try.write(f'  "right_list": [\n')
        for i in range(len(right_list)):
            first_try.write(f'    "{right_list[i]}"')
            k += 1
            if len(right_list) >= k:
                first_try.write(',\n')
        first_try.write(f'  ],\n')

        first_try.write('  "data": [\n')

        j = 0
        for button in moving_controller.moving_area.buttons:
            # сохраняем флажок передачи данных
            if button.enclosed_dialog.value_sending_flag.isChecked():
                button.set_send_flag(True)

            # сохраняем id блоков
            button.set_button_id(j)

            # сохраняем общую информацию о блоке
            json.dump({
                "id": f"{button.get_button_id()}",
                "type": f"{button.get_button_type()}",
                "button": f"{button.get_button_name()}",
                "position": [
                    {
                        "pos_x": f"{button.get_coords()[0]}",
                        "pos_y": f"{button.get_coords()[1]}"
                    }
                ],
                "send_flag": f"{button.get_send_flag()}",
                # "send_to": f"{button.get_send_to()}"
            }
                , first_try, indent=4)

            m += 1
            j += 1
            if len(moving_controller.moving_area.buttons) >= m:
                first_try.write(',\n')

            print(f'Имя кнопки: {button.get_button_name()}')

        first_try.write('\n ]\n}')
    first_try.close()


# загрузить/открыть
def load():
    if moving_controller.is_proj_created:
        ackn = QMessageBox(
            QMessageBox.Question,
            "Подтверждение открытия проекта",
            "Несохраненные данные будут утрачены. Хотите сохранить текущий проект?"
        )

        ackn.addButton(QMessageBox.Cancel)
        ackn.addButton(QMessageBox.No)
        yes = ackn.addButton(QMessageBox.Yes)
        ackn.setDefaultButton(yes)

        ackn.buttons()[2].setText("НЕТ")
        ackn.buttons()[1].setText("ДА")
        ackn.buttons()[0].setText("НАЗАД")

        result = ackn.exec()

        if result == QMessageBox.Cancel:
            return

        if result == QMessageBox.Yes:
            save()  # -#-#-

    try:
        file_name = QFileDialog.getOpenFileName(moving_controller.moving_area, 'Открыть проект',
                                                '/PyCharm/pythonProject2', filter='JSON-файлы(*.json)')[0]

        with open(file_name, 'r') as read_file:
            something = json.load(read_file)

    except FileNotFoundError:
        err_msg = QMessageBox()  # сообщение об ошибке
        err_msg.setWindowTitle('Ошибка')
        err_msg.setText('Файл не выбран.')
        err_msg.setInformativeText('Выберите существующий файл.')
        err_msg.setIcon(QMessageBox.Warning)

        err_msg.setStandardButtons(QMessageBox.Cancel)
        err_msg.setDefaultButton(QMessageBox.Cancel)
        err_msg.setButtonText(QMessageBox.Cancel, 'Закрыть')

        err_msg.exec()  # номер нажатой кнопки
        return 0

    else:
        set_selected_file(file_name)

    # создание рабочей области
    moving_controller.moving_area.partition = SpaceAccess(moving_controller.moving_area.width(),
                                                          moving_controller.moving_area.height(),
                                                          int(something['hor_parts']),
                                                          int(something['vert_parts']))
    moving_controller.moving_area.vert_parts = int(something['vert_parts'])
    moving_controller.moving_area.hor_parts = int(something['hor_parts'])

    moving_controller.moving_area.setEnabled(True)
    moving_controller.bottom.setStyleSheet("background-color: #ebe7e3; border-top: none;")

    for action in moving_controller.menu_bar.actions():
        if action.text() != "Стоп":
            action.setEnabled(True)

    for action in moving_controller.file_menu.actions():
        action.setEnabled(True)

    deleted_buttons = 0
    for i in range(len(moving_controller.moving_area.buttons)):
        moving_controller.moving_area.buttons[i - deleted_buttons].clear_object()
        deleted_buttons += 1
    LPHButton.static_num = WSPButton.static_num = CondButton.static_num = 0

    moving_controller.set_window_title(
        file_name[((file_name.rfind('/')) + 1):])  # меняем заголовок окна на название нашего файла
    moving_controller.set_project_state("режим редактирования")
    moving_controller.show()

    send_flag = False  # передача данных

    # создание кнопок
    for i in range(len(something['data'])):  # -#-#-
        # определяем, есть ли флажок передачи данных
        str_send_flag = something['data'][i]['send_flag']
        if str_send_flag == 'True':
            send_flag = True

        # определяем тип блока
        func_type = something['data'][i]['type']

        if func_type == 'LPH':
            func_button = LPHButton(moving_controller.moving_area)
            load_for_all(something, func_button, i)
        elif func_type == 'Cond_red':
            func_button = CondButton(moving_controller.moving_area)
            load_for_all(something, func_button, i)
        elif func_type == 'WSP':
            func_button = WSPButton(moving_controller.moving_area)
            load_for_all(something, func_button, i)

    for i in range(len(something['left_list'])):
        print('i = ', i)
        left_button_id = int(something['left_list'][i])
        right_button_id = int(something['right_list'][i])

        pair = ButtonsPair()
        pair.set_btnl(moving_controller.moving_area.buttons[left_button_id])
        pair.set_btnr(moving_controller.moving_area.buttons[right_button_id])
        moving_controller.moving_area.logic_connected_pair.append(pair)
        moving_controller.moving_area.printing()

    # если встретился хоть один установленный флажок
    if send_flag:
        i = 0
        for button in moving_controller.moving_area.buttons:
            str_send_flag = something['data'][i]['send_flag']

            if str_send_flag == 'True':
                button.enclosed_dialog.value_sending_flag.setChecked(True)

            i += 1

    read_file.close()
    # moving_controller.setWindowTitle(
    #     file_name[((file_name.rfind('/')) + 1):])  # меняем заголовок окна на название нашего файла

    moving_controller.is_proj_created = True

    print("Load successful")


# общие действия при загрузке всех блоков
def load_for_all(load_source, function_button, counter: int):  # -#-#-
    i = counter
    button_id = load_source['data'][i]['id']
    function_button.set_button_id(button_id)
    button_text = load_source['data'][i]['button']
    function_button.setText(button_text)  # -#-#-
    # function_button.setTextWithResize(button_text)
    function_button.set_button_name(function_button.text())

    moving_controller.moving_area.buttons.append(function_button)
    function_button.show()
    # action_add_function(moving_controller.moving_area, function_button)
    print('in loadig: ', moving_controller.moving_area.buttons)

    move_x = int(load_source['data'][i]['position'][0]['pos_x'])
    move_y = int(load_source['data'][i]['position'][0]['pos_y'])
    function_button.set_coords(move_x, move_y)
    moving_controller.moving_area.partition.place_button_resizing(function_button)
# ------------------------------


# Запуск программы
thread = threading.Thread(target=threading_run, daemon=True)
thread.start()
app = QApplication(sys.argv)
moving_controller = MovingController()
moving_controller.show()
sys.exit(app.exec())
