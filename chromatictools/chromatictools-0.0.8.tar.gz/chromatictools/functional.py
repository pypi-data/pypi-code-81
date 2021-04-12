"""Utilities for handling and wrapping functions"""
import functools
from typing import Type, Union, Tuple


def recast_exception(
  type_a: Union[Type[Exception], Tuple[Type[Exception], ...]],
  type_b: Type[Exception]
):
  """Function decorator for wrapping a function: when that function would have
  raised an Exception in :data:`type_a`, now it will return a :data:`type_b`
  exception

  Args:
    type_a (type(s) of exception): A subclass of :class:`Exception` or a tuple
      of subclasses. These exceptions will be recast
    type_b (type of exception): New type for recast exceptions

  Returns:
    Function decorator"""
  def wrapper_(func):
    @functools.wraps(func)
    def func_(*args, **kwargs):
      try:
        r = func(*args, **kwargs)
      except type_a as e:
        raise type_b from e
      return r
    return func_
  return wrapper_
