# file matrixb/iterator.py

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

class MatrixIterator():
    """ Defines the iterator class for a Matrix. """

    def __init__(self, matrix):
        self.matrix = matrix
        # Because the underlying data source of the matrix may be present or may be in the process of being loaded,
        # we use the _topindex to track where the iterator is in the iteration. This allows trivial implementation
        # of the top() function, but is more substantially necessary in the implementation of __next__.
        self._topindex = 0

    def __iter__(self):
        return(self)

    def __next__(self):
        # Case 1: The Matrix data source has already loaded beyond the next row, and so we merely increment _topindex and return the already loaded row
        if self._topindex < self.matrix.rows_loaded:
            self._topindex += 1
            return(self.matrix[self._topindex-1])
        # Invariant: The row requested by __next__() is not already available in the underlying Matrix data source.

        # Case 2: The entire data source has been loaded, and thus there is no next row, so stop iteration.
        if self.matrix.loaded:
            raise StopIteration

        # Case 3: We have no knowledge about the next row, so attempt to load it from the underlying data source.
        #   Note: self.matrix.load_next() raises stop iteration and sets self.matrix.loaded to true if there is no next row.

        # NOTE: This was originally a while statement, but I don't understand why.
        # TODO: Find out why. The following is a temporary error to determine when the above block would potentially
        # lead to a different result than the while loop version
        #while self.matrix.rows_loaded <= self._topindex:
        #    row = self.matrix.load_next()
        if self._topindex != self.matrix.rows_loaded:
            raise Exception("CASE DISCOVERED: INVESTIGATE WHEN THE MATRIX ITERATOR TOPINDEX WOULD BE DIFFERENT THAN ROWS LOADED IN THIS CASE")
        #
        #

        row = self.matrix.load_next()
        self._topindex += 1


        return(row)

    def top(self):
        """ Look at the next row, but do not actually iterate over it. This is an extension of the required Python iterator definition. """

        if self._topindex < self.matrix.rows_loaded:
            return(self.matrix[self._topindex])
        elif self.matrix.loaded:
            raise IndexError("Iterator has exceeded all iterations; there is no new top item")

        row = self.matrix.load_next()
        return(row)
