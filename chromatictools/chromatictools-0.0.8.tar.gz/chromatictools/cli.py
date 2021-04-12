"""Utilities for Command-Line Interface applications"""
import sys


def main(name: str, *args, **kwargs):
  """Decorator for "main" functions of modules

  Args:
    name (str): Module name. Builtin variable :data:`__name__` should be
      passed as argument
    args: Positional arguments for execution as main function
    kwargs: Keyword arguments for execution as main function"""
  def main_(func):
    if name == "__main__":
      sys.exit(func(*args, **kwargs))
    return func
  return main_
