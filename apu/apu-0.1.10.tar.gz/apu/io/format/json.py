""" handling json files """
from typing import Any

from json import loads, dumps, load
from apu.io.fileformat import FileFormat


# pylint: disable=C0301
class JSONL(FileFormat):
    """ json line files """
    def read(self):
        """ read json line files """
        with open(self._filepath.absolute(), encoding="utf8",
                  mode="r") as jsonl_file:
            self.data = [
                loads(line, **self._args) for line in jsonl_file
                if len(line) > 0
            ]

        return self.data

    def write(self):
        """ read json line """
        with open(self._filepath, mode="w", encoding="utf8") as jsonl_file:
            self._args["indent"] = None  # JSON has to be on one line!
            if "sort_keys" not in self._args:
                self._args["sort_keys"] = True
            if "separators" not in self._args:
                self._args["separators"] = (",", ": ")
            if "ensure_ascii" not in self._args:
                self._args["ensure_ascii"] = False
            for line in self.data:
                str_ = dumps(line, **self._args)
                jsonl_file.write(str_)
                jsonl_file.write("\n")
        return self.data

    @classmethod
    def suffix(cls):
        """ json line suffix """
        return tuple(".jsonl")


class JSON(FileFormat):
    """ json file """
    def read(self):
        """ read json file """
        with open(self._filepath.absolute(), encoding="utf8",
                  mode="r") as json_file:
            self.data: Any = load(json_file, **self._args)

        return self.data

    def write(self):
        """ write json files """
        with open(self._filepath, mode="w", encoding="utf8") as json_file:
            if "indent" not in self._args:
                self._args["indent"] = 4
            if "sort_keys" not in self._args:
                self._args["sort_keys"] = True
            if "separators" not in self._args:
                self._args["separators"] = (",", ": ")
            if "ensure_ascii" not in self._args:
                self._args["ensure_ascii"] = False
            str_ = dumps(self.data, **self._args)
            json_file.write(str_)
        return self.data

    @classmethod
    def suffix(cls):
        """ json suffix """
        return tuple(".json")
