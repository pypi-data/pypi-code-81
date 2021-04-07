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

class CSV (SourceBase):

    def __init__(self, *args, encoding='utf-8-sig', csvdialect='excel', **kwargs):
        """
        Extends the SourceBase and includes all arguments provided there.  In addition, provides the following csv-only arguments:

        Args:
            encoding (str): Forwards to the encoding on to the file open() command. Default is 'utf-8-sig', which is useful to strip out Byte-Order-Marker u'feff' which happens for certain generated csv files in windows. 'latin_1' is a common alternative when 'utf-8-sig' leads to issues.
            csvdialect (str): Forwards to the dialect parameter for csv.reader. Default is 'excel'.
        """
        super().__init__(*args, **kwargs)
        self.encoding = encoding
        self.csvdialect = csvdialect
        self.stream = None

    def open_stream(self):
        import csv
        self.fh = open(os.path.expanduser(self.filename), 'r', newline='', encoding=self.encoding)
        self.stream = csv.reader(self.fh, dialect=self.csvdialect)

    def skip_rows(self, count):
        skipped = []
        for i in range(count):
            skipped.append(next(self.stream))
        return(skipped)

    def next_row(self):
        """ next() for csv matrix sources, which translates empty strings to None and skips blank lines."""

        if not self.stream:
            self.open()

        hasText = False
        while True:
            try:
                row = next(self.stream)
            except StopIteration:
                self.fh.close()
                raise(StopIteration)

            # csvreader should raise a StopException exception at EOF so we don't have to

            for i in range(0, len(row)):
                if row[i] is not None:
                    if type(row[i]) is str:
                        if self.nonemptyre.search(row[i]):
                            hasText = i+1
                            # -- don't break because we want to convert empty cells
                            # later in the row to None
                        else:
                            row[i] = None
                    elif type(row[i]) in (int, float):
                        hasText = i+1

            if hasText:
                return(row[:hasText])

    @classmethod
    def export_to(self, matrix, filename, topmatter=None, autosize=None):
        """The export_to class method to export a matrixb matrix to a CSV file.

        Args:
            matrix (matrixb.Matrix): The Matrix object to export.
            filename (str): The full path to send the file.
            topmatter (list|str, optional): Lines to appear above the exported table.
            autosize: This parameter is not used, only maintained for consistency with the export_to interface.
        """

        with open(filename, 'w') as fh:
            if topmatter:
                if type(topmatter) in (list, tuple):
                    fh.writelines(topmatter)
                else:
                    fh.write('"' + topmatter + '"' + "\n")
            fh.write(','.join(self.export_cell(colname) for colname in matrix.columns) + "\n")
            for row in matrix:
                fh.write(','.join(self.export_cell(cell) for cell in row) + "\n")


    @classmethod
    def export_cell(self, cell):
        if cell is None:
            return('')
        if type(cell) is str:
            # quotes need to be substitutded
            cell = cell.replace('"', '""')
            if "\n" in cell or "," in cell or "\r" in cell:
                return('"' + str(cell) + '"')
        return(str(cell))


    def __getstate__(self):
        """ To pickle/serialze the csv source, we delete the stream and filehandle - this will allow future restored objects to get things like the source filename, but attempts to access the source object will fail. """
        state = super().__getstate__()
        del state['stream']
        del state['fh']
        return(state)
