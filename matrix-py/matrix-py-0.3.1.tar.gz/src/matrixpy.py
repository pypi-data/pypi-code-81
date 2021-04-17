#!/usr/bin/python3
"""matrix-py module to add, substract, multiply matrices.

Copyright (C) 2021 Fares Ahmed

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

# pylint: disable=C0103 # Variable name "m" is "iNvAlId-nAmE"

import argparse
import json


name = 'matrixpy'
__version__ = '0.3.1'
__all__     = ['Matrix']


class MatrixError(Exception):

    """Error for the Matrix Object invalid operations"""


class Matrix:

    """Matrix Object: add, sub, mul, and a lot more"""

    # Object Creation: START
    def __init__(self, matrix) -> None:
        """Initialize matrix object."""
        # Matrix([[1, 2, 3], [4, 5, 6]]) -> Row1 = (1 2 3), Row2 = (4 5 6)
        self.matrix = matrix

        # Matrix(3) -> (3x3) Zero Matrix
        if isinstance(matrix, int):
            self.matrix = Matrix.identity(matrix).to_list()

        # Matrix("1 2 3; 4 5 6") -> Row1 = (1 2 3), Row2 = (4 5 6)
        if isinstance(matrix, str):
            # input: Matrix("1 2 3; 4 5 6") | output: Matrix([[1, 2, 3], [4, 5, 6]])
            matrix = matrix.split(';')             # ["1 2 3", " 4 5 6"]
            matrix = list(map(str.lstrip, matrix)) # ["1 2 3", "4 5 6"]
            for i, nums in enumerate(matrix):      # [['1', '2', '3'], ['4', '5', '6']]
                matrix[i] = nums.split(' ')
            matrix = [list(map(int, matrix[i])) for i in range(len(matrix))]

            self.matrix = matrix

        self.rowsnum = len(self.matrix)
        self.colsnum = len(self.matrix[0])

    def __repr__(self):
        """Return the matrix size (string representation of the object)"""
        return '<{} ({}x{}) 0x{}x>'.format(self.__class__.__name__,
        self.rowsnum, self.colsnum,
        id(self))

    def __str__(self, dims=True):
        """Return the Matrix, the size of it (Activated when using print)"""
        for row in self.matrix:
            print(' '.join(map(str,row)))

        if dims:
            return "({}x{})".format(self.rowsnum, self.colsnum)

        return str()

    def __getitem__(self, rowcol):
        """Return matrix item | a_matrix[1, 2] 1->row 2->col"""
        # Return row if one argument (int) was given (M[1])
        if isinstance(rowcol, int):
            return Matrix(self.matrix).row(rowcol)

        # Return col if slice was given (M[:1])
        if isinstance(rowcol, slice):
            return Matrix(self.matrix).col(rowcol.stop)

        # Return Matrix item if 2 arguments (list) was given
        return self.matrix[rowcol[0]][rowcol[1]]

    def __contains__(self, item):
        """Return True if item in Object else False"""
        for row in self.matrix:
            if item in row:
                return True
        return False
    # Object Creation: END

    # Object Expressions: START
    def __pos__(self):
        """Positive operator: +A | Return the matrix * 1 (copy)"""
        result = list()

        for i in range(self.rowsnum):
            result.append([])
            for m in range(self.colsnum):
                result[i].append(+self.matrix[i][m])

        return Matrix(result)

    def __neg__(self):
        """Negative operator: -A. | Returns the matrix * -1"""
        result = [[-x for x in y] for y in self.matrix]

        return Matrix(result)
    # Object Expressions: END

    # Object Math operations: START
    def __add__(self, other):
        """Matrix Addition: A + B or A + INT."""
        if isinstance(other, Matrix):
            # A + B
            result = list()

            if (self.rowsnum != other.rowsnum or
                self.colsnum != other.colsnum):
                raise MatrixError('To add matrices, the matrices must have'
                ' the same dimensions')

            for m in range(self.rowsnum):
                result.append([])
                for j in range(self.colsnum):
                    result[m].append(self.matrix[m][j] + other.matrix[m][j])

        else:
            # A + INT
            result = list()

            for m in range(self.rowsnum):
                result.append([])
                for i in range(self.colsnum):
                    result[m].append(self.matrix[m][i] + other)

        return Matrix(result)

    def __sub__(self, other):
        """Matrix Subtraction: A - B or A - INT."""
        if isinstance(other, Matrix):
            # A + B
            result = list()

            if (self.rowsnum != other.rowsnum or
                self.colsnum != other.colsnum):
                raise MatrixError('To sub matrices, the matrices must have'
                ' the same dimensions')

            for m in range(self.rowsnum):
                result.append([])
                for j in range(self.colsnum):
                    result[m].append(self.matrix[m][j] - other.matrix[m][j])
        else:
            # A + INT
            result = list()

            for m in range(self.rowsnum):
                result.append([])
                for i in range(self.colsnum):
                    result[m].append(self.matrix[m][i] - other)

        return Matrix(result)

    def __mul__(self, other):
        """Matrix Multiplication: A * B or A * INT."""
        if isinstance(other, Matrix):
            # A * B
            if len(self.matrix[0]) != len(other.matrix):
                raise MatrixError('The number of rows in matrix A must be'
                ' equal to the number of columns in B matrix')

            # References:
            # https://www.geeksforgeeks.org/python-program-multiply-two-matrices
            result = [[sum(a * b for a, b in zip(A_row, B_col))
                            for B_col in zip(*other.matrix)]
                                    for A_row in self.matrix]
        else:
            # A * INT
            result = list()

            for m in range(self.rowsnum):
                result.append([])
                for i in range(self.colsnum):
                    result[m].append(self.matrix[m][i] * other)

        return Matrix(result)
    # Object Math opertaions: END

    # Object Manpulation: START
    def row(self, num: int, start=0):
        if num <= start-1: raise MatrixError('The matrix rows start from'
        f' {start} row(num) to start from 0')
        if num > start-1: num -= start

        try:
            return Matrix([self.matrix[num]])
        except IndexError:
            raise MatrixError('Matrix Index out of range')


    def col(self, num: int, start=0):
        if num <= start-1: raise MatrixError('The matrix cols start from'
        f' {start} col(num) to start from 0')
        if num > start-1: num -= start

        try:
            return Matrix([[row[num]] for row in self.matrix])
        except IndexError:
            raise MatrixError('Matrix Index out of range')


    def transpose(self: list):
        """Return a new matrix transposed"""
        result = [list(i) for i in zip(*self.matrix)]
        return Matrix(result)


    def to_list(self):
        """Convert Matrix object to a list"""
        return self.matrix
    # Object Manpulation: END

    # Booleon Expressions: START
    def is_square(self):
        """Check if the matrix is square"""
        if self.rowsnum == self.colsnum:
            return True
        else:
            return False


    def is_symmetric(self):
        """Check of the matrix is symmetric"""
        if self.matrix == (Matrix(self.matrix).transpose()).to_list():
            return True
        return False
    # Booleon Expressions: END

    # Pre Made Objects: START
    @staticmethod
    def identity(size: int):
        """Return a New Identity Matrix"""
        result = list()

        for i in range(size):
            result.append([0] * size)
            result[i][i] = 1

        return Matrix(result)


    @staticmethod
    def zero(size: int):
        """Return a New Zero Matrix"""
        return Matrix([[0] * size] * size)


    @staticmethod
    def diagonal(*numbers: int):
        """"Return a New diagonal Matrix"""
        result = list()

        for i, number in enumerate(numbers):
            result.append([0] * len(numbers))
            result[i][i] = number

        return Matrix(result)
    # Pre Made Objects: END


def main():
    """The CLI for the module"""
    parser=argparse.ArgumentParser(
        description = 'matrix-py module to add, substract, multiply'
        'matrices.',
        epilog = 'Usage: .. -ma "[[1, 2, 3], [4, 5, 6]]" -op "+" -mb'
        ' "[[7, 8, 9], [10, 11, 12]]"')

    parser.add_argument('-v', '--version',
        action="version",
        version=__version__,
    )

    parser.add_argument('-s', '--size',
        type=json.loads,
        metavar='',
        help='Size of A Matrix'
    )

    parser.add_argument('-t', '--transpose',
        type=json.loads,
        metavar='',
        help='Transpose of A Matrix (-t "[[1, 2, 3], [4, 5, 6]]")'
    )

    parser.add_argument('-ma', '--matrixa',
        type=json.loads,
        metavar='',
        help='Matrix A (.. -ma "[[1, 2, 3], [4, 5, 6]]")'
    )

    parser.add_argument('-op', '--operator',
        type=str,
        metavar='',
        help='Operator (.. -op "+", "-", "*")'
    )

    parser.add_argument('-mb', '--matrixb',
        type=json.loads,
        metavar='',
        help='Matrix B (.. -mb "[[1, 2, 3], [4, 5, 6]]")'
    )

    parser.add_argument('-I', '--identity',
        type=int,
        metavar='',
        help='Identity (.. -I 3)'
    )

    parser.add_argument('-i', '--int',
        type=int,
        metavar='',
        help='Integer (.. -i 5)'
    )

    parser.add_argument('-diag', '--diagonal',
        type=json.loads,
        metavar='',
        help='Diagonal (.. -diag [1, 2, 3, 4])'
    )

    args = parser.parse_args()

    if args.size:
        print(Matrix(args.size))

    elif args.transpose:
        print(Matrix(args.transpose).transpose())

    elif args.matrixa:
        if args.matrixb:
            b = Matrix(args.matrixb)
        elif args.int:
            b = args.int
        elif args.identity:
            b = Matrix.identity(args.identity)
        elif args.diagonal:
            b = Matrix.diagonal(args.diagonal)

        if args.operator == '+':
            print(Matrix(args.matrixa) + b)
        elif args.operator == '-':
            print(Matrix(args.matrixa) - b)
        elif args.operator == '*':
            print(Matrix(args.matrixa) * b)
        else:
            raise SyntaxError('The avillable operations are +, -, *')
    else:
        return parser.print_help()


if __name__ == '__main__':
    main()
