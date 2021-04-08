#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple classes to add obj.key syntax to dictionary."""
import logging

_LOG = logging.getLogger('peyutil')
_DANGEROUS_KEYS = frozenset(['items', 'values', 'keys', 'get', 'setdefault'])


# noinspection PyUnresolvedReferences
class DictWrapper(object):
    """Base class that wraps the key->value mapping of a dict by delegation.

    Stores an internal copy of the dict, `d` that is used to initialize the
    instance.
    """

    # pylint: disable=E1101
    def __init__(self, d):
        """Wraps dict `d`. Keys should not be dict class attributes."""
        assert '_raw_dict' not in d  # this would mess up the hacky __getattr__
        for k in _DANGEROUS_KEYS:
            if k in d:
                _LOG.warning('Key "{k}" in DictWrapper clashes with a dict member.', k=k)
        object.__setattr__(self, '_raw_dict', d)

    def __getitem__(self, key):
        """Return the value of d[k] when the DictWrapper was created."""
        return self._raw_dict[key]

    def items(self):
        """Return the d.items() when the DictWrapper was created."""
        return self._raw_dict.items()

    def values(self):
        """Return the d.values() when the DictWrapper was created."""
        return self._raw_dict.values()

    def keys(self):
        """Return the d.keys() when the DictWrapper was created."""
        return self._raw_dict.keys()

    def get(self, key, default=None):
        """Return the d.get(key) when the DictWrapper was created."""
        return self._raw_dict.get(key, default=default)

    def setdefault(self, key, default):
        """Returns and stores the d.setdefault(key, default)."""
        return self._raw_dict.setdefault(key, default)

    def __setitem__(self, key, value):
        """Sets the key mapping key->value for the wrapper."""
        self._raw_dict[key] = value

    def __contains__(self, key):
        """Returns True if key is in the dict."""
        return key in self._raw_dict

    def __str__(self):
        """Returns a __repr__ of the wrapper."""
        return '{c}({d})'.format(c=self.__class__.__name__, d=str(self._raw_dict))


class DictAttrWrapper(DictWrapper):
    """Class the provides the dot (setattr) syntax for key access to a dict.

    This is just syntactic sugar for dictionaries.
    It is only used in some API wrappers of peyotl.
    Note that the wrappers (even the frozen forms) hold references to the dict
    used to initialize them. So, changing that dict will have effects on the
    wrappers, too.
    """
    def __init__(self, d):
        """Builds internal copy of `d` via shallow copy."""
        DictWrapper.__init__(self, d)

    def __setattr__(self, key, value):
        """Same as __setitem__(key, value)."""
        self._raw_dict[key] = value

    def __getattr__(self, key):
        """Same as __getitem__(key, value), but raises AttributeErrors instead of KeyErrors."""
        try:
            return self._raw_dict[key]
        except KeyError:
            raise AttributeError('DictWrapper has no key "{}"'.format(key))


_write_msg_template = 'A "frozen" class derived from {} does not support rebinding keys'


class FrozenDictWrapper(DictWrapper):
    """Read-only dict wrapper."""

    _write_msg = _write_msg_template.format('FrozenDictWrapper')

    def __init__(self, d):
        """Builds internal copy of `d` via shallow copy."""
        DictWrapper.__init__(self, d)

    def __setattr__(self, key, value):
        """Raises TypeError because this class is read-only."""
        raise TypeError(FrozenDictWrapper._write_msg)

    def __setitem__(self, key, value):
        """Raises TypeError because this class is read-only."""
        raise TypeError(FrozenDictWrapper._write_msg)


class FrozenDictAttrWrapper(DictAttrWrapper):
    """Read-only dict wrapper, but adds dot read-syntax like DictAttrWrapper."""

    _write_msg = _write_msg_template.format('FrozenDictAttrWrapper')

    def __init__(self, d):
        """Builds internal copy of `d` via shallow copy."""
        DictAttrWrapper.__init__(self, d)

    def __setattr__(self, key, value):
        """Raises TypeError because this class is read-only."""
        raise TypeError(FrozenDictAttrWrapper._write_msg)

    def __setitem__(self, key, value):
        """Raises TypeError because this class is read-only."""
        raise TypeError(FrozenDictAttrWrapper._write_msg)
