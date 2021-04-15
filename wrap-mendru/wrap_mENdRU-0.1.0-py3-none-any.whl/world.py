"""
Этот модуль содержит команды, необходимые для создания и изменения игрового мира.
Эти команды, например, позволяют изменить размер окна или поменять его заголовок.
"""


def create_world(width: int, height: int, start_pos_x: int = None, start_pos_y: int = None):
    """
    Создает игровое окно. Можно задать размеры и положение окна.

    :param width: ширина окна
    :param height: высота окна
    :param start_pos_x: смещение окна от левого края монитора.
    :param start_pos_y: смещение окна от верхнего края монитора.
    :return: None
    """

    return world.create_world(width, height, start_pos_x, start_pos_y)


def change_world(width: int, height: int):
    """
    Меняет размеры игрового окна.

    :param width: Новая ширина окна
    :param height: Новая высота окна
    :return: None
    """
    return world.change_world(width, height)


def set_title(title: str):
    """
    Меняет заголовок окна игры.

    :param title: Новый заголовок окна.
    :return: None
    """
    return app.set_title(title)


def get_title():
    """
    :return: Возвращает строку - текущий заголовок окна игры.
    """
    return app.get_title()


def set_back_color(r: int, g: int, b: int):
    """
    Устанавливает фоновый цвет окна. r, g, b - цвет в формате RGB.
    """
    return world.set_world_background_color_rgb(r, g, b)


def set_back_image(path: str):
    """
    Устанавливает картинку в качестве рисунка окна.

    :param path: Строка. Путь к картинке.
    :return: None
    """
    return world.set_world_background_image(path)


def clear_back_image():
    """
    Очищает установленную картинку окна.
    """
    return world.clear_world_background_image()


def w1():
    global world, app
    from wrap_py import world, app


w1()
