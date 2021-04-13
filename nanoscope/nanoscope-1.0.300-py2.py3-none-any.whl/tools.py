# -*- coding: utf-8 -*-
"""
Common tools for the package.

"""

import sys
from shutil import copyfile


def check_unit_type(unit_type, accepted_types):
    """Check if the unit_type is part of the accepted_types.

    Raise a ValueError if the unit_type is not acceptable.
    """
    if unit_type not in accepted_types:
        raise ValueError("Wrong unit_type parameter.")


def copy_py_file(source, dest=None):
    """Save a copy of the python file.

    The file is copied in the given filename.
    If no file is given, a file dialog will request one.
    """
    if source.endswith(".pyc"):
        source = source[:-1]

    if not dest:
        if sys.version_info.major == 2:  # Python 2
            from tkinter import Tk
            from tkinter.filedialog import asksaveasfilename
        else:  # Python 3
            from tkinter import Tk
            from tkinter.filedialog import asksaveasfilename
        Tk().withdraw()  # To avoid root GUI
        dest = asksaveasfilename(
            defaultextension=".py",
            filetypes=(("Python file", "*.py"),))

    if dest:
        copyfile(source, dest)


class constant_property(property):
    """Decorator for constant properties.

    Once the function has been called once, it caches the result.
    """

    def __init__(self, func):
        super(constant_property, self).__init__(fget=self.getx)
        self.__doc__ = func.__doc__
        self._func = func
        self._name = "_constant_property__" + func.__name__

    def getx(self, owner):
        if self._name not in owner.__dict__:
            owner.__dict__[self._name] = self._func(owner)
        return owner.__dict__[self._name]


class script_tools:
    @staticmethod
    def blank_unitless(number, unit):
        """ Replace values that have no units with blanks. Used to hide
        irrelevant parameters from example table generated below.
        """
        if unit == "":
            return '', ''
        else:
            return str(number), unit

    @staticmethod
    def decode_2d_char_array(array):
        """Decodes arrays that are of type LP_c_char_Array_X_Array_Y
        where X and Y are integers.

        Returns list of strings.
        """
        array_decoded = []
        for item in array:
            try:
                array_decoded.append(item.contents.value.decode("latin-1"))
            except:
                raise RuntimeError("Decoding failed")
        return array_decoded
