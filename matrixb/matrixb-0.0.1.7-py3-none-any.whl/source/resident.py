# Copyright (c) 2019-2020 Kevin Crouse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @license: http://www.apache.org/licenses/LICENSE-2.0
# @author: Kevin Crouse (krcrouse@gmail.com)

import os
from .base import SourceBase

class Resident (SourceBase):

    def __init__(self, matrix, **kwargs):
        """
        Extends the SourceBase for resident objects in which the actual data is an array matrix. In this case, filename is an invalid parameter
        """
        if 'filename' in kwargs:
            raise Exception("Resident matrixb sources do not include filenames")

        self.source_data = matrix
        self._row_tracker = 0
        super().__init__(**kwargs)
        self.open()

    def open_stream(self):return

    def skip_rows(self, count):
        skipped = self.source_data[self._row_tracker:self._row_tracker + count]
        self._row_tracker += count
        return(skipped)

    def next_row(self):
        self._row_tracker += 1
        if self._row_tracker > len(self.source_data):
            raise StopIteration

        # check to see if there are values that are not none
        result = self.source_data[self._row_tracker-1]
        for item in result:
            if item is not None and (type(item) is not str or self.nonemptyre.match(item)):
                return(result)

        # if we get to this line, we are at a blank line, and so we are going to recursively look for the next row
        return(self.next_row())
