# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import os
import glob


class LineSentenceIterator:

    def __init__(self, pls_directory):
        self.path_list = sorted(glob.glob(os.path.join(pls_directory, "*.txt")))
        self.n_path = len(self.path_list)
        self.i_path = 0
        self.line_list = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.line_list) == 0:
            if len(self.path_list) == 0:
                raise StopIteration()

            path = self.path_list.pop(0)

            with open(path, "r") as f:
                self.line_list = f.readlines()

            self.i_path += 1

        return self.line_list.pop(0)
