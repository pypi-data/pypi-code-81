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
import os
class XLS(SourceBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._row_tracker = None
        self.xlsheet = None

    def open_stream(self):
        import xlrd
        self.workbook = xlrd.open_workbook(os.path.expanduser(self.filename))
        self._worksheets = self.workbook.sheet_names()
        if self.worksheet:
            self.xlsheet = self.workbook.sheet_by_name(self.worksheet)
        else:
            self.xlsheet = self.workbook.sheet_by_index(0)
            self.worksheet = self.xlsheet.name
        self._row_tracker = 0

    @property
    def worksheet(self): return(self._worksheet)

    @worksheet.setter
    def worksheet(self, worksheet):
        self._worksheet = worksheet
        self.xlsheet = self.workbook.sheet_by_name(worksheet)


    def skip_rows(self, count):
        if not self.xlsheet:
            self.open()
        if self._row_tracker + count > self.xlsheet.nrows:
            raise IndexError("Asked to skip " + str(count) + " rows from current row ("+
                             str(self._row_tracker)+"), but there are not that many rows in the worksheet")
        skipped = []
        for row in range(count):
            skipped.append(list(map(lambda col: self.xlsheet.cell(self._row_tracker,col).value,
                                    range(self.xlsheet.ncols))))
            self._row_tracker += 1
        return(skipped)

    def next_row(self):
        if not self.xlsheet:
            self.open()
        while self._row_tracker < self.xlsheet.nrows:
            hasText = False
            row = []
            for i_col in range(self.xlsheet.ncols):
                v = self.xlsheet.cell(self._row_tracker, i_col).value
                if type(v) is str:
                    if self.nonemptyre.search(v):
                        hasText = i_col+1
                    else:
                        v = None
                elif type(v) is not None:
                    hasText = i_col+1
                else:
                    v = None
                # add the cell value to the row
                row.append(v)

            self._row_tracker += 1

            if hasText:
                return(row[:hasText])

        # if we get here, we are at EOF
        raise StopIteration


    @classmethod
    def export_to(self, matrix, filename, topmatter=None, autosize=None):
        """The export_to class method to export a matrixb matrix to a modern Excel ('.xlsx') file.

        Args:
            matrix (matrixb.Matrix): The Matrix object to export.
            filename (str): The full path to send the file.
            topmatter (list|str, optional): Lines to appear above the exported table.
            autosize (bool): TODO.
        """
        import xlwt

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Matrix Export')

        irow = 0
        # handle topmatter
        if topmatter:
            if type(topmatter) in (list, tuple):
                for rowdata in topmatter:
                    ws.write(irow, 0, rowdata)
                    irow += 1
            else:
                ws.write(irow, 0, rowdata)
                irow += 1

        # handle column headers, with some formatting
        headerstyle = xlwt.XFStyle()

        headerfont = xlwt.Font()
        headerfont.bold = True
        headerfont.height = 12
        headerstyle.font = headerfont

        headerborder = xlwt.Borders()
        headerborder.bottom = 2
        headerstyle.border = headerborder

#        headerborder = openpyxl.styles.Border(bottom=openpyxl.styles.Side(border_style='thick',color='000000'))
        #headerfont = openpyxl.styles.Font(bold=True, size=12)
        for icol in range(len(matrix.columns)):
            cell = ws.write(irow, icol, matrix.columns[icol], headerstyle)
        irow += 1

        for rowdata in matrix:
            for icol, val in enumerate(rowdata):
                ws.write(irow, icol, val)
            irow += 1
        wb.save(filename)

    def __getstate__(self):
        """ To pickle/serialze the csv source, we delete the stream and filehandle - this will allow future restored objects to get things like the source filename, but attempts to access the source object will fail. """
        state = super().__getstate__()
        del state['workbook']
        del state['xlsheet']
        return(state)
