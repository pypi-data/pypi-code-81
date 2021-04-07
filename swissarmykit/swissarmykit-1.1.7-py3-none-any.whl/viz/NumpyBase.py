import numpy as np

class NumpyBase:
    data: np.ndarray

    def __lt__(self, other):
        if isinstance(other, Numpy):
            return self.data < other.data

        return self.data < other

    def __gt__(self, other):
        if isinstance(other, Numpy):
            return self.data > other.data

        return self.data > other

    def __le__(self, other):
        if isinstance(other, Numpy):
            return self.data <= other.data

        return self.data <= other

    def __ge__(self, other):
        if isinstance(other, Numpy):
            return self.data >= other.data
        
        return self.data >= other

    def __eq__(self, other):
        if isinstance(other, Numpy):
            return self.data == other.data
        
        return self.data == other

    def __ne__(self, other):
        if isinstance(other, Numpy):
            return self.data != other.data

        return self.data != other

    def __mod__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data % other.data)

        return Numpy(self.data % other)

    def __pow__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data ** other.data)

        return Numpy(self.data ** other)

    def __floordiv__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data // other.data)

        return Numpy(self.data // other)

    def __truediv__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data / other.data)

        return Numpy(self.data / other)

    def __sub__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data - other.data)

        return Numpy(self.data - other)

    def __add__(self, other):
        if isinstance(other, Numpy):
            return Numpy(self.data + other.data)

        return Numpy(self.data + other)

    def __mul__(self, other):
        ''' https://www.geeksforgeeks.org/operator-overloading-in-python/ '''
        if isinstance(other, Numpy):
            return Numpy(self.data * other.data)

        return Numpy(self.data * other)

    def __str__(self):
        return 'Numpy Wrapper: \n'  + str(self.data)
