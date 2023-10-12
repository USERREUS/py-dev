import queue
import DB
import datetime
import math
import random

from stat_info import InfoWindow


class BlockMdl:
    """
    Модель функционального блока
    """
    def __init__(
            self,
            id: int,
            noi_table: str = None,
            noc_data: str = None,
            noo_table: str = None
    ) -> None:
        """
        Инициализация
        :param id: идентификатор
        :param noi_table: наименование таблицы входных данных
        :param noc_data: наименование расчетного параметра
        :param noo_table: наименование таблицы выходных данных
        """
        if noi_table:
            self.__noi_table = noi_table
        if noc_data:
            self.__noc_data = noc_data
        if noo_table:
            self.__noo_table = noo_table

        self.__id = id

    def process_data(self, dt: dict) -> dict:
        """
        Обработка данных
        :param dt: данные для обработки
        :return: обработанные данные
        """
        pass


# Класс модель генератора
# Блок должен уметь считать данные из БД и подготовить их для передачи дальше
class GeneratorMdl(BlockMdl):
    """
    Класс модель генератора
    Блок должен уметь считать данные из БД и подготовить их для передачи дальше
    """
    def __init__(self, id: int, noi_table: str) -> None:
        """
        Инициализация
        :param id: идентификатор
        :param noi_table: наименование таблицы входных данных
        """
        super().__init__(id=id, noi_table=noi_table)
        self.data_rows = []

    def process_data(self, dt: dict) -> dict:
        """
        Обработка данных
        :param dt: данные для обработки
        :return: обработанные данные
        """
        return self.load_data()

    def load_data(self) -> dict:
        """
        Загрузка данных из хранилища
        :return: словарь данных
        """
        if not self.data_rows:
            msg, data = DB.get_json_data(self.__noi_table)
            self.data_rows = data['data']
        row_data = self.data_rows.pop(0)
        row_data['gen'] = self.__id
        return row_data


class CalculatorMdl(BlockMdl):
    """
    Блок для расчета
    Должен уметь принять данные, посчитать и отдать
    """
    def __init__(self, id: int, noc_data: str) -> None:
        """
        Инициализация
        :param id:
        :param noc_data:
        """
        super().__init__(id=id, noc_data=noc_data)

    def process_data(self, dt: dict) -> dict:
        """
        Обработка данных
        :param dt: данные для обработки
        :return: обработанные данные
        """
        return self.calc_data(dt)

    def calc_data(self, row: dict) -> dict:
        """
        Расчет данных
        :param row: данные для расчета
        :return: результаты расчета
        """
        idata = row[self.__noc_data]
        rdata = math.sqrt(idata)
        real_data = math.sqrt(idata) + random.uniform(-0.1*rdata, 0.1*rdata)  # тут ли ?
        row['y'] = round(rdata, 4)
        row['y_real'] = round(real_data, 4)
        row['datetime'] = datetime.datetime.now().isoformat(timespec='milliseconds')
        row['calc'] = self.__id
        return row


class DisplayMdl(BlockMdl):
    """
    Класс модель отображения
    Блок должен уметь принять данные и сохранить их
    """
    def __init__(self, id: int, noo_table: str) -> None:
        """
        Инициализация
        :param id: идентификатор
        :param noi_table: наименование таблицы выходных данных
        """
        super().__init__(id=id, noo_table=noo_table)
        # Установка параметров
        self.q: queue.Queue = queue.Queue(100)
        self.info: InfoWindow = InfoWindow(self.q)
        self.count: int = 0

    def show_statistics(self) -> None:
        """
        Вывод окна отображения статистической информации
        """
        self.info.show()

    def process_data(self, dt: dict) -> dict:
        """
        Обработка данных
        :param dt: данные для обработки
        :return: обработанные данные
        """
        self.save_data(dt)
        return {}

    def save_data(self, row: dict) -> None:
        """
        Сохранение данных в хранилище
        :param row: данные для сохранения
        """
        row['disp'] = self.__id
        try:
            self.q.put_nowait(row)
        except:
            self.q.get_nowait()
            self.q.put_nowait(row)

        self.count += 1
        if self.count >= 100:
            msg, json_data = DB.get_json_data(self.__noo_table)
            json_data['data'] += list(self.q.queue)
            DB.set_json_data(self.__noo_table, json_data)
            self.count = 0
