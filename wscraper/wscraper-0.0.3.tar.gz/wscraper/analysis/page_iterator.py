# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import os
import glob

from ..utility import *


class PageIterator:

    def __init__(self, xml_directory):
        self.path_list = sorted(glob.glob(os.path.join(xml_directory, "*.xml")))
        self.n_path = len(self.path_list)
        self.i_path = 0
        self.page_list = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.page_list) == 0:
            if len(self.path_list) == 0:
                raise StopIteration()

            path = self.path_list.pop(0)
            self.page_list = FileManager.load_xml(path).findall("page")
            self.i_path += 1

        return self.page_list.pop(0)

    def for_progress_manager(self):
        return [{ "name": "reader", "value": f"{self.i_path}/{self.n_path}" }]
