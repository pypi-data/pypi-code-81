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

from .base import SourceBase

class GoogleSheet(SourceBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = None

    @property
    def worksheet(self): return(self._worksheet)

    @worksheet.setter
    def worksheet(self, worksheet):
        self._worksheet = worksheet
        self.xlsheet = self.googlesheet.get_worksheet(worksheet)

    def open_stream(self):
        try:
            import googleapps
        except:
            raise Exception("matrixb.source.GoogleSheet requires googleapps, which is not yet released by the author. Please contact Kevin Crouse for details")
        if type(self.filename) is str:
            self.googlesheet = googleapps.sheets.get(self.filename)
            self._worksheets = self.googlesheet.worksheet_titles
            if self.worksheet:
                self.googlews = self.googlesheet.get_worksheet(self.worksheet)
            else:
                self.googlews = self.googlesheet.active
                self._worksheet = self.googlews.title
        else:
            # we expect it here to be an actual google sheet object
            if type(self.filename).__module__ == 'googleapps.sheets.spreadsheet':
                self.googlesheet = self.filename
                self.googlews = self.filename.active
            elif type(self.filename).__module__ == 'googleapps.sheets.worksheet':
                self.googlesheet = self.filename.spreadsheet
                self.googlews = self.filename
            else:
                raise Exception("Unknown object provided to GoogleSheet Matrix Importer")

        self.row = 0

    def skip_rows(self, count):
        if self.row is None:
            self.open()
        skipped = []
        for i in range(count):
            if not self.row < self.googlews.nrows:
                break
            skipped.append(self.googlews.celldata[self.row])
            self.row += 1
        return(skipped)

    def next_row(self):
        if self.row is None:
            self.open()
        hasText = False
        while True:
            if not self.row < self.googlews.nrows:
                raise(StopIteration)

            row = self.googlews.celldata[self.row]
            self.row += 1
            for i in range(len(row)):
                if type(row[i]) is str:
                    if self.nonemptyre.search(row[i]):
                        hasText = i+1
                        # -- don't break because we want to convert empty cells
                        # later in the row to None
                    else:
                        row[i] = None
                elif type(row[i]) in (int, float):
                    hasText = i+1

            if hasText is not False:
                return(row[:hasText])
