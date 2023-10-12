import sys
import save_and_load

from PyQt6 import QtCore
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMenu, QMenuBar, QApplication, QVBoxLayout, QLabel, QWidget

from login import LoginDialog
from mvc import Controller, View, Model
from main_interfaces import BlockModelType, WorkMode, IMainWindow


class ThreadProcess(QtCore.QThread):
    """
    Класс потока расчета
    """
    def __init__(self, method) -> None:
        """
        Инициализация объекта потока.
        :param method: метод, который будет выполняться в потоке.
        """
        super().__init__()
        self.running = False  # Флаг выполнения
        self.method = method

    def run(self) -> None:
        """
        Запуск выполнения потока.
        """
        self.running = True
        while self.running:  # Проверяем значение флага
            self.method()
            self.msleep(500)  # Имитируем процесс


class WorkArea(QWidget):
    """
    Класс, представляющий рабочую область.
    """
    def __init__(self, view: View):
        """
        Инициализация рабочей области.
        :param view: объект View для отображения на рабочей области.
        """
        super().__init__()
        # Создаем метку и устанавливаем текст
        self.__status_label = QLabel()
        self.__status_label.setText("режим работы: редактирование...")
        # Создаем вертикальный контейнер, добавляем наши элементы управления
        v_box = QVBoxLayout()
        v_box.addWidget(view)
        v_box.addWidget(self.__status_label)
        # Устанавливаем вертикальный контейнер как основной
        self.setLayout(v_box)

    def set_text(self, text):
        """
        Устанавливает текст метки статуса.
        :param text: текст для установки.
        """
        self.__status_label.setText(text)


class MainWnd(IMainWindow):
    """
    Класс, представляющий главное окно проекта.
    """
    def __init__(self, user_mode: int = 0):
        """
        Инициализация главного окна проекта.
        :param user_mode: режим пользователя.
        """
        super().__init__()
        self.__user_mode: int = user_mode
        self.__scene = Controller()
        self.__model = Model()
        self.__view = View()
        self.__work_area = WorkArea(self.__view)
        self.__functions_menu: QMenu = None
        self.__file_menu: QMenu = None
        self.__debug_menu: QMenu = None
        self.__work_mode_menu: QMenu = None
        self.__menu_bar: QMenuBar = None
        self.__title = "Тестовый проект"
        self.__mythread = ThreadProcess(self.__scene.process_model)

        self.__scene.set_model(self.__model)
        self.__scene.set_view(self.__view)

        self.setCentralWidget(self.__work_area)
        self.setWindowTitle(self.__title)

        if user_mode == 1:
            self.setWindowTitle(f'{self.__title}: Администратор')

        self.create_menu_bar()
        self.set_edit_mode()
        self.show()

    def get_scene(self) -> Controller:
        """
        Возвращает объект сцены.
        :return: объект сцены.
        """
        return self.__scene

    def create_menu_bar(self) -> None:
        """
        Метод для создания главного меню.
        """
        self.__functions_menu = QMenu("Блоки", self)
        self.__functions_menu.addAction("Генератор", self.add_gen)
        self.__functions_menu.addAction("Расчетный блок", self.add_clc)
        self.__functions_menu.addAction("Отображение", self.add_out)

        self.__file_menu = QMenu("Файл", self)
        self.__file_menu.addAction("Открыть", self.open)  #
        if self.__user_mode == 1:
            self.__file_menu.addAction("Создать")  #
            self.__file_menu.addAction("Сохранить", self.save)  #
            self.__file_menu.addAction("Сохранить как...")  #
            self.__file_menu.addAction("Очистить", self.clear)

        self.__debug_menu = QMenu("Отладка", self)
        self.__debug_menu.addAction("Показать модель задачи", self.print_model)

        self.__work_mode_menu = QMenu("Режим работы", self)
        self.__work_mode_menu.addAction("Редактирование", self.set_edit_mode)
        self.__work_mode_menu.addAction("Удаление", self.set_del_mode)

        self.__menu_bar = QMenuBar()
        self.setMenuBar(self.__menu_bar)
        self.__menu_bar.addMenu(self.__file_menu)
        if self.__user_mode == 1:
            self.__menu_bar.addMenu(self.__functions_menu)
            self.__menu_bar.addMenu(self.__debug_menu)
            self.__menu_bar.addMenu(self.__work_mode_menu)
        self.__menu_bar.addAction("Расчет", self.on_start)
        self.__menu_bar.addAction("Стоп", self.on_stop)

    def save(self) -> None:
        """
        Метод сохранения данных.
        """
        save_and_load.scene_save(self.__scene)

    def open(self) -> None:
        """
        Метод открытия данных.
        """
        save_and_load.file_open(self)

    def clear(self) -> None:
        """
        Метод очистки данных.
        """
        self.__scene.clear()

    def set_clc_mode(self, msg: str) -> None:
        """
        Установка режима работы "расчет".
        :param msg: сообщение для отображения.
        """
        self.__work_area.set_text("режим работы: расчет... " + msg)
        self.__scene.set_work_mode(WorkMode.process)

    def set_del_mode(self) -> None:
        """
        Установка режима работы "удаление".
        """
        self.__work_area.set_text('режим работы: удаление...')
        self.__scene.set_work_mode(WorkMode.delete)

    def set_edit_mode(self) -> None:
        """
        Установка режима работы "редактирование".
        """
        self.__work_area.set_text('режим работы: редактирование...')
        self.__scene.set_work_mode(WorkMode.edit)

    def add_gen(self) -> None:
        """
        Добавление генератора.
        """
        self.__scene.set_work_mode(WorkMode.adding)
        self.__scene.set_adding_block(BlockModelType.generator)

    def add_clc(self) -> None:
        """
        Добавление расчетного блока.
        """
        self.__scene.set_work_mode(WorkMode.adding)
        self.__scene.set_adding_block(BlockModelType.calculator)

    def add_out(self) -> None:
        """
        Добавление блока отображения.
        """
        self.__scene.set_work_mode(WorkMode.adding)
        self.__scene.set_adding_block(BlockModelType.display)

    def on_start(self) -> None:
        """
        Обработчик события "Расчет".
        """
        if not self.__mythread.isRunning():
            flag, msg = self.__scene.is_ready_to_calc()
            self.set_clc_mode(msg)
            if flag:
                self.__mythread.start()  # Запускаем поток

    def on_stop(self) -> None:
        """
        Обработчик события "Стоп".
        """
        self.set_edit_mode()
        self.__mythread.running = False  # Изменяем флаг выполнения

    def on_close(self, event: QCloseEvent) -> None:
        """
        Обработчик события "Закрытие окна".
        """
        self.hide()  # Скрываем окно
        self.__mythread.running = False  # Изменяем флаг выполнения
        self.__mythread.wait(5000)  # Даем время, чтобы закончить
        event.accept()  # Закрываем окно

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Обработчик события "Закрытие окна".
        """
        self.on_close(event)

    def print_model(self) -> None:
        """
        Вывод модели задачи.
        """
        print("-------------------------Print Schema Graph----------------")
        self.__scene.print_model()
        print("-------------------------End print-------------------------")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    result = LoginDialog().exec()
    if result:
        main_window = MainWnd(result)
        sys.exit(app.exec())
