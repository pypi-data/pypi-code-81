""" reading and writing yaml files """

from yaml import safe_load, dump
from apu.io.fileformat import FileFormat


class YAML(FileFormat):
    """ reading and writing yaml files"""
    def read(self):
        """ open a yaml file and read the data into the buffer """
        with open(self._filepath.absolute(), encoding="utf8",
                  mode="r") as yaml_file:
            self.data = safe_load(yaml_file)
        return self.data

    def write(self):
        """ write the data into a data sink """
        with open(self._filepath, mode="w", encoding="utf8") as yaml_file:
            dump(self.data,
                 yaml_file,
                 default_flow_style=False,
                 allow_unicode=True)

        return self.data

    @classmethod
    def suffix(cls):
        """ yaml suffix """
        return (".yaml", ".yml")
