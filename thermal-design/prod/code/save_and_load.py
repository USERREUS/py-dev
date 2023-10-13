from PyQt6.QtWidgets import QFileDialog, QMessageBox

import DB
from main_interfaces import IMainWindow, IBlockGfx, IConnector, IScene, BlockModelType as BMT
from block_graphics import Link, Generator, Calculator, Display


def link_to_dict(link: Link) -> dict:
    """
    Сериализация связи
    :param link: объект линии связи
    :return: словарь описания связи
    """
    return {
        'x0': link.line().x1(),
        'y0': link.line().y1(),
        'x1': link.line().x2(),
        'y1': link.line().y2()
    }


def connector_to_dict(connector: IConnector) -> [dict]:
    """
    Сериализация соединителя
    :param connector: объект соединителя
    :return: список словарей связей
    """
    if connector.is_dst_complete():
        links_serialize = []
        for link in connector.get_links():
            links_serialize.append(link_to_dict(link))
        return links_serialize
    return []


def block_to_dict(block: IBlockGfx) -> dict:
    """
    Сериализация блока
    :param block: объект блока
    :return: словарь описания блока
    """
    result = {
        'x': block.x(),
        'y': block.y(),
        'width': block.rect().width(),
        'height': block.rect().height(),
        'noi': block.get_noi(),
        'noo': block.get_noo(),
        'title': block.get_title(),
        'id': block.get_id(),
        'model_type': block.get_model_type().value
    }

    if block.get_connector():
        if block.get_connector().get_destination():
            result['dst'] = block.get_connector().get_destination().get_id()
            result['links'] = connector_to_dict(block.get_connector())

    return result


def scene_save(scene: IScene) -> None:
    """
    Сохранение схемы
    :param scene: объект контроллера области редактирования
    """
    schema = []
    for block in scene.get_blocks():
        schema.append(block_to_dict(block))
    DB.set_json_data('save110523', {
        'about': 'About us / Time / Date / Comments / User',
        'schema': schema
    })


def scene_load(scene: IScene, data: dict) -> None:
    """
    Загрузка схемы
    :param scene: объект контроллера области редактирования
    :param data: словарь описания схемы
    """
    scene.clear()
    for item in data['schema']:
        x = item['x']
        y = item['y']
        id = item['id']
        model_type = item['model_type']
        if model_type == BMT.generator.value:
            block = Generator(scene, id, x, y)
        elif model_type == BMT.calculator.value:
            block = Calculator(scene, id, x, y)
        else:
            block = Display(scene, id, x, y)
        scene.add_block(block)
        if 'links' in item:
            for link in item['links']:
                new_link = Link(link['x0'], link['y0'], link['x1'], link['y1'], block.get_connector())
                block.get_connector().get_links().append(new_link)  # !!! возможно не работает
                scene.addItem(new_link)

    for item in data['schema']:
        if 'dst' in item:
            src_id = item['id']
            src = scene.block_by_id(src_id)
            dst_id = item['dst']
            dst = scene.block_by_id(dst_id)
            scene.create_link(src_id, dst_id)
            src.get_connector().destination_complete = True
            src.get_connector().destination = dst
            src.get_connector().hide()


def file_open(window: IMainWindow) -> None:
    """
    Открытие файла для загрузки схемы
    :param window: объект главного окна программы
    """
    file_name = QFileDialog.getOpenFileName(parent=None,
                                            caption="Выберите файл",
                                            filter="json (*.json)")[0]
    msg, data = DB.load_scheme(file_name)
    if data:
        scene_load(window.get_scene(), data)
    else:
        QMessageBox.critical(window, "Схема", msg)
