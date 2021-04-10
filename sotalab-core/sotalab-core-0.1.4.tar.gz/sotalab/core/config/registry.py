from ..utils import Singleton


class ClassRegistry(metaclass=Singleton):
    def __init__(self):
        self._classes = {}

    def register(self, cls, name=None):
        if name is None:
            name = cls.__name__

        if cls not in self._classes:
            self._classes[cls] = {}

        for c in cls.mro():
            if c in self._classes:
                assert name not in self._classes[c], f"Duplicate class name. {c} {name}"
                self._classes[c][name] = cls

    def get(self, cls, name=None):
        if name is None:
            name = cls.__name__

        if name not in self._classes[cls]:
            return None
        else:
            return self._classes[cls][name]

    def __contains__(self, cls):
        return cls in self._classes


def register(cls=None, name=None):
    def wrapper(x):
        ClassRegistry().register(x, name=name)
        return x

    if cls is None:
        return wrapper
    else:
        return wrapper(cls)
