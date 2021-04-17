import collections
if "defaults" not in collections.namedtuple.__kwdefaults__:
    def namedtuple(typename, field_names, defaults=()):
        T = collections.namedtuple(typename, field_names)
        T.__new__.__defaults__ = (None,) * len(T._fields)
        if isinstance(defaults, collections.Mapping):
            prototype = T(**defaults)
        else:
            prototype = T(*defaults)
        T.__new__.__defaults__ = tuple(prototype)
        return T
else:
    namedtuple = collections.namedtuple

