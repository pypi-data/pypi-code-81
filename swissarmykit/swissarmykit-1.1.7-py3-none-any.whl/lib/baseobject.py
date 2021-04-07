import sys
import types
import traceback
import inspect

from swissarmykit.utils.fileutils import FileUtils


class BaseObject:

    _object:any
    _plt:any

    def __init__(self, _object=None):
        self._object = _object

    @staticmethod
    def get_variable_name(var):
        """
        Ref: https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string

        Gets the name of var. Does it from the out most frame inner-wards.
        """
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]

    @classmethod
    def get_cls_name(cls):
        return cls.__name__

    def __getattr__(self, attr):
        ''' https://medium.com/@satishgoda/python-attribute-access-using-getattr-and-getattribute-6401f7425ce6 '''
        if attr in dir(self):
            return self.get()
        else:
            return self._object.__getattribute__(attr)

    def __getitem__(self, item):
        return self._object.__getitem__(item)

    def __bool__(self):
        return self.is_empty()

    def is_empty(self):
        return True

    def __str__(self):
        return str(self._object)

    def __repr__(self):
        return str(self._object)

    def __eq__(self, other):
        return self._object.equals(other._object)

    def copy(self):
        return self # override at child

    def dump(self, path=None):
        pass

if __name__ == '__main__':

    class TestBase:

        def __init__(self):
            self.data = 'testbase'

        def pri(self, *args, **kwargs):
            print('pri function TestBase', *args, kwargs)

    class Test(BaseObject):

        def __init__(self):
            self.data = TestBase()
            self._object = self.data

if __name__ == '__main__':
    t = Test()
    print(t.pri(1,test='43'))


