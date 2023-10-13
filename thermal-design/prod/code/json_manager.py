import json


def load_scheme(file_name: str) -> (str, dict):
    """
    Загрузка схемы
    :param file_name: имя файла со схемой в формате "name.json"
    :return: кортеж из строки ошибки и словаря данных
    """
    try:
        with open(file_name, 'r') as f:
            return '', json.load(f)
    except:
        return "Не удалось открыть файл", {}


def get_json_data(name: str) -> (str, dict):
    """
    Получение данных из JSON файла
    :param name: имя JSON файла в формате "name.json"
    :return: кортеж из строки ошибки и словаря данных
    """
    name += '.json'
    try:
        with open(name, 'r') as openfile:
            return '', json.load(openfile)
    except Exception:
        json_object = json.dumps({'users': []}, indent=4)
        with open(name, 'w') as outfile:
            outfile.write(json_object)
            return f'Файл "{name}" не найден. Создан новый пустой файл.', {}


def set_json_data(name: str, data: dict) -> None:
    """
    Запись данных в JSON файл
    :param name: имя JSON файла в формате "name.json"
    :param data: словарь данных
    """
    name += '.json'
    json_object = json.dumps(data, indent=4)
    with open(name, 'w') as outfile:
        outfile.write(json_object)
