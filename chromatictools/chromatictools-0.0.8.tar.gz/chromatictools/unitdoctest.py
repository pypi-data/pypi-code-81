"""Utilities for extracting unittests from doctests"""
import unittest
import doctest
import contextlib
import io
from typing import Tuple


class DocTestMeta(type):
  """Metaclass for generating :class:`unittest.TestCase` classes.
  Modules to test should be listed in an attribute called :data:`_modules`"""
  def __new__(mcs: type, name: str, bases: Tuple[type, ...], dct: dict):
    if len(bases) == 0:
      bases = (unittest.TestCase,)
    for m in dct.get("_modules", ()):
      def method(self, mod=m):
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
          res = doctest.testmod(mod, verbose=True)
          msg = buf.getvalue()
        self.assertFalse(bool(res.failed), msg=msg)
      method.__name__ = "test_" + m.__name__.replace(".", "_")
      method.__doc__ = m.__doc__.split("\n", 1)[0]
      dct[method.__name__] = method
    cls = super().__new__(mcs, name, bases, dct)
    return cls
