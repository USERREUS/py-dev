import datetime as datetime
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

dbname = "test"
dbuser = "postgres"
password = "admin"

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


# Создание таблицы для сохранения результатов вычисления
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


# Добавление результата вычисления в БД
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


# Добавление результата вычисления в таблицу турбины
def add_value_lph(result, name_of_table):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"INSERT INTO {name_of_table} ("
                    "steam_consumption, "
                    "parallel_pipes, "
                    "heat_transfer_coefficient)"
                    "VALUES (%s, %s, %s)",
                    (result[0], result[1], result[2])
                )
    finally:
        conn.close()

# Получаение значений из базы данных
def get_data(name_of_data, name_of_column=None):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                if name_of_column:
                    curs.execute(f"SELECT {name_of_column} FROM {name_of_data}")
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
    data_table = []
    for record in records:
        data_row = []
        for item in record:
            if item == name:
                data_row.append(record[item])
        data_table.append(data_row)
    return data_table


# Получить заголовки колонок из таблицы
def get_column_names(recors):
    column_names = []
    for item in recors[0]:
        column_names.append(item)
    return column_names


# (НЕ ИСПОЛЬЗУЕТСЯ)
def get_data_timediff(time_interval) -> [str]:
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=password)
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT result_value FROM time_calculation WHERE calc_dt > %s", (time_interval,))
                return curs.fetchall()
    finally:
        conn.close()


# (НЕ ИСПОЛЬЗУЕТСЯ)
def LAST_MINUTE():
    dt_now = datetime.datetime.now().timetuple()
    dt_new = datetime.datetime(dt_now[0], dt_now[1], dt_now[2], dt_now[3], dt_now[4] - 1, dt_now[5], dt_now[6])
    return dt_new


# Типа словарь с для хранения информации в кириллице
pairs = {
    'heating_vapor_pressure': ('P_п', 'МПа'),
    'heating_steam_temperature': ('t_п', '°С'),
    'saturation_temperature': ('t_н', '°С'),
    'heated_condensate_pressure': ('p_к', 'МПа'),
    'condensate_temperature': ('t_вх', '°С'),
    'condensate_flow': ('G_к', 'кг/с'),
    'efficiency_factor': ('etta_п', ''),
    'steam_consumption': ('D_п', 'кг/с'),
    'parallel_pipes': ('z_1', ''),
    'heat_transfer_coefficient': ('k', 'Вт/(м^2*K)'),
    'created_date': ('Дата создания', '')
}


# Получить значение из словаря по заголовку колонки
def to_readable_data(value):
    return pairs[value]


# Получить заголовок колонки по значению из словаря
def readable_to_data(value):
    for key in pairs:
        if value == pairs[key][0]:
            return key

# create_table()
# add_value("T", "F", datetime.datetime.now(), 5, 25)
# add_value("T", "F", datetime.datetime.now(), 6, 36)
# add_value("T", "F", datetime.datetime.now(), 7, 49)
# # print(parse_data(get_data_timediff(LAST_MINUTE())))
# data = get_data('lph_out_data')
# print(parse_data_for_name(data, 'created_date'))
# print(get_column_names(data))
# print(readable_to_data('z_1'))

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
