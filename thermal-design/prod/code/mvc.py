from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsRectItem, QGraphicsView, \
    QGraphicsSceneMouseEvent

from main_interfaces import IScene, IModel, WorkMode as WM, \
    BlockModelType as BMT, IBlockGfx
from block_graphics import Generator, Calculator, Display, GridLine, Link


class Controller(IScene):
    """
    Контроллер области редактирования
    """
    def __init__(self) -> None:
        """
        Инициализация контроллера
        """
        super().__init__()
        self.__y_cstart: int = 0
        self.__x_cstart: int = 0
        self.__delete_in_process: bool = False
        self.__model: IModel = None  # модель рабочей области
        self.__view: 'View' = None
        self.__work_mode: WM = WM.edit  # режим работы
        self.__prev_del_line: QGraphicsLineItem = None  # линия удаления
        self.__bounding_rect: QGraphicsRectItem = None
        self.__obj_count: int = 0  # количество объектов
        self.__blocks: [IBlockGfx] = []  # добавленные блоки
        self.__add_collision: bool = False  # флаг добавление блока
        self.__adding_block: BMT = BMT.generator

        self.setSceneRect(0, 0, 2000, 2000)  # установка размеров сцены
        self.draw_grid()

    def set_adding_block(self, block_type: BMT) -> None:
        """
        Устанавливает тип добавляемого блока
        :param block_type: тип блока
        """
        self.__adding_block = block_type

    def set_model(self, model: IModel) -> None:
        """
        Устанавливает модель области редактирования
        :param model: объект модели области редактирования
        """
        self.__model = model
        self.__model.set_scene(self)

    def set_view(self, view: 'View') -> None:
        """
        Устанавливает представление области редактирования
        :param view: объект представления
        """
        self.__view = view
        self.__view.setScene(self)

    def is_ready_to_calc(self) -> (bool, str):
        """
        Проверка на готовность к расчету модели
        :return: кортеж из результата проверки и строки ошибки
        """
        return self.__model.is_ready_to_calc()

    def create_link(self, src: int, dst: int) -> None:
        """
        Добавление в модель связи между двумя блоками
        :param src: источник
        :param dst: приемник
        """
        self.__model.add_edge(src, dst)

    def set_work_mode(self, mode: WM) -> None:
        """
        Установка режима работы
        :param mode: режим работы
        """
        self.__work_mode = mode

    def process_model(self) -> None:
        """
        Сигнализирует модели о начале расчета
        """
        self.__model.calc()

    def print_model(self) -> None:
        """
        Вывести текстовое представление модели графа
        """
        self.__model.print()

    def get_blocks(self) -> [IBlockGfx]:
        """
        Возвращает список блоков с индексом по id
        :return: список блоков
        """
        ids = []
        # сбор идентификаторов блоков в список
        for block in self.__blocks:
            ids.append(block.get_id())
        blocks = [None for _ in range(max(ids) + 1)]
        # заполнение списка блоков по идентификаторам
        for block in self.__blocks:
            blocks[block.get_id()] = block
        return blocks

    def remove_links(self, id: int) -> None:
        """
        Удаление связей у всех блоков, связанных с данным
        :param id: идентификатор блока
        """
        # получение списка идентификаторов вершин-источников для переданной
        rm = self.__model.remove_node(id)
        blks = self.get_blocks()
        # удаление связей для каждой вершины
        for i in rm:
            blks[i].move_connector()

    def create_block(self, x: int = 100, y: int = 100) -> IBlockGfx:
        """
        Метод добавления блока на графическую сцену
        :param x: координата по горизонтали
        :param y: координата по вертикали
        :return: блок
        """
        # создание нового блока по переданным параметрам и добавление его на рабочую область
        if self.__adding_block == BMT.generator:
            block = Generator(self, self.__obj_count, x=x, y=y)
        elif self.__adding_block == BMT.calculator:
            block = Calculator(self, self.__obj_count, x=x, y=y)
        else:
            block = Display(self, self.__obj_count, x=x, y=y)
        self.addItem(block)
        self.__blocks.append(block)
        self.__obj_count += 1
        return block

    def add_block(self, block: IBlockGfx) -> None:
        """
        Метод добавления блока на графическую сцену
        :param block: блок
        """
        # создание нового блока по переданным параметрам и добавление его на рабочую область
        self.addItem(block)
        self.__blocks.append(block)
        self.__obj_count += 1

    def on_press(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработчик события нажатия кнопки мыши
        :param event: событие нажатия кнопки мыши
        """
        # проверка на нажатую кнопку мыши
        if event.button() == Qt.MouseButton.LeftButton:
            # проверка на режим работы
            if self.__work_mode == WM.delete:
                self.__delete_in_process = True
                # сохранение начальной позиции курсора мыши
                self.__x_cstart = event.scenePos().x()
                self.__y_cstart = event.scenePos().y()
            elif self.__work_mode == WM.adding:
                if not self.__add_collision:
                    self.create_block(round((event.scenePos().x() - 30) / 10) * 10,
                                      round((event.scenePos().y() - 25) / 10) * 10)
                    self.removeItem(self.__bounding_rect)
        elif event.button() == Qt.MouseButton.RightButton:
            self.__work_mode = WM.edit
            if self.__bounding_rect:
                self.removeItem(self.__bounding_rect)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_press(event)
        super().mousePressEvent(event)

    def on_move(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработчик событие перемещения курсора мыши
        :param event: событие мыши
        """
        if self.__work_mode == WM.adding:
            if self.__bounding_rect:
                self.removeItem(self.__bounding_rect)
            self.__bounding_rect = QGraphicsRectItem(round((event.scenePos().x() - 40) / 10) * 10,
                                                     round((event.scenePos().y() - 35) / 10) * 10, 80, 70)
            self.addItem(self.__bounding_rect)
            col_items = self.__bounding_rect.collidingItems()
            self.__bounding_rect.setPen(QColor(QtCore.Qt.GlobalColor.black))
            self.__add_collision = False
            for item in col_items:
                if not isinstance(item, GridLine):
                    print("COLLISION")
                    self.__bounding_rect.setPen(QColor(QtCore.Qt.GlobalColor.red))
                    self.__add_collision = True
                    break
        # проверка на режим работы
        elif self.__work_mode == WM.delete and self.__delete_in_process:
            # установка новых координат курсора мыши
            x_cnew = event.scenePos().x()
            y_cnew = event.scenePos().y()
            # обновление линии удаления
            if self.__prev_del_line:
                self.removeItem(self.__prev_del_line)
            if self.__x_cstart and self.__y_cstart:
                self.__prev_del_line = QGraphicsLineItem(self.__x_cstart, self.__y_cstart, x_cnew, y_cnew)
                self.__prev_del_line.setPen(QColor(QtCore.Qt.GlobalColor.red))
                self.addItem(self.__prev_del_line)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_move(event)
        super().mouseMoveEvent(event)

    def on_release(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Обработка события отпускания кнопки мыши
        :param event: событие мыши
        """
        # проверка на нажатие кнопки
        if event.button() == Qt.MouseButton.LeftButton:
            # проверка на режим работы
            if self.__work_mode == WM.delete and self.__delete_in_process:
                self.__delete_in_process = False
                # получение списка пересекающих линию элементов
                ci = self.__prev_del_line.collidingItems()
                # фильтрация списка элементов
                c_links = list(filter(lambda x: (isinstance(x, Link)), ci))
                if c_links:
                    # удаление связей с рабочей области
                    for link in c_links:
                        link.get_connector().get_block().move_connector()
                        # удаление связей из модели
                        if link.get_connector().is_dst_complete():
                            self.__model.remove_edge(link.get_connector().get_block().get_id(),
                                                     link.get_connector().get_destination().get_id())
                # извлечение линии удаления
                self.removeItem(self.__prev_del_line)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.on_release(event)
        super().mouseReleaseEvent(event)

    def clear(self) -> None:
        """
        Очистка контроллера
        """
        super().clear()
        self.__y_cstart = None
        self.__x_cstart = None
        self.__delete_in_process = False
        self.__work_mode = WM.edit  # режим работы
        self.__prev_del_line = None  # линия удаления
        self.__obj_count = 0  # количество объектов
        self.__blocks = []  # добавленные блоки
        self.__model.clear()
        self.draw_grid()

    def block_by_id(self, id: int) -> IBlockGfx:
        """
        Возвращает блок по идентификатору
        :param id: идентификатор блока
        :return: блок
        """
        for item in self.items():
            if isinstance(item, IBlockGfx):
                if item.get_id() == id:
                    return item

    def draw_grid(self) -> None:
        """
        Рисует сетку на области редактирования
        """
        # Создаем перо для задания стиля линии
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)  # Толщина линии
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)  # Стиль линии
        for i in range(10, int(self.width()), 10):
            # Создаем объект QGraphicsLineItem
            line_item = GridLine(i, 0, i, int(self.height()))
            # Задаем перо для линии
            line_item.setPen(pen)
            self.addItem(line_item)
        for i in range(10, int(self.height()), 10):
            line_item = GridLine(0, i, int(self.width()), i)
            # Задаем перо для линии
            line_item.setPen(pen)
            self.addItem(line_item)


class Model(IModel):
    """
    Класс модели области редактирования
    """
    def __init__(self, edges: [(int, int)] = None) -> None:
        """
        Инициализация модели
        :param edges: список ребер
        """
        self.__scene: IScene = None  # контроллер рабочей области
        # проверяет на содержание переданных параметров
        if edges:
            # расчет размера списка смежности исходя из списка ребер
            max_index: int = 0
            for edge in edges:
                max_index = max(edge[0], edge[1], max_index)
            self.__list_size: int = max_index + 1
            # выделяет память для списка смежности и списка посещенных вершин
            self.__adj_list = [[] for _ in range(self.__list_size)]
            # добавляет ребра в ориентированный graph
            for (src, dst) in edges:
                # выделяет узел в списке смежности от src до dst
                self.__adj_list[src].append(dst)
        else:
            # в случае, если граф должен быть пустым
            self.__adj_list: [[int]] = []
            self.__used: [bool] = []
            self.__list_size: int = 0

    def set_scene(self, scene: IScene) -> None:
        """
        Устанавливает контроллер области редактирования
        :param scene: объект контроллера
        """
        self.__scene = scene

    def edges(self) -> [(int, int)]:
        """
        Получает список ребер графа
        :return: список ребер
        """
        edges = []
        # проход по каждому элементу списка смежности
        for src in range(len(self.__adj_list)):
            # вывести текущую вершину и все соседние с ней вершины
            for dst in self.__adj_list[src]:
                edges.append((src, dst))
        return edges

    def nodes_to_calc(self) -> [int]:
        """
        Получает список вершин, которые могут быть рассчитаны
        :return: список вершин
        """
        dsts = []
        # проход по всем элементам списка смежности
        for src in range(len(self.__adj_list)):
            for dst in self.__adj_list[src]:
                dsts.append(dst)
        srcs = []
        # добавление вершин, которых не оказалось в списке приемников данных
        for src in range(len(self.__adj_list)):
            if self.__adj_list[src]:
                if src not in dsts:
                    srcs.append(src)
        return srcs

    def add_edge(self, src: int, dst: int) -> None:
        """
        Добавляет ребро в граф
        :param src: источник
        :param dst: приемник
        """
        # Расширение списка смежности
        self.__list_size = max(src + 1, dst + 1, self.__list_size)
        if len(self.__adj_list) < self.__list_size:
            while len(self.__adj_list) < self.__list_size:
                self.__adj_list.append([])
        # Добавление ребра
        self.__adj_list[src].append(dst)

    def remove_edge(self, src: int, dst: int) -> bool:
        """
        Удаляет ребра из графа
        :param src: источник
        :param dst: приемник
        :return: результат операции
        """
        try:
            self.__adj_list[src].remove(dst)
            return True
        except:
            return False

    def remove_node(self, node: int) -> [int]:
        """
        Удаляет вершину и возвращает список связанных вершин
        :param node: вершина
        :return: список вершин
        """
        rm = []
        try:
            # Удаление ребер
            self.__adj_list[node] = []
            # Проход по списку смежности
            for i in range(self.__list_size):
                for u in self.__adj_list[i]:
                    if u == node:
                        # Добавление связанной вершины
                        rm.append(i)
                        self.__adj_list[i].remove(u)
        finally:
            return rm

    def dfs(self, used: [bool], v: int) -> bool:
        """
        Поиск циклов в односвязном графе
        :param used: массив пройденных вершин
        :param v: вершина начала поиска
        :return: результат поиска
        """
        used[v] = True
        for u in self.__adj_list[v]:
            if used[u]:
                return True
            else:
                if self.dfs(used, u):
                    return True
        return False

    def search_cycles(self) -> bool:
        """
        Поиск циклов в многосвязном графе
        :return: результат поиска
        """
        if not self.is_empty():
            # инициализация списка посещенных вершин
            used = [False for _ in range(self.__list_size)]
            for i in range(self.__list_size):
                if not used[i]:
                    # поиск циклов в односвязном графе
                    if self.dfs(used, i):
                        return True
        return False

    def has_edge(self, src: int, dst: int) -> bool:
        """
        Проверка наличие ребра в графе
        :param src: источник
        :param dst: приемник
        :return: результат проверки
        """
        return dst in self.__adj_list[src]

    def calc(self) -> None:
        """
        Расчет модели
        """
        # получение списка ребер графа
        calc_edges: [int] = self.edges()
        # получаение списка блоков рабочей области
        blocks: [IBlockGfx] = self.__scene.get_blocks()
        # инициализация списка рассчитанных блоков
        calculated = []
        # получение списка вершин для расчета
        nodes_to_calc: [int] = self.nodes_to_calc()
        # подготовка списка данных
        data = [None for _ in range(len(blocks))]
        i = 0
        # основной цикл расчета
        while calc_edges:
            # проверка вершины-источника на наличие данных
            if calc_edges[i][0] in nodes_to_calc:
                # расчет вершины-источника с сохранением данных
                data[calc_edges[i][0]] = blocks[calc_edges[i][0]].block_model.process_data(None)
                # добавление вершины-источника в список рассчитанных вершин
                calculated.append(calc_edges[i][0])
                # удаление вершины из списка доступных для расчета
                nodes_to_calc.remove(calc_edges[i][0])
            # проверка вершины-источника на готовность к передаче данных
            if calc_edges[i][0] in calculated:
                # расчет вершины-приемника с сохранением данных
                data[calc_edges[i][1]] = blocks[calc_edges[i][1]].block_model.process_data(data[calc_edges[i][0]])
                calculated.append(calc_edges[i][1])
                # извлечение рассчитанного ребра из списка
                calc_edges.remove(calc_edges[i])
            # изменение итеративной переменной
            i += 1
            if i >= len(calc_edges):
                i = 0

    def is_empty(self) -> bool:
        """
        Проверка графа на пустоту
        :return: результат проверки
        """
        if self.__list_size > 0:
            if self.__adj_list:
                for item in self.__adj_list:
                    if item:
                        return False
        return True

    def is_ready_to_calc(self) -> (bool, str):
        """
        Проверка на возможность расчета модели
        :return: кортеж из результата проверки и строки ошибки
        """
        msg = ""
        if not self.is_empty():
            if not self.search_cycles():
                return True, msg
            else:
                msg = "Расчет невозможен. Циклические соединения"
        else:
            msg = "Расчет невозможен. Нет связей."
        return False, msg

    def print(self) -> None:
        """
        Вывод модели в текстовом виде
        """
        if self.is_empty():
            print("Graph is empty")
            return
        print(f'__list_size = {self.__list_size}')
        print('edges:', end=" ")
        for src in range(len(self.__adj_list)):
            # вывести текущую вершину и все соседние с ней вершины
            for dst in self.__adj_list[src]:
                print(f'({src} —> {dst}) ', end='')
        print()

    def clear(self) -> None:
        """
        Сброс модели
        """
        self.__adj_list = []
        self.__used = []
        self.__list_size = 0


class View(QGraphicsView):
    """
    Представление области редактирования
    """
    def __init__(self):
        """
        Инициализация представления
        """
        super().__init__()
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
