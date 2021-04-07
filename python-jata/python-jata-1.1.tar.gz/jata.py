# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from typing import Union, Callable, Dict, ClassVar

__all__ = ('Jata', 'JataAttributeError', 'MutableDefault', 'asdict')
__version__ = '1.1'

ALLOWED_TYPES = (str, int, float, bool, list, dict, type(None))

JSON_TYPE = Union[ALLOWED_TYPES + ('Jata',)]
DEFAULT_TYPE = Callable[[], JSON_TYPE]

PYTHON_KEYWORD_PREFIX = 'pykw_'


def _remove_keyword_prefix(key: str):
    if key.startswith(PYTHON_KEYWORD_PREFIX):
        return key[len(PYTHON_KEYWORD_PREFIX):]
    return key


def _remove_all_keyword_prefix(d: dict):
    return {_remove_keyword_prefix(key): val for key, val in d.items()}


class MutableDefault:
    __slots__ = ('default',)

    def __init__(self, default: DEFAULT_TYPE):
        self.default = default


class JataMeta(type):
    def __new__(mcs, name, bases, attrs):
        """
        The objects anyway cannot have any further properties
        So disabling __dict__ using __slots__
        """
        if '__slots__' not in attrs:
            attrs['__slots__'] = tuple()
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, *args, **kwargs):
        """
        Populates class defaults
        """
        super(JataMeta, cls).__init__(*args, **kwargs)
        cls_defaults = {}
        cls_mutable_defaults = {}
        for b_class in cls.mro():
            for key, value in b_class.__dict__.items():
                key = _remove_keyword_prefix(key)
                if key.startswith("__") or key.startswith('_Jata'):
                    continue
                if (key in cls_defaults) or (key in cls_mutable_defaults):
                    continue
                if isinstance(value, MutableDefault):
                    cls_mutable_defaults[key] = value.default
                elif isinstance(value, ALLOWED_TYPES + (Jata,)):
                    cls_defaults[key] = value
                else:
                    raise TypeError(f"Can only have json types for value. Type {type(value)} for {key} is invalid")
        cls._Jata_cls_defaults = cls_defaults
        cls._Jata_cls_mutable_defaults = cls_mutable_defaults


class Jata(metaclass=JataMeta):
    """
    Typed Json Data
    """
    _Jata_DATA_FIELD_NAME = "_Jata_data"
    __slots__ = (_Jata_DATA_FIELD_NAME,)

    # Below fields are set by JataMeta
    _Jata_cls_defaults: ClassVar[Dict[str, JSON_TYPE]]
    _Jata_cls_mutable_defaults: ClassVar[Dict[str, DEFAULT_TYPE]]

    def __init__(self, content=None, /, **kwargs):
        """
        Initializes the fields from class defaults, content and then kwargs. Latter overriding former
        """
        self._Jata_data = {}
        self._Jata_data.update(self._Jata_cls_defaults)

        for key, default_func in self._Jata_cls_mutable_defaults.items():
            self._Jata_data[key] = default_func()

        if content:
            if isinstance(content, dict):
                self._Jata_data.update(_remove_all_keyword_prefix(content))
            elif isinstance(content, Jata):
                self._Jata_data.update(content._Jata_data)
            else:
                content = json.loads(content)  # Assumes keyword prefix is already removed
                self._Jata_data.update(content)

        self._Jata_data.update(_remove_all_keyword_prefix(kwargs))

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __getattribute__(self, key):
        """
        Gets the attribute from the _Jata_data except for internal ones
        Dicts in the list are converted to Jata
        Cannot use __getattr__ as that is not called for fields that have class defaults
        """
        if key.startswith("__") or key.startswith('_Jata'):
            return super(Jata, self).__getattribute__(key)

        key = _remove_keyword_prefix(key)

        try:
            attr = self._Jata_data[key]
        except KeyError:
            raise JataAttributeError(key)

        def convert_jata_list(jata_list: list):
            def convert(item):
                if isinstance(item, dict):
                    return Jata(item)
                elif isinstance(item, list):
                    convert_jata_list(item)
                return item

            jata_list[:] = [convert(item) for item in jata_list]

        if isinstance(attr, dict):
            return Jata(attr)
        elif isinstance(attr, list):
            convert_jata_list(attr)

        return attr

    def __setattr__(self, key, value):
        if key == Jata._Jata_DATA_FIELD_NAME:
            super(Jata, self).__setattr__(key, value)
            return

        key = _remove_keyword_prefix(key)
        self._Jata_data[key] = value

    # noinspection PyProtectedMember
    def __str__(self):
        return json.dumps(self._Jata_data, default=lambda obj: obj._Jata_data)

    def __repr__(self):
        data_repr = repr(self._Jata_data)
        max_len = 80
        if len(data_repr) > max_len:
            data_repr = f"{data_repr[:max_len - 3]}..."

        return f"{self.__class__.__name__}({data_repr})"


def asdict(jata: Union[Jata, dict]):
    """
    Converts to a regular python dict
    """

    def convert(obj):
        if isinstance(obj, Jata) or isinstance(obj, dict):
            return asdict(obj)
        elif isinstance(obj, list):
            return [convert(item) for item in obj]
        else:
            return obj

    if isinstance(jata, Jata):
        # noinspection PyProtectedMember
        jata = jata._Jata_data

    return {key: convert(value) for key, value in jata.items()}


class JataAttributeError(AttributeError):
    pass
