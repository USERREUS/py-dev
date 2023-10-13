import datetime as datetime
import json
import random

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values


# Подгрузка конфигурационных данных из файла
with open("user_data.json", 'r') as read_file:
    data = json.load(read_file)

dbname = data['dbname']
dbuser = data['dbuser']
password = data['password']

""" EXAMPLE OF USAGE DB
conn = psycopg2.connect(dbname='test', user='postgres', password='admin')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS super_heroes")
cur.execute("DROP TABLE IF EXISTS traffic_light")

conn.commit()

cur.execute("CREATE TABLE super_heroes (hero_id serial PRIMARY KEY, hero_name varchar, strength int);")

cur.execute("INSERT INTO super_heroes (hero_name, strength) VALUES (%s, %s)", ("Superman", 100))
cur.execute("INSERT INTO super_heroes (hero_name, strength) VALUES (%s, %s)", ("Flash", 1000))

cur.execute(""""""
                INSERT INTO super_heroes  (hero_name, strength)
                VALUES (%(name)s, %(strength)s);
            """""", {'name': 'Green Arrow', 'strength': 80})

conn.commit()


cur.execute("CREATE TABLE traffic_light (light_id serial PRIMARY KEY, light text);")

cur.execute("INSERT INTO traffic_light (light) VALUES (%s)", ("red",))

conn.commit()

cur.execute("SELECT * FROM super_heroes")

one_line = cur.fetchone()
print(one_line)

full_fetch = cur.fetchall()
for record in full_fetch:
    print(record)

# full_fetch[0][0]
conn.commit()

cur.close()
conn.close()

# Менеждер контекста

with psycopg2.connect(dbname='test', user='postgres', password='admin') as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as curs:

        execute_values(curs, "INSERT INTO traffic_light (light) VALUES %s", [("green",), ("yellow",)])

        curs.execute("SELECT * FROM traffic_light")
        records = curs.fetchall()
        print(records)
        print(records[0]["light"])

conn = psycopg2.connect(dbname='test', user='postgres', password='admin')
try:
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                        """"""
                        UPDATE super_heroes
                        SET strength = %s
                        WHERE hero_name = %s
                        """""", (90, 'Superman')
            )
finally:
    conn.close()

conn = psycopg2.connect(dbname='test', user='postgres', password='admin')
with conn:
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM super_heroes")
        print(curs.fetchall())

conn.close()
"""


# Создание таблицы для сохранения результатов вычисления (НЕ ИСПОЛЬЗУЕТСЯ)
def create_table():
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("DROP TABLE IF EXISTS time_calculation")
                curs.execute(
                    "CREATE TABLE time_calculation ("
                    "calc_id serial PRIMARY KEY, "
                    "block_name VARCHAR(10), "
                    "func_name VARCHAR(20), "
                    "calc_dt TIMESTAMP(3), "
                    "add_db_dt TIMESTAMP(3) DEFAULT NOW(), "
                    "input_value NUMERIC(10,4), "
                    "result_value NUMERIC(20,4)); "
                )
    finally:
        conn.close()


# Добавление результата вычисления в БД (НЕ ИСПОЛЬЗУЕТСЯ)
def add_value(block_name, func_name, calc_dt, input_val, result_val):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    "INSERT INTO time_calculation ("
                    "block_name, "
                    "func_name, "
                    "calc_dt, "
                    "input_value, "
                    "result_value) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (block_name, func_name, calc_dt, input_val, result_val)
                )
    finally:
        conn.close()


# Добавление результата вычисления в таблицу подогревателя
def add_value_lph(row_id, result):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO lph_out ("
                    "row_id, "
                    "calc_date, "
                    "heat_transfer_coefficient, "
                    "underheating_condensate, "
                    "condensate_outlet_temperature)"
                    "VALUES (%s, %s, %s, %s, %s)",
                    (row_id, str(datetime.datetime.now()), result[0], result[1], result[2])
                )
    finally:
        conn.close()


# Добавление результата вычисления в таблицу конденсатора
def add_value_cond(row_id, result):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO condenser_out ("
                    "row_id, "
                    "calc_date, "
                    "water_temperature, "
                    "saturation_temperature, "
                    "hydraulic_resistance, "
                    "heat_transfer)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (row_id, str(datetime.datetime.now()), result[0], result[1], result[2], result[3])
                )
    finally:
        conn.close()


# Добавление результата вычисления в таблицу турбины
def add_value_wsp(row_id, result):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO turbine_out ("
                    "row_id, "
                    "calc_date, "
                    "enthalpy_before, "
                    "entropy_before, "
                    "enthalpy_after, "
                    "entropy_after, "
                    "steam_temperature, "
                    "enthalpy_1, "
                    "steam_temperature_1)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (row_id, str(datetime.datetime.now()), result[0], result[1], result[2], result[3],
                     result[4], result[5][1], result[5][2])
                )
    finally:
        conn.close()


# Добавление результата вычисления в таблицу сравнения
def add_value_cmp(cmp_table_name, row_id, result):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO {cmp_table_name} ("
                    "row_id, "
                    "calc_date, "
                    "its, "
                    "technical_condition, "
                    "recommended_effect, "
                    "state)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (row_id, str(datetime.datetime.now()), result[0], result[1], result[2], result[3])
                )
    finally:
        conn.close()


# Получаение значений из базы данных
def get_data(name_of_data, name_of_columns=None, row_id=None):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                if name_of_columns:
                    if row_id:
                        curs.execute(f"SELECT {name_of_columns} FROM {name_of_data} WHERE row_id = {row_id}")
                    else:
                        curs.execute(f"SELECT {name_of_columns} FROM {name_of_data}")
                else:
                    if row_id:
                        curs.execute(f"SELECT * FROM {name_of_data} WHERE row_id = {row_id}")
                    else:
                        curs.execute(f"SELECT * FROM {name_of_data}")
                return curs.fetchall()
    finally:
        conn.close()


# Получение значений из БД для графика (НЕ ИСПОЛЬЗУЕТСЯ)
def get_data_graph(name_of_data):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(f"SELECT heating_vapor_pressure FROM {name_of_data}")
                return curs.fetchall()
    finally:
        conn.close()


# Парсинг данных на массив строк
def parse_data(records) -> [str]:
    data_table = []
    for record in records:
        data_row = []
        for item in record:
            data_row.append(record[item])
        data_table.append(data_row)
    return data_table


# Парсинг данных по имени колонки
def parse_data_for_name(records, name) -> [str]:
    data = []
    for record in records:
        for item in record:
            if item == name:
                data.append(record[item])
    return data


# Получить заголовки колонок из таблицы
def get_column_names(records):
    column_names = []
    if len(records) > 0:
        for item in records[0]:
            column_names.append(item)
    return column_names


# Вернуть данные по времени
def get_data_timediff(table, dt_col_name, time_from) -> [str]:
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                    f"SELECT * "
                    f"FROM {table} "
                    f"WHERE {dt_col_name} > %s", (time_from, )
                )
                return curs.fetchall()
    finally:
        conn.close()


# Преобразовать в дату для базы данных
def TO_DT_DB_FORMAT(date):
    dt_new = datetime.datetime(date[0], date[1], date[2])
    return dt_new


# Типа словарь с для хранения информации в кириллице
pairs = {
    # LPH IN DATA
    'row_id': ('id', ''),
    'date': ('Дата загрузки', ''),
    'steam_pressure': ('P_п', ', МПа'),
    'condensate_temperature': ('t_вх', ', °С'),
    'condensate_flow_rate': ('G_к', ', т/ч'),
    'internal_diameter': ('d_вн', ', м'),
    'outer_diameter': ('d_нар', ', м'),
    'water_passes': ('z', ', шт'),
    'length_tube': ('l', ', м'),
    'number_tubes': ('N', ', м'),
    'heating_area': ('F', ', м^2'),
    'heat_conductivity': ('lyambda_me', ', Вт/м*°С'),

    # LPH OUT DATA
    'heat_transfer_coefficient': ('k_ideal', ', Вт/м^2*K'),
    'underheating_condensate': ('delta_t_out_ideal', ', °C'),
    'condensate_outlet_temperature': ('t_out', ', °C'),
    'calc_date': ('Дата расчета', ''),
    'recording_date': ('Дата загрузки', ''),

    # CONDENSER IN DATA
    'consumption_steam': ('Gп', ', кг/с'),
    'consumption_water': ('Gв', ', кг/с'),
    'temperature_entry': ('t1в', ', K'),
    'diameter_outside': ('dн', ', мм'),
    'diameter_inside': ('dвн', ', мм'),
    'number_of_water_strokes': ('z', ', шт.'),
    'water_speed': ('W', ', м/с'),
    'square': ('F', ', м2'),
    'saturation_temperature': ('tk', ', °С'),
    'tube_length': ('L', ', м'),

    # CONDENSER OUT DATA
    'hydraulic_resistance': ('Hr', ', Па'),
    'water_temperature': ('t2в', ', °C'),
    'heat_transfer': ('k', ', Вт/(м^2*K)'),

    # WSP IN DATA
    'efficiency': ('этта_цилиндра', ''),
    'pressure_entry': ('P_вход_цилиндра', ', МПа'),
    'consumption_entry': ('G_вход', ', кг/с'),
    'pressure_out': ('P_выход_цилиндра', ', МПа'),
    'number_of_selections': ('N_отбор', ', шт.'),
    'selection_pressure': ('p_i', ', кг/с'),
    'sampling_flow': ('g_i', ', МПа'),

    # WSP OUT DATA
    'enthalpy_before': ('h_вход_цилинда', ', кДж/кг'),
    'entropy_before': ('s_вход_цилинда', ', кДж/кг*К'),
    'enthalpy_after': ('h_выход_цилинда_реал', ', кДж/кг'),
    'entropy_after': ('s_выход_цилинда_реал', ', кДж/кг*К'),
    'enthalpy_1': ('h_отбор', ', кДж/кг'),
    'steam_temperature': ('t_выход_цилинда', ', К'),
    'steam_temperature_1': ('t_отбор', ', К'),

    # CMP MODEL OUT DATA
    'its': ('ИТС', ''),
    'technical_condition': ('Состояние', ''),
    'recommended_effect': ('Рекомендации', ''),
    'state': ('Константа контроля состояния', '')
}


# Получить значение из словаря по заголовку колонки
def to_readable_data(key):
    return pairs[key]


# Получить заголовок колонки по значению из словаря
def readable_to_data(value):
    for key in pairs:
        if value == pairs[key][0]:
            return key


# Конвертировать заголовки в читабельный вид
def readable_labels(labels):
    new_labels = []
    for label in labels:
        new_label = to_readable_data(label)
        new_labels.append(new_label[0] + new_label[1])
    return new_labels


# # Данные для сравнения с эталоном (НЕ ИСПОЛЬЗУЕТСЯ)
# required_data_lph = {
#     'steam_consumption': '100',
#     'parallel_pipes': '2200',
#     'heat_transfer_coefficient': '4700'
# }


def get_random(lst):
    list_random = []
    for data in lst:
        list_random.append(random.uniform(data - data / 20, data + data / 20))
    return list_random


def insert_random_data():
    # LPH random
    lph_data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lph_data_random = get_random(lph_data)

    # Cond random
    cond_data = [319.6, 15700, 15, 28, 26, 2, 2.1, 36138, 18.2, 35]
    cond_data_random = get_random(cond_data)

    # WSP random
    wsp_data = [120, 2.5, 500, 0.24, 0.95, 1, 1.4, 6]
    wsp_data_random = get_random(wsp_data)

    # CMP lph random
    cmp_lph_data = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    cmp_lph_data_random = get_random(cmp_lph_data)

    # CMP cond random
    cmp_cond_data = [27, 3500, 28, 90000, 3, 0.5, 8]
    cmp_cond_data_random = get_random(cmp_cond_data)

    # CMP wsp random
    cmp_wsp_data = [570, 3050, 2, 2, 2, 2, 50]
    cmp_wsp_data_random = get_random(cmp_wsp_data)

    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO condenser_in ("
                    "consumption_steam, "
                    "consumption_water, "
                    "temperature_entry, "
                    "diameter_outside, "
                    "diameter_inside, "
                    "number_of_water_strokes, "
                    "water_speed,"
                    "square,"
                    "tube_length,"
                    "saturation_temperature"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING row_id",
                    (
                        cond_data_random[0],
                        cond_data_random[1],
                        cond_data_random[2],
                        cond_data_random[3],
                        cond_data_random[4],
                        cond_data_random[5],
                        cond_data_random[6],
                        cond_data_random[7],
                        cond_data_random[8],
                        cond_data_random[9]
                    )
                )
                id = curs.fetchone()[0]
                curs.execute(
                    f"INSERT INTO lph_in ("
                    "row_id, "
                    "steam_pressure, "
                    "condensate_temperature, "
                    "condensate_flow_rate, "
                    "internal_diameter, "
                    "outer_diameter, "
                    "water_passes, "
                    "length_tube, "
                    "number_tubes, "
                    "heating_area, "
                    "heat_conductivity"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        lph_data_random[0],
                        lph_data_random[1],
                        lph_data_random[2],
                        lph_data_random[3],
                        lph_data_random[4],
                        lph_data_random[5],
                        lph_data_random[6],
                        lph_data_random[7],
                        lph_data_random[8],
                        lph_data_random[9]
                    )
                )
                curs.execute(
                    f"INSERT INTO turbine_in ("
                    "row_id, "
                    "temperature_entry, "
                    "pressure_entry, "
                    "consumption_entry, "
                    "pressure_out, "
                    "efficiency, "
                    "number_of_selections, "
                    "selection_pressure, "
                    "sampling_flow"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        wsp_data_random[0],
                        wsp_data_random[1],
                        wsp_data_random[2],
                        wsp_data_random[3],
                        wsp_data_random[4],
                        wsp_data_random[5],
                        wsp_data_random[6],
                        wsp_data_random[7]
                    )
                )
                curs.execute(
                    f"INSERT INTO cmp_lph_in ("
                    "row_id, "
                    "steam_pressure, "
                    "condensate_temperature, "
                    "condensate_flow_rate, "
                    "internal_diameter, "
                    "outer_diameter, "
                    "water_passes, "
                    "length_tube, "
                    "number_tubes, "
                    "heating_area, "
                    "heat_conductivity"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        cmp_lph_data_random[0],
                        cmp_lph_data_random[1],
                        cmp_lph_data_random[2],
                        cmp_lph_data_random[3],
                        cmp_lph_data_random[4],
                        cmp_lph_data_random[5],
                        cmp_lph_data_random[6],
                        cmp_lph_data_random[7],
                        cmp_lph_data_random[8],
                        cmp_lph_data_random[9]
                    )
                )
                curs.execute(
                    f"INSERT INTO cmp_cond_in ("
                    "row_id, "
                    "t2in, "
                    "k, "
                    "tk, "
                    "delta_p, "
                    "ph, "
                    "elect, "
                    "o2"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        cmp_cond_data_random[0],
                        cmp_cond_data_random[1],
                        cmp_cond_data_random[2],
                        cmp_cond_data_random[3],
                        cmp_cond_data_random[4],
                        cmp_cond_data_random[5],
                        cmp_cond_data_random[6]
                    )
                )
                curs.execute(
                    f"INSERT INTO cmp_wsp_in ("
                    "row_id, "
                    "t_out, "
                    "h_out, "
                    "opp, "
                    "oc, "
                    "vib_h, "
                    "vib_v, "
                    "tem_oil"
                    ")"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        cmp_wsp_data_random[0],
                        cmp_wsp_data_random[1],
                        cmp_wsp_data_random[2],
                        cmp_wsp_data_random[3],
                        cmp_wsp_data_random[4],
                        cmp_wsp_data_random[5],
                        cmp_wsp_data_random[6]
                    )
                )
    finally:
        conn.close()


def clear_all_data():
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    "DELETE FROM lph_in"
                )
                curs.execute(
                    "DELETE FROM lph_out"
                )
                curs.execute(
                    "DELETE FROM turbine_in"
                )
                curs.execute(
                    "DELETE FROM turbine_out"
                )
                curs.execute(
                    "DELETE FROM cmp_lph_in"
                )
                curs.execute(
                    "DELETE FROM cmp_lph_out"
                )
                curs.execute(
                    "DELETE FROM cmp_cond_in"
                )
                curs.execute(
                    "DELETE FROM cmp_cond_out"
                )
                curs.execute(
                    "DELETE FROM cmp_wsp_in"
                )
                curs.execute(
                    "DELETE FROM cmp_wsp_out"
                )
                curs.execute(
                    "DELETE FROM condenser_out"
                )
                curs.execute(
                    "DELETE FROM condenser_in"
                )
    finally:
        conn.close()


# clear_all_data()
# for i in range(10):
# insert_random_data()
# create_table()
# add_value("T", "F", datetime.datetime.now(), 5, 25)
# add_value("T", "F", datetime.datetime.now(), 6, 36)
# add_value("T", "F", datetime.datetime.now(), 7, 49)
# # print(parse_data(get_data_timediff(LAST_MINUTE())))
# print(get_data('lph_in'))
# print(parse_data_for_name(data, 'created_date'))
# print(get_column_names(data))
# print(readable_to_data('z_1'))
# a = TO_DT_DB_FORMAT(0, 0, 0)
# b = TO_DT_DB_FORMAT(20, 20, 20)
# print(a, b)
# print(get_data_timediff("id", "lph_inp_data", "dt_load", a, b))

# ---------------------------------------------------------------------------------------

# def lph_out_create():
#     conn = psycopg2.connect(dbname='workwork', user='postgres', password='zaq123')
#     try:
#         with conn:
#             with conn.cursor() as curs:
#                 curs.execute("DROP TABLE IF EXISTS lph_out")
#                 curs.execute(
#                     "CREATE TABLE lph_out ("
#                     "calc_id serial PRIMARY KEY, "
#                     "block_name VARCHAR(10), "
#                     "func_name VARCHAR(20), "
#                     "calc_dt TIMESTAMP(3), "
#                     "add_db_dt TIMESTAMP(3) DEFAULT NOW(), "
#                     "input_value NUMERIC(10,4), "
#                     "result_value NUMERIC(20,4)); "
#                 )
#     finally:
#         conn.close()

# CREATE TABLE public.lph_out
# (
#     row_id serial NOT NULL,
#     calc_date date NOT NULL,
#     recording_date date NOT NULL,
#     steam_consumption real NOT NULL,
#     number_of_tubes integer NOT NULL,
#     heat_transfer real NOT NULL,
#     PRIMARY KEY (row_id),
#     CONSTRAINT row_id FOREIGN KEY (row_id)
#         REFERENCES public.condenser_in (row_id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
#         NOT VALID
# );

#
# def lph_out_add_value(calc_date, recording_date, steam_consumption, number_of_tubes, heat_transfer):
#     conn = psycopg2.connect(dbname='workwork', user='postgres', password='zaq123')
#     try:
#         with conn:
#             with conn.cursor() as curs:
#                 curs.execute(
#                     "INSERT INTO lph_out ("
#                     "calc_date, "
#                     "recording_date, "
#                     "steam_consumption, "
#                     "number_of_tubes, "
#                     "heat_transfer) "
#                     "VALUES (%s, %s, %s, %s, %s)",
#                     (calc_date, recording_date, steam_consumption, number_of_tubes, heat_transfer)
#                 )
#     finally:
#         conn.close()
#
#
# def condenser_out_add_value(calc_date, recording_date, water_temperature, saturation_temperature, saturation_pressure):
#     conn = psycopg2.connect(dbname='workwork', user='postgres', password='zaq123')
#     try:
#         with conn:
#             with conn.cursor() as curs:
#                 curs.execute(
#                     "INSERT INTO condenser_out ("
#                     "calc_date, "
#                     "recording_date, "
#                     "water_temperature, "
#                     "saturation_temperature, "
#                     "saturation_pressure) "
#                     "VALUES (%s, %s, %s, %s, %s)",
#                     (calc_date, recording_date, water_temperature, saturation_temperature, saturation_pressure)
#                 )
#     finally:
#         conn.close()
#
#
# def turbine_out_add_value(calc_date, recording_date, enthalpy_before, entropy_before, enthalpy_after, entropy_after,
#                           steam_temperature):
#     conn = psycopg2.connect(dbname='workwork', user='postgres', password='zaq123')
#     try:
#         with conn:
#             with conn.cursor() as curs:
#                 curs.execute(
#                     "INSERT INTO turbine_out ("
#                     "calc_date, "
#                     "recording_date, "
#                     "enthalpy_before, "
#                     "entropy_before, "
#                     "enthalpy_after, "
#                     "entropy_after, "
#                     "steam_temperature) "
#                     "VALUES (%s, %s, %s, %s, %s, %s, %s)",
#                     (calc_date, recording_date, enthalpy_before, entropy_before, enthalpy_after, entropy_after,
#                      steam_temperature)
#                 )
#     finally:
#         conn.close()
#
