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

import re

from ..matrix import Matrix

class SourceBase():
    nonemptyre = re.compile(r'\s*\S')

    @property
    def filename(self): return(self._filename)

    @property
    def worksheets(self):
        """ Worksheets returns a list of worksheet names available for this matrix class. By default, and if it is not a traditional spreadsheet with multiple possible worksheets, it should return a 1-element list of ['<default>']. Otherwise, when subclassing MatrixSource, the programmer should defined _worksheets based on the possible values """
        return(self._worksheets)

    @property
    def worksheet(self): return(self._worksheet)
    # worksheets are common enough that we will keep it in the baseclass

    @worksheet.setter
    def worksheet(self, worksheet):
        raise Exception("MatrixSource " + self.__class__.__name__ + " has not instatiated a way to load a specific worksheet")

    @property
    def header_ignore(self): return(self._header_ignore)

    @property
    def postheader_ignore(self): return(self._postheader_ignore)

    @property
    def footer_ignore(self): return(self._footer_ignore)

    @property
    def ignored_header(self): return(self._ignored_header)

    @property
    def ignored_postheader(self): return(self._ignored_postheader)

    @property
    def ignored_footer(self): return(self._ignored_footer)

    def __init__(self, filename=None, worksheet=None, header_ignore=0, postheader_ignore=0, footer_ignore=0, **matrixparams):
        self._filename = filename
        self._worksheets = ['<default>']
        self._worksheet = worksheet
        self._header_ignore = header_ignore
        self._postheader_ignore = postheader_ignore
        self._footer_ignore = footer_ignore
        self._ignored_header = self._ignored_postheader = self._ignored_footer = None
        self.matrixparams = matrixparams

    def __iter__(self):
        return(self)

    def __next__(self):
        return(self.next_row())

    def open(self):
        self.open_stream()
        # HEADER IGNORE - are there lines to skip?
        if self.header_ignore:
            self._ignored_header = self.skip_rows(self.header_ignore)

    def skip_postheader(self):
        if self.postheader_ignore:
            self._ignored_postheader = self.skip_rows(self.postheader_ignore)

    def next_row(self):
        raise Exception("Matrix Source is an abstract base class! next is not implemented in subclass "+self.__class__.__name__+"!")

    def open_stream(self):
        raise Exception("Matrix Source is an abstract base class! open_stream is not implemented in subclass "+self.__class__.__name__+"!")

    def skip_rows(self, count):
        raise Exception("Matrix Source is an abstract base class! skip_rows is not implemented in subclass "+self.__class__.__name__+"!")

    def get_matrix(self, worksheet=None, **additionalparams):
        """Gets the matrixb.Matrix for the current parameters.

        Args:
            worksheet (str): Specifies a worksheet name, for sources that can have multiple worksheet matrices. The default is the worksheet property; if None and there are multiple worksheets, it will choose either the active or default, based on the functions available in the underlying handler class.

            All other keyword parameters will be passed directly to the matrix init call alongside any unrecognized parameters that were passed into the source's init call. It is therefore possible that invalid parameters passed into the SourceBase constructor will lead to a deferred Exception when get_matrix is called.

        Returns:
            A matrixb.Matrix given the current parameters.
        """

        if worksheet:
            self.worksheet = worksheet
            self.open()

        for k, v in self.matrixparams.items():
            if k not in additionalparams:
                additionalparams[k] = v
        return(Matrix(source=self, **additionalparams))


    @classmethod
    def export_to(self, matrix, destination, topmatter=None, autosize=False):
        """The export_to class method is designed to export a matrixb matrix to the source type. This method is abstract in the base class, and implementers should override it to export correctly. In many cases, this will be delegated to from the Matrixb.export() method, which attempts to identify the export based on the file extension.

        Args:
            matrix (matrixb.Matrix): The Matrix object to export.
            destination: The full path to the destination to export the data to.
            topmatter (list|str, optional): A line or lines to appear above the exported matrix.
            autosize (bool): This parameter may be removed in the future - the original intent was for Excel and ODS files to autosize the columns, but that's not very generic.

        TODO: Changing autosize to a more generic format configuration may be in order.
        """
        raise Exception('export_to must be defined in the subclass. It is abstract in SourceBase.')

    def __getstate__(self):
        """ To pickle/serialze the csv source, we delete the stream and filehandle - this will allow future restored objects to get things like the source filename, but attempts to access the source object will fail. """
        state = self.__dict__.copy()
        return(state)

    def __setstate__(self, state):
        """ Set/load the state based on serialized data. In some cases, open files or data handles may not be set."""
        self.__dict__ = state
