""" csv file read write """

import csv
from typing import Union, List, Dict

from apu.io.fileformat import FileFormat
from apu.datastructures.enhanced_list import EnhancedList

class CSV(FileFormat):
    """ read write csv files """
    def read(self):
        """ read a csv file """
        if "delimiter" not in self._args:
            self._args["delimiter"] = ","
        if "quotechar" not in self._args:
            self._args["quotechar"] = "\""
        if "skiprows" not in self._args:
            self._args["skiprows"] = []
        if isinstance(self._args["skiprows"], int):
            self._args["skiprows"] = list(range(self._args["skiprows"]))
        if "format" in self._args:
            format_ = self._args["format"]
            self._args.pop("format", None)
        else:
            format_ = "default"

        skiprows = self._args["skiprows"]
        self._args.pop("skiprows", None)

        with open(self._filepath.absolute(), encoding="utf8", mode="r") \
            as csv_file:
            if format_ == "default":
                reader = csv.reader(csv_file, **self._args)
                data_tmp = EnhancedList(list(reader))
                self.data: Union[List, Dict] = data_tmp.reject_indices(skiprows)
            elif format_ == "dict":
                reader = csv.DictReader(csv_file, **self._args)
                self.data = list(reader)
            else:
                raise NotImplementedError(f"format \"{format_}\" unkown")

        return self.data

    def write(self):
        """ write a csv file"""
        with open(self._filepath, mode="w", encoding="utf8") as csv_file:
            if "delimiter" not in self._args:
                self._args["delimiter"] = ","
            if "quotechar" not in self._args:
                self._args["quotechar"] = "\""

            writer = csv.writer(csv_file, **self._args)
            writer.writerows(self.data)
        return self.data

    @classmethod
    def suffix(cls):
        return tuple(".cvs")
