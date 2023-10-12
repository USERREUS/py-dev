import enum
from abc import abstractmethod
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QLineF
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsRectItem, \
    QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QMainWindow, QMenuBar


# Перечисление режимов работы
class WorkMode(enum.Enum):
    edit = 0  # редактирование
    delete = 1  # удаление
    process = 2  # расчет
    adding = 3  # добавление


# Перечисление моделей блоков
class BlockModelType(enum.Enum):
    generator = 0  # генератор
    calculator = 1  # расчетный блок
    display = 2  # блок отображения


# Определение интерфейса для графического блока
class IBlockGfx(QGraphicsRectItem):
    @abstractmethod
    def get_noi(self) -> int:
        pass

    @abstractmethod
    def get_noo(self) -> int:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_model_type(self) -> BlockModelType:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_connector(self) -> 'IConnector':
        pass

    @abstractmethod
    def model_process(self, data: dict) -> dict:
        """
        Обрабатывает данные модели блока.
        :param data: данные модели блока в виде словаря.
        :return: результат обработки данных модели блока в виде словаря.
        """
        pass

    @abstractmethod
    def exceeding_the_boundaries(self, new_x: int, new_y: int) -> bool:
        """
        Проверка на выход за границы рабочей области.
        :param new_x: новая коррдината x.
        :param new_y: новая координата y.
        :return: результат проверка на выход за границы.
        """
        pass

    @abstractmethod
    def on_bounding_rect(self) -> QtCore.QRectF:
        """
        Возвращает ограничивающий прямоугольник блока.
        :return: ограничивающий прямоугольник блока.
        """
        pass

    @abstractmethod
    def detect_collision(self) -> bool:
        """
        Проверяет наличие коллизии с другими объектами.
        :return: True, если есть коллизия; False в противном случае.
        """
        pass

    @abstractmethod
    def move_connector(self) -> None:
        """
        Перемещение соединителя.
        """
        pass

    @abstractmethod
    def on_foreground(self) -> None:
        """
        Обрабатывает событие перевода блока в передний план.
        """
        pass

    @abstractmethod
    def on_background(self) -> None:
        """
        Обрабатывает событие перевода блока в задний план.
        """
        pass

    @abstractmethod
    def on_press(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обрабатывает событие нажатия кнопки мыши на блоке.
        :param event: объект события нажатия кнопки мыши.
        """
        pass

    @abstractmethod
    def on_move(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обрабатывает событие перемещения мыши на блоке.
        :param event: объект события перемещения мыши.
        """
        pass

    @abstractmethod
    def on_release(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обрабатывает событие отпускания кнопки мыши на блоке.
        :param event: объект события отпускания кнопки мыши.
        """
        pass

    @abstractmethod
    def draw_triangles(self) -> None:
        """
        Рисует треугольники на блоке.
        """
        pass


# Определение интерфейса для графической сцены
class IScene(QGraphicsScene):
    @abstractmethod
    def set_adding_block(self, block_type: BlockModelType) -> None:
        """
        Устанавливает тип блока, который будет добавлен на сцену.
        :param block_type: тип блока для добавления.
        """
        pass

    @abstractmethod
    def set_model(self, model: 'IModel') -> None:
        """
        Устанавливает модель для сцены.
        :param model: модель для сцены.
        """
        pass

    @abstractmethod
    def is_ready_to_calc(self) -> (bool, str):
        """
        Проверяет готовность к расчету.
        :return: кортеж (bool, str) - True и пустую строку, если готовность к расчету;
                 False и сообщение об ошибке в противном случае.
        """
        pass

    @abstractmethod
    def create_link(self, src: int, dst: int) -> None:
        """
        Создает связь между блоками на сцене.
        :param src: идентификатор исходного блока.
        :param dst: идентификатор целевого блока.
        """
        pass

    @abstractmethod
    def set_work_mode(self, mode: WorkMode) -> None:
        """
        Устанавливает режим работы сцены.
        :param mode: режим работы сцены.
        """
        pass

    @abstractmethod
    def process_model(self) -> None:
        """
        Обрабатывает модель.
        """
        pass

    @abstractmethod
    def print_model(self) -> None:
        """
        Печатает модель.
        """
        pass

    @abstractmethod
    def get_blocks(self) -> [IBlockGfx]:
        """
        Возвращает список блоков на сцене.
        :return: список блоков на сцене.
        """
        pass

    @abstractmethod
    def remove_links(self, id: int) -> None:
        """
        Удаляет связи, связанные с указанным идентификатором блока.
        :param id: идентификатор блока.
        """
        pass

    @abstractmethod
    def create_block(self, x: int, y: int) -> IBlockGfx:
        """
        Создает блок на сцене с указанными координатами.
        :param x: координата X для создания блока.
        :param y: координата Y для создания блока.
        :return: созданный блок.
        """
        pass

    @abstractmethod
    def add_block(self, block: IBlockGfx) -> None:
        """
        Добавляет блок на сцену.
        :param block: блок для добавления на сцену.
        """
        pass

    @abstractmethod
    def block_by_id(self, id: int) -> IBlockGfx:
        """
        Возвращает блок на сцене по указанному идентификатору.
        :param id: идентификатор блока.
        :return: блок на сцене.
        """
        pass

    @abstractmethod
    def draw_grid(self) -> None:
        """
        Рисует сетку на графической сцене.
        """
        pass


# Интерфейс подвижного блока соединителя
class ILink(QGraphicsLineItem):
    @abstractmethod
    def get_connector(self) -> 'IConnector':
        pass


class IConnector(QGraphicsEllipseItem):
    @abstractmethod
    def get_destination(self) -> IBlockGfx:
        pass

    @abstractmethod
    def remove_links(self):
        """
        Удаляет все связи, связанные с данным коннектором.
        """

    @abstractmethod
    def on_press(self, event: 'QGraphicsSceneMouseEvent'):
        """
        Обрабатывает событие нажатия кнопки мыши.
        :param event: объект события нажатия кнопки мыши.
        """

    @abstractmethod
    def on_move(self, event: 'QGraphicsSceneMouseEvent'):
        """
        Обрабатывает событие перемещения мыши.
        :param event: объект события перемещения мыши.
        """

    @abstractmethod
    def on_release(self, event: 'QGraphicsSceneMouseEvent'):
        """
        Обрабатывает событие отпускания кнопки мыши.
        :param event: объект события отпускания кнопки мыши.
        """

    @abstractmethod
    def detect_collision(self) -> bool:
        """
        Проверяет наличие коллизии с другими объектами.
        :return: True, если есть коллизия; False в противном случае.
        """

    @abstractmethod
    def move_connector(self, x_cnew, y_cnew):
        """
        Перемещает коннектор в новые координаты.
        :param x_cnew: новая координата по оси X.
        :param y_cnew: новая координата по оси Y.
        """

    @abstractmethod
    def is_complete_link_possible(self):
        """
        Проверяет, возможно ли завершить связь с данным коннектором.
        """

    @abstractmethod
    def link_complete(self):
        """
        Завершает связь с данным коннектором.
        """

    @abstractmethod
    def set_base_color(self):
        """
        Устанавливает базовый цвет для коннектора.
        """

    @abstractmethod
    def set_collision_color(self):
        """
        Устанавливает цвет при коллизии с другим объектом.
        """

    @abstractmethod
    def set_complete_color(self):
        """
        Устанавливает цвет при завершении связи.
        """

    @abstractmethod
    def set_color(self, r, g, b, a=0):
        """
        Устанавливает цвет для коннектора.
        :param r: значение красного цвета (от 0 до 255).
        :param g: значение зеленого цвета (от 0 до 255).
        :param b: значение синего цвета (от 0 до 255).
        :param a: значение альфа-канала (от 0 до 255), по умолчанию 0.
        """

    @abstractmethod
    def is_dst_complete(self) -> bool:
        pass

    @abstractmethod
    def get_links(self) -> [ILink]:
        pass


# Интерфейс класса модели рабочей области
class IModel:
    @abstractmethod
    def set_scene(self, scene: IScene) -> None:
        """
        Устанавливает контроллер рабочей области.
        :param scene: контроллер рабочей области.
        """
        pass

    @abstractmethod
    def edges(self) -> [(int, int)]:
        """
        Получает список ребер графа.
        :return: список ребер графа.
        """
        pass

    @abstractmethod
    def nodes_to_calc(self) -> [int]:
        """
        Получает список вершин, которые могут быть рассчитаны.
        :return: список вершин, которые могут быть рассчитаны.
        """
        pass

    @abstractmethod
    def add_edge(self, src: int, dst: int) -> None:
        """
        Добавляет ребро в граф.
        :param src: начальная вершина ребра.
        :param dst: конечная вершина ребра.
        """
        pass

    @abstractmethod
    def remove_edge(self, src: int, dst: int) -> bool:
        """
        Удаляет ребро из графа.
        :param src: начальная вершина ребра.
        :param dst: конечная вершина ребра.
        :return: True, если ребро успешно удалено; False в противном случае.
        """
        pass

    @abstractmethod
    def remove_node(self, node: int) -> [int]:
        """
        Удаляет вершину и возвращает список связанных вершин.
        :param node: вершина для удаления.
        :return: список связанных вершин.
        """
        pass

    @abstractmethod
    def dfs(self, used: [bool], v: int) -> bool:
        """
        Поиск циклов в односвязном графе.
        :param used: список посещенных вершин.
        :param v: вершина для старта поиска.
        :return: True, если циклы найдены; False в противном случае.
        """
        pass

    @abstractmethod
    def search_cycles(self) -> bool:
        """
        Поиск циклов в графе.
        :return: True, если циклы найдены; False в противном случае.
        """
        pass

    @abstractmethod
    def has_edge(self, src: int, dst: int) -> bool:
        """
        Проверка наличия ребра в графе.
        :param src: начальная вершина ребра.
        :param dst: конечная вершина ребра.
        :return: True, если ребро существует; False в противном случае.
        """
        pass

    @abstractmethod
    def calc(self) -> None:
        """
        Расчет графа.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Проверка графа на пустоту.
        :return: True, если граф пустой; False в противном случае.
        """
        pass

    @abstractmethod
    def is_ready_to_calc(self) -> (bool, str):
        """
        Проверка на возможность расчета.
        :return: кортеж (bool, str) - True и пустую строку, если граф готов к расчету;
                 False и сообщение об ошибке в противном случае.
        """
        pass

    @abstractmethod
    def print(self) -> None:
        """
        Функция печати представления списка смежности Graph.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Очищает граф.
        """
        pass


# Интерфейс главного окна проекта
class IMainWindow(QMainWindow):
    @abstractmethod
    def get_scene(self) -> IScene:
        pass


