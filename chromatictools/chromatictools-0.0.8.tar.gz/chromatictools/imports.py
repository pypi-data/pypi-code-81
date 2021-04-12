"""Utilities for imports"""
import importlib
import types
from typing import Union


def import_if_installed(
  name: str
) -> Union[types.ModuleType, ModuleNotFoundError]:
  """Import a module if it is installed. Otherwise return a
  :class:`ModuleNotFoundError`

  Args:
    name (str): Module name

  Returns:
    module or ModuleNotFoundError: The module, if it is found. Otherwise a
    :class:`ModuleNotFoundError` instance"""
  try:
    module = importlib.import_module(name)
  except ModuleNotFoundError as e:
    return e
  else:
    return module
