import os
from pathlib import Path
from wrap_data_source import data_source, costume_loader, settings


class FileDataSource(data_source.DataSource):
    def __init__(self, base_path, sprite_types_subfolder=None, sprite_type_costumes_subfolder=None):

        self._base_path = os.path.abspath(base_path)

        # path to sprite types
        self._sprite_types_path = self._join_if_not_none(self._base_path, sprite_types_subfolder)

        # path to costume of any sprite type
        self._sprite_type_costumes_subfolder = sprite_type_costumes_subfolder

    @staticmethod
    def _join_if_not_none(base_path, add_path):
        return base_path if add_path is None else os.path.join(base_path, add_path)

    def _get_sprite_type_path(self, sprite_type_id):
        return os.path.join(self._sprite_types_path, str(sprite_type_id))

    def _get_sprite_type_costume_path(self, sprite_type_id):
        sprite_type_path = self._get_sprite_type_path(sprite_type_id)

        return self._join_if_not_none(sprite_type_path, self._sprite_type_costumes_subfolder)


    #### DataSource

    @staticmethod
    def _sprite_types_generator(path, extended_data=False):
        po = Path(path)
        for p in po.iterdir():

            if not extended_data:
                yield p.name
            else:
                yield {
                    'name': p.name,
                    'path': str(p)
                }

    @staticmethod
    def _costumes_generator(path, extended_data=False):
        costume_list=[]

        po = Path(path)
        if not po.exists():
            return
        for p in po.iterdir():
            if p.is_dir(): continue

            if p.suffix not in settings.PYGAME_SUPPORTS_IMAGE_EXTS:
                continue

            #ignore files with same names but diff exts
            if p.name in costume_list:
                continue

            costume_list.append(p.name)
            if not extended_data:
                yield p.stem
            else:
                yield {
                    'name': p.stem,
                    'path': str(p)
                }

    def get_sprite_types_enumerator(self, extended_data=False):
        assert os.path.exists(self._sprite_types_path)
        return self._sprite_types_generator(self._sprite_types_path, extended_data)

    def get_sprite_type_costumes_enumerator(self, sprite_type_id, extended_data=False):
        costumes_path = self._get_sprite_type_costume_path(sprite_type_id)
        return self._costumes_generator(costumes_path)

    def get_sprite_type_costume_data(self, sprite_type_id, costume_id):
        """
        Should return False if loading failed.

        :param sprite_type_id:
        :param costume_id:
        :return:
        """

        costumes_path = self._get_sprite_type_costume_path(sprite_type_id)
        for i in self._costumes_generator(costumes_path, True):
            if i['name'] == costume_id:
                return costume_loader.Costume_loader.load_data(i['path'])

        return False