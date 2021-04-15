"""
Обучающая библиотека.

Создана для изучения программирования на примере создания простых двумерных игр.
"""

from wrap import w1 #wrap_py launcher
from wrap_mENdRU import world, const, sprite, action

def add_sprite_dir(dir):
    """
    Добавляет папку в список мест, где будут искаться загружаемые спрайты.

    :param dir: Путь к папке со спрайтами. Например: C:\Temp
    """
    import wrap_data_source, wrap_py
    ds = wrap_data_source.file_data_source.FileDataSource(dir)
    wrap_py.site.sprite_data_sources.insert(0, ds)