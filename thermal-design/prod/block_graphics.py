import math

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPolygonF, QPen, QFont
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsPolygonItem, \
    QGraphicsTextItem

from block_models import GeneratorMdl, CalculatorMdl, DisplayMdl, BlockMdl

from main_interfaces import ILink, IScene, BlockModelType as BMT, IBlockGfx, IConnector


class GridLine(QGraphicsLineItem):
    """
    Линия сетки области редактирования
    """
    pass


class BlockGfx(IBlockGfx):
    """
    Графическое описание функционального блока
    """
    def __init__(self, scene: IScene, id: int, model_type: BMT,
                 x: int = 100, y: int = 100,
                 width: int = 50, height: int = 50,
                 noi: int = 0, noo: int = 0,
                 title: str = "") -> None:
        """
        Инициализация
        :param scene: контроллер области редактирования
        :param id: идентификатор
        :param model_type: тип модели
        :param x: координата по горизонтали
        :param y: координата по вертикали
        :param width: ширина
        :param height: высота
        :param noi: количество входов
        :param noo: количество выходов
        :param title: заголовок
        """
        super().__init__(0, 0, width, height)
        #  координаты начала события перетаскивания
        self.__y_cstart: int = None
        self.__x_cstart: int = None
        #  координаты начального местоположения блока
        self.__y_start: int = None
        self.__x_start: int = None
        #  модель, которую реализует блок
        self.__model_type: BMT = model_type
        self.__block_model: BlockMdl = None
        #  контроллер рабочей области
        self.__scene: IScene = scene
        self.__s_width: int = int(scene.width())
        self.__s_height: int = int(scene.height())
        # размеры блока
        self.__width: int = width
        self.__height: int = height
        # уникальный идентификатор блока
        self.__id: int = id
        self.__number_of_outputs: int = noo  # число выходов
        self.__number_of_inputs: int = noi  # число входов
        self.__prev_triangles: [QGraphicsPolygonItem] = []  # список областей отображения точек входа и выхода
        self.__collision_flag: bool = False  # флаг возникновения конфликта при перемещении
        self.__title = title
        self.__text: QGraphicsTextItem = QGraphicsTextItem(title, self)  # наименование блока
        self.__connector = None  # отправитель данных
        self.__target = None  # цель для приема данных
        self.__is_set_up = False
        # настройка параметров
        self.__text.setPos(25 - len(title) * 6, 10)
        self.__text.setFont(QFont('Courier', 12))
        self.__moving: bool = False

        self.setPos(x, y)
        self.setBrush(QtCore.Qt.GlobalColor.white)
        # отрисовка треугольников
        self.draw_triangles()
        if noo:
            # связь
            self.__connector: Connector = Connector(self.x() + self.__width + 5, self.y() + self.__height / 2 - 5, 10,
                                                    self.__scene, self)
            self.__scene.addItem(self.__connector)
            self.move_connector()
        if noi:
            # ВХОД ДАННЫХ
            self.__target: Target = Target(0, 0, 6, 6, self)
            self.__target.setPos(self.x() - 17, self.y() + self.__height / 2 - 3)
            self.__target.setOpacity(0)
            self.__scene.addItem(self.__target)

    def get_noi(self) -> int:
        """
        Получение числа входов
        :return: число входов
        """
        return self.__number_of_inputs

    def get_noo(self) -> int:
        """
        Получение числа выходов
        :return: число выходов
        """
        return self.__number_of_outputs

    def get_id(self) -> int:
        """
        Получение идентификатора
        :return: идентификатор
        """
        return self.__id

    def get_model_type(self) -> BMT:
        """
        Получение типа модели
        :return: тип модели
        """
        return self.__model_type

    def get_connector(self) -> 'IConnector':
        """
        Получение соединителя
        :return: соединитель
        """
        return self.__connector

    def get_title(self) -> str:
        """
        Получение заголовка
        :return: заголовок
        """
        return self.__title

    def model_process(self, data: dict) -> dict:
        """
        Расчет реализуемой модели
        :param data: данные для расчета
        :return: обработанные данные
        """
        return self.__block_model.process_data(data)

    def on_bounding_rect(self) -> QtCore.QRectF:
        """
        Обработка события запроса описывающего прямоугольника
        :return: описывающий прямоугольник
        """
        if self.__moving:
            return QtCore.QRectF(-19, -9, 108, 68)
        return QtCore.QRectF(-9, -9, 68, 68)

    def detect_collision(self) -> bool:
        """
        Обнаружение конфликтов при перемещении
        :return: результат операции
        """
        items = self.collidingItems(QtCore.Qt.ItemSelectionMode.IntersectsItemBoundingRect)
        for item in items:
            if isinstance(item, BlockGfx) \
                    or isinstance(item, Link) \
                    or (isinstance(item, Connector) and item != self.__connector):
                return True

    def on_foreground(self) -> None:
        """
        Переместить блок на ближний слой
        """
        self.setZValue(1)
        if self.__connector:
            self.__connector.hide()
        # удаление предыдущих
        if self.__prev_triangles:
            for triangle in self.__prev_triangles:
                self.__scene.removeItem(triangle)
            self.__prev_triangles = []
        self.__is_set_up = True

    def on_background(self) -> None:
        """
        Переместить блок на дальний слой
        """
        self.setZValue(0.1)
        if self.__connector:
            self.__connector.show()
        self.__is_set_up = False

    def on_press(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработка события нажатия мыши
        :param event: событие мыши
        """
        self.__moving = True
        self.__x_start = self.scenePos().x()
        self.__y_start = self.scenePos().y()
        self.__x_cstart = event.scenePos().x()
        self.__y_cstart = event.scenePos().y()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_press(event)

    def exceeding_the_boundaries(self, new_x: int, new_y: int) -> bool:
        """
        Проверка на выход за границы области редактирования
        :param new_x: новая координата по горизонтали
        :param new_y: новая координата по вертикали
        :return: результат проверки
        """
        return new_x < 40 or new_y < 20 or new_x > (self.__s_width - self.__width - 40) \
            or new_y > (self.__s_height - self.__height - 20)

    def move_connector(self) -> None:
        """
        Перемещение соединителя
        """
        if self.__number_of_outputs:
            self.__connector.setPos(self.x() + self.__width + 5, self.y() + self.__height / 2 - 5)
            self.__connector.remove_links()
            self.__connector.set_base_color()
            self.__connector.show()

    def on_move(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработка событие перемещения курсора мыши
        :param event: событие перемещения курсора
        """
        x_clast = event.lastScenePos().x()
        y_clast = event.lastScenePos().y()
        x_cnew = event.scenePos().x()
        y_cnew = event.scenePos().y()
        x_orig = self.scenePos().x()
        y_orig = self.scenePos().y()
        x_cupd = x_cnew - x_clast + x_orig
        y_cupd = y_cnew - y_clast + y_orig
        # проверка на выход за границы
        if not self.exceeding_the_boundaries(x_cupd, y_cupd):
            if math.dist((self.__x_cstart, self.__y_cstart), (x_cnew, y_cnew)) >= 10:
                if not self.__is_set_up:
                    self.on_foreground()
                self.setPos(QPointF(x_cupd, y_cupd))
                # Разрушить связи
                self.move_connector()
                self.move_target()
                self.__scene.remove_links(self.__id)
                # Обнаружение коллизий
                if self.detect_collision():
                    self.set_collision_color()
                    self.__collision_flag = True
                else:
                    self.set_base_color()
                    self.__collision_flag = False

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_move(event)

    def set_collision_color(self) -> None:
        """
        Установка цвета коллизии
        """
        self.setBrush(QColor(QtCore.Qt.GlobalColor.red))

    def set_base_color(self) -> None:
        """
        Установка базового цвета
        """
        self.setBrush(QColor(QtCore.Qt.GlobalColor.white))

    def move_target(self) -> None:
        """
        Перемещение цели
        """
        if self.__number_of_inputs:
            self.__target.setPos(self.x() - 17, self.y() + self.__height / 2 - 3)

    def on_release(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработка события отпускания кнопки мыши
        :param event: событие мыши
        """
        self.on_background()
        self.__moving = False
        if math.dist((self.__x_cstart, self.__y_cstart), (event.scenePos().x(), event.scenePos().y())) >= 10:
            # Если перетаскивания не было
            if self.__collision_flag:
                self.setPos(self.__x_start, self.__y_start)
                self.draw_triangles()
                self.move_connector()
                self.move_target()
                # восстанавливаем цвет
                self.set_base_color()
                # в любом случае восстанавливаем курсор
                # app.restoreOverrideCursor()
                return
            self.setPos(round((self.scenePos().x()) / 10) * 10, round((self.scenePos().y()) / 10) * 10)
            self.draw_triangles()
            self.move_connector()
            self.move_target()

    def mouseReleaseEvent(self, event):
        self.on_release(event)

    def draw_triangles(self) -> None:
        """
        Отрисовка связанных частей
        """
        # удаление предыдущих
        if self.__prev_triangles:
            for triangle in self.__prev_triangles:
                self.__scene.removeItem(triangle)
            self.__prev_triangles = []
        # отрисовка выходов
        for i in range(self.__number_of_outputs):
            start_x = self.scenePos().x() + self.__width
            start_y = self.scenePos().y() + round(
                (self.__height * ((i + 1) / (self.__number_of_outputs + 1)) - 5) / 10) * 10
            triangle = QGraphicsPolygonItem(
                QPolygonF(
                    [QPointF(start_x, start_y), QPointF(start_x + 10, start_y + 5), QPointF(start_x, start_y + 10)]))
            self.__scene.addItem(triangle)
            self.__prev_triangles.append(triangle)
        # отрисовка входов
        for i in range(self.__number_of_inputs):
            start_x = self.scenePos().x() - 10
            start_y = self.scenePos().y() + round((self.__height * ((i + 1) /
                                                                    (self.__number_of_inputs + 1)) - 5) / 10) * 10
            triangle = QGraphicsPolygonItem(
                QPolygonF(
                    [QPointF(start_x, start_y), QPointF(start_x + 10, start_y + 5), QPointF(start_x, start_y + 10)]))
            self.__scene.addItem(triangle)
            self.__prev_triangles.append(triangle)


class Target(QGraphicsRectItem):
    """
    Область для соединения между блоками
    """
    def __init__(self, x, y, w, h, b: BlockGfx):
        """
        Инициализация
        :param x: координата по горизонтали
        :param y: координата по вертикали
        :param w: ширина
        :param h: высота
        :param b: блок-приемник
        """
        super().__init__(x, y, w, h)
        self.__block = b

    def get_block(self) -> IBlockGfx:
        """
        Получение блока-приемника
        :return: объект блока
        """
        return self.__block


class Link(ILink):
    """
    Линия связи между блоками
    """
    def __init__(self, x0, y0, x1, y1, c: IConnector):
        """
        Инициализация
        :param x0: координата начала по горизонтали
        :param y0: координата начала по вертикали
        :param x1: координата конца по горизонтали
        :param y1: координата конца по вертикали
        :param c:  объект соединителя-источника
        """
        super().__init__(x0, y0, x1, y1)
        self.__connector = c

    def get_connector(self) -> IConnector:
        """
        Получение соединителя-источника
        :return: объект соединителя
        """
        return self.__connector


class Connector(IConnector):
    """
    Подвижный соединитель блоков связью
    """
    def __init__(self, x: int, y: int, d: int, s: IScene, b: BlockGfx) -> None:
        """
        Инициализация
        :param x: координата по горизонтали
        :param y: координата по вертикали
        :param d: диаметр
        :param s: объект контроллера области редактирования
        :param b: объект блока-источника
        """
        super().__init__(0, 0, d, d)
        self.__diameter = d
        self.__scene = s
        self.__links: [Link] = []
        self.__destination_complete: bool = False
        self.__destination: BlockGfx = None
        self.__collision_flag: bool = False
        self.__scene_width = s.width()
        self.__scene_height = s.height()
        self.__block: [BlockGfx] = b
        self.__prev_line_intersect = None
        self.__line_intersect = None
        self.__x_start = 0
        self.__y_start = 0
        self.__x_cstart = 0
        self.__y_cstart = 0

        self.setZValue(0.5)  # расположение блока поверх остальных
        self.setBrush(QtCore.Qt.GlobalColor.white)
        self.setPos(x, y)

    def get_block(self) -> IBlockGfx:
        """
        Получение блока-источника
        :return: объект блока
        """
        return self.__block

    def remove_links(self) -> None:
        """
        Удаление всех связей, построенных соединителем
        """
        for link in self.__links:
            self.__scene.removeItem(link)
        self.__links = []

    def on_press(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработчик события нажатия мыши
        :param event: событие мыши
        """
        self.__x_start = self.scenePos().x()
        self.__y_start = self.scenePos().y()
        self.__x_cstart = event.scenePos().x()
        self.__y_cstart = event.scenePos().y()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_press(event)

    def exceeding_the_boundaries(self, new_x: int, new_y: int) -> bool:
        """
        Проверка на выход за границы области редактирования
        :param new_x: новая координата по горизонтали
        :param new_y: новая координата по вертикали
        :return: результат проверки
        """
        return new_x < 40 or new_y < 20 or new_x > (self.__scene_width - self.__diameter - 40) \
            or new_y > (self.__scene_height - self.__diameter - 20)

    def detect_collision(self) -> bool:
        """
        Проверка на пересечение с другими графическими компонентами
        :return: результат проверки
        """
        if self.__line_intersect in self.__scene.items():
            self.__scene.removeItem(self.__line_intersect)

        delta_x = delta_y = 0
        if self.__x_start != self.scenePos().x():
            delta_x = (self.scenePos().x() - self.__x_start) / math.fabs((self.scenePos().x() - self.__x_start))
        if self.__y_start != self.scenePos().y():
            delta_y = (self.scenePos().y() - self.__y_start) / math.fabs((self.scenePos().y() - self.__y_start))

        # Линия для контроля пересечений
        self.__line_intersect = Link(self.__x_start + self.__diameter / 2 + 1 * delta_x,
                                     self.__y_start + self.__diameter / 2 + 1 * delta_y,
                                     self.scenePos().x() + self.__diameter / 2,
                                     self.scenePos().y() + self.__diameter / 2, self)

        self.__line_intersect.setPen(QPen(QtCore.Qt.PenStyle.DashLine))

        self.__scene.addItem(self.__line_intersect)

        intersections = self.__line_intersect.collidingItems()

        # Пересечение с блоками
        for item in self.__scene.items():
            if isinstance(item, BlockGfx):
                if self.__line_intersect in item.collidingItems(Qt.ItemSelectionMode.IntersectsItemBoundingRect):
                    # Запрет связи
                    return True

        # Пересечение со связями
        if intersections:
            for item in intersections:
                if isinstance(item, Link) or \
                        isinstance(item, Connector) and item != self:
                    return True

        # восстановление цвета + снятие запрета соединения
        self.set_base_color()
        self.__line_intersect.setPen(QPen(QColor(Qt.GlobalColor.black), 1, style=QtCore.Qt.PenStyle.DashLine))
        self.__collision_flag = False
        return False

    def move_connector(self, x_cnew: int, y_cnew: int) -> None:
        """
        Смещение в вертикальном или горизонтальном направлении
        :param x_cnew: новая координата по горизонтали
        :param y_cnew: новая координата по вертикали
        """
        if math.fabs(self.__x_cstart - x_cnew) > math.fabs(self.__y_cstart - y_cnew):
            self.setPos(QPointF(round((self.__x_start + x_cnew - self.__x_cstart) / 10) * 10, self.__y_start))
        else:
            self.setPos(QPointF(self.__x_start, round((self.__y_start + y_cnew - self.__y_cstart) / 10) * 10))

    def is_complete_link_possible(self) -> bool:
        """
        Индикация о возможности завершения построения связи
        :return: результат проверки
        """
        for coll in self.collidingItems():
            if isinstance(coll, Target):
                self.set_complete_color()
                return True
        return False

    def on_move(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработчик события перемещения мыши
        :param event: событие мыши
        """
        # сохранение новой позиции курсора
        x_cnew = event.scenePos().x()
        y_cnew = event.scenePos().y()
        # Проверка на выход за границы
        if self.exceeding_the_boundaries(x_cnew, y_cnew):
            return
        # Проверка на расстояние перемещения
        if math.dist((self.__x_cstart, self.__y_cstart), (x_cnew, y_cnew)) < 10:
            return
        self.move_connector(x_cnew, y_cnew)  # перемещение соединителя
        # Проверка на конфликты с другими графическими объектами
        if self.detect_collision():
            self.set_collision_color()
            self.__line_intersect.setPen(QPen(QColor(Qt.GlobalColor.red), 1, style=QtCore.Qt.PenStyle.DashLine))
            self.__collision_flag = True

        self.is_complete_link_possible()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_move(event)

    def link_complete(self) -> None:
        """
        Завершение связи
        """
        # завершение построения связи
        for coll in self.collidingItems():
            if isinstance(coll, Target):
                # операция завершения связи
                link = Link(self.scenePos().x() + self.__diameter / 2,
                            self.scenePos().y() + self.__diameter / 2,
                            self.scenePos().x() + self.__diameter,
                            self.scenePos().y() + self.__diameter / 2,
                            self)
                self.__links.append(link)
                self.__scene.addItem(link)

                # добавление новой связи в граф
                self.__scene.create_link(self.__block.get_id(), coll.get_block().get_id())

                self.__destination_complete = True
                self.__destination = coll.get_block()

                self.hide()
                return

    def on_release(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработка события отпускания мыши
        :param event: событие мыши
        """
        if math.dist((self.__x_start, self.__y_start), (event.scenePos().x(), event.scenePos().y())) >= 10:
            # Если на этапе перетаскивания возникла коллизия
            self.__scene.removeItem(self.__line_intersect)

            if self.__collision_flag:
                self.setPos(self.__x_start, self.__y_start)
                self.set_base_color()
            else:
                link = Link(self.__x_start + self.__diameter / 2,
                            self.__y_start + self.__diameter / 2,
                            self.scenePos().x() + self.__diameter / 2,
                            self.scenePos().y() + self.__diameter / 2, self)
                self.__scene.addItem(link)
                self.__links.append(link)

            self.link_complete()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_release(event)

    def get_destination(self) -> IBlockGfx:
        """
        Возвращает блок-приемник данных
        :return: объект блока
        """
        return self.__destination

    def get_links(self) -> [Link]:
        """
        Получение списка связей
        :return: список связей
        """
        return self.__links

    def is_dst_complete(self) -> bool:
        """
        Проверка на завершенность связи
        :return: результат проверки
        """
        return self.__destination_complete

    def set_base_color(self) -> None:
        """
        Установка базового цвета
        """
        self.setBrush(QtGui.QColor(255, 255, 255))

    def set_collision_color(self) -> None:
        """
        Установка цвета коллизии
        """
        self.setBrush(QColor(QtCore.Qt.GlobalColor.red))

    def set_complete_color(self) -> None:
        """
        Установка цвета завершения связи
        """
        self.setBrush(QColor(QtCore.Qt.GlobalColor.blue))


class CalculatorGfx(BlockGfx):
    """
    Расчетный блок
    """
    def __init__(self, scene: IScene, id: int, x: int, y: int) -> None:
        """
        Инициализация
        :param scene: контроллер области редактирования
        :param id: идентификатор
        :param x: координата по горизонтали
        :param y: координата по вертикали
        """
        super().__init__(
            scene,
            id,
            BMT.calculator,
            x=x,
            y=y,
            title="PROC",
            noi=1,
            noo=1)
        self.block_model = CalculatorMdl(id, 'x')


class Generator(BlockGfx):
    """
    Блок генератор
    """
    def __init__(self, scene: IScene, id: int, x: int, y: int) -> None:
        """
        Инициализация
        :param scene: контроллер области редактирования
        :param id: идентификатор
        :param x: координата по горизонтали
        :param y: координата по вертикали
        """
        super().__init__(
            scene,
            id,
            BMT.generator,
            x=x,
            y=y,
            title="GEN",
            noo=1)
        self.block_model = GeneratorMdl(id, "sample")


class Display(BlockGfx):
    """
    Блок вывода информации
    """
    def __init__(self, scene: IScene, id: int, x: int = 100, y: int = 100) -> None:
        """
        Инициализация
        :param scene: контроллер области редактирования
        :param id: идентификатор
        :param x: координата по горизонтали
        :param y: координата по вертикали
        """
        super().__init__(
            scene,
            id,
            BMT.display,
            x=x,
            y=y,
            title="DISP",
            noi=1)
        self.block_model = DisplayMdl(id, "output")

    def on_double_click(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        Обработчик двойного нажатия мыши
        :param event: событие мыши
        """
        self.block_model.show_statistics()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.on_double_click(event)
