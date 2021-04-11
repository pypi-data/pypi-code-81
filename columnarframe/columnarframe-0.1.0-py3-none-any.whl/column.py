import pyarrow as pa


class Column:

    def __init__(self, parent, key, value):
        self.parent = parent
        self.key = key

        if isinstance(value, Column):
            pass

        if isinstance(value, pa.Array):
            if self.parent.rows != len(value):
                raise RuntimeError('different record count')
            self.value = pa.array(value.to_pylist())
        elif isinstance(value, list):
            if self.parent.rows != len(value):
                raise RuntimeError('different record count')
            self.value = pa.array(value)
        else:
            self.value = pa.array([value] * self.parent.rows)

    def __repr__(self):
        return self.value.__repr__()

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        print('aaa')
        return self.__class__
