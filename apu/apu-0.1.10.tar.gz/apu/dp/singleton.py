"""
different realization to implement a base singletion structure

Author: anton feldmann <anton.feldmann@gmail.com>
"""

import functools

def singleton(cls):
    """ singleton declerator

        Examples:
        ..  example_code::
            >>> from apu.dp.singleton import singleton

            >>> @singleton
            >>> class Duck():
            >>>     pass

            >>> Duck() is Duck()
            True
    """
    pre_instance={}
    functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls in pre_instance and \
            pre_instance.get(cls, None).get('args') == (args,kwargs):
            return pre_instance[cls].get('instance')

        pre_instance[cls] = {"args": (args,kwargs),
                            "instance": cls(*args, **kwargs)}
        return pre_instance[cls].get('instance')

    return wrapper

class Singleton(type):
    """ singleton metaclass

    Examples:
    ..  example_code::
        >>> from apu.dp.singleton import Singleton

        >>> class Duck(metaclass=Singleton):
        >>>     pass

        >>> Duck() is Duck()
        True
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls). \
                                __call__(*args, **kwargs)
        return cls._instances[cls]
