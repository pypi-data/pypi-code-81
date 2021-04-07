from typing import Union

import numpy as np
import pandas as pd
from swissarmykit.lib.baseobject import BaseObject

from swissarmykit.viz.numpy_base import NumpyBase


class Numpy(NumpyBase, BaseObject):

    data: np.ndarray

    def __init__(self, data=None, is_one=None):
        super().__init__()
        if isinstance(data, np.ndarray):
            if is_one !=None:
                if is_one:
                    self.data = Numpy.ones(data, is_one=is_one, is_like=True)
                else:
                    self.data = Numpy.ones(data, is_one=is_one, is_like=True)
            else:
                self.data = data
        elif isinstance(data, tuple) or isinstance(data, int):
            if is_one != None:
                if is_one:
                    self.data = Numpy.ones(data, is_one=is_one)
                else:
                    self.data = Numpy.ones(data, is_one=is_one)
            else:
                self.data = np.ndarray(data if isinstance(data, tuple) else (data,))

        self._object = self.data

    def reshape(self, *args):
        ''' reshape '''
        return Numpy(self.data.reshape(*args))


    def mean(self, axis=0):
        ''' Compute the arithmetic mean along the specified axis. '''
        return self.data.mean(axis)

    def sort(self):
        self.data.sort()
        return self

    def repeat(self, *args):
        return Numpy(self.data.repeat(*args))

    def get_shape(self):
        return self.data.shape

    def get_ndim(self):
        ''' get number dimension'''
        return self.data.ndim

    def get_dtype(self):
        return self.data.dtype

    def issubdtype(self, type: np.typename):
        return np.issubdtype(self.data.dtype, type)

    def get_type(self):
        return type(self.data)

    def concatenate(self, arr, axis=0):
        return Numpy(np.concatenate([self.data, arr], axis=axis))


    def flatten(self):
        ''' always returns a copy.     https://stackoverflow.com/questions/28930465/what-is-the-difference-between-flatten-and-ravel-functions-in-numpy
        Return a copy of the array collapsed into one dimension.
        '''
        return Numpy(self.data.flatten())

    def ravel(self):
        '''  same as flatten. but ravel will often be faster since no memory is copied        '''
        self.data.ravel()
        return self



    @staticmethod
    def ones(shape, is_one=True, is_like=False, dtype=None, order='C'):
        '''
            empty_like: Return an empty array with shape and type of input.
            zeros_like: Return an array of zeros with shape and type of input. <= put another ndarray and copy as 111
            full_like:  Return a new array with shape of input filled with value.
            ones:       Return a new array setting values to one.
        '''

        if is_like:
            if is_one:
                return np.ones_like(shape, dtype=dtype)
            else:
                return np.zeros_like(shape, dtype=dtype)
        else:
            if is_one:
                return np.ones(shape, dtype=dtype, order=order)
            else:
                return np.zeros(shape, dtype=dtype, order=order)

    @staticmethod
    def range(*args):
        ''' arange([start,] stop[, step,], dtype=None) '''
        return np.arange(*args)

    @staticmethod
    def random(*args):
        return np.random.randn(*args)



if __name__ == '__main__':
    # n = Numpy((4,3), is_one=True)
    n = Numpy((4,2))

    print(n.reshape((2,4)))
    print(n)
    # n.sort()
    # print(n)
    # print(n.get_dtype())

    # print(Numpy.ones((10, 4), is_one=False))
    # print(Numpy.ones((10,10)))
    # print(Numpy.ones(Numpy.ones((10,10)), is_like=True))


