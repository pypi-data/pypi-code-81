"""Utilities for pickle"""
import functools
import pickle
import os
from typing import Any, Callable, Union


def read_pickled(filepath: str, encoding: str = "latin1") -> Any:
  """Read the pickled data in the file

    Args:
      filepath (str): The file path
      encoding (str): File encoding. Defaults to :data:`"latin1"`

    Returns:
      The unpickled data"""
  with open(filepath, "rb") as f:
    return pickle.load(f, encoding=encoding)


def save_pickled(obj: Any, filepath: str):
  """Save data in a pickled file

    Args:
      obj (Any): The data to pickle
      filepath (str): The path of the file to write.
        Directory is created if it doesn't exist"""
  d = os.path.dirname(filepath)
  if d:
    os.makedirs(d, exist_ok=True)
  with open(filepath, "wb") as f:
    pickle.dump(obj, f)


def _pickled_cache_m(
  filepath: Callable[[Any], str]
) -> Callable[[Callable], Callable]:
  """Store the last result of the function call
  in a pickled file (method version). See
  :func:`pickled_cache` for usage example

  Args:
    filepath (Callable): A method that takes no other
      arguments other than the instance and returns the
      path of the file to read/write

  Returns:
    Callable[[Callable], Callable]: function decorator.
    The decorated function will also have an attribute
    function 'forced', that calls the function forcing
    cache overwriting"""
  def pickled_cache_(foo: Callable) -> Callable:
    @functools.wraps(foo)
    def foo_forced(*args, **kwargs):
      r = foo(*args, **kwargs)
      save_pickled(r, filepath(*args[:1]))
      return r

    @functools.wraps(foo)
    def foo_cached(*args, **kwargs):
      return read_pickled(filepath(*args[:1]))\
        if os.path.isfile(filepath(*args[:1]))\
        else foo_forced(*args, **kwargs)

    foo_cached.forced = foo_forced
    return foo_cached
  return pickled_cache_


def _pickled_cache_s(filepath: str) -> Callable[[Callable], Callable]:
  """Store the last result of the function call
  in a pickled file (string version)

  Args:
    filepath (str): The path of the file to read/write

  Returns:
    Callable[[Callable], Callable]: function decorator.
    The decorated function will also have an attribute
    function 'forced', that calls the function forcing
    cache overwriting"""
  return _pickled_cache_m(lambda *args, **kwargs: filepath)


def _pickled_cache_p(
  filepath: property
) -> Callable[[Callable], Callable]:
  """Store the last result of the function call
  in a pickled file (property version). See
  :func:`pickled_cache` for an usage example

  Args:
    filepath (property): A property that returns the
      path of the file to read/write

  Returns:
    Callable[[Callable], Callable]: function decorator.
    The decorated function will also have an attribute
    function 'forced', that calls the function forcing
    cache overwriting"""
  return _pickled_cache_m(filepath.fget)


_pickled_cache_funcs = (
  (str, _pickled_cache_s),
  (property, _pickled_cache_p),
  (Callable, _pickled_cache_m),
)


def pickled_cache(
  filepath: Union[str, Callable, property]
) -> Callable[[Callable], Callable]:

  """Store the last result of the function call
  in a pickled file (string version)

  Args:
    filepath (str or property or method): The path of the file to read/write as
     a string or as a getter method or property

  Returns:
    Callable[[Callable], Callable]: function decorator.
    The decorated function will also have an attribute
    function 'forced', that calls the function forcing
    cache overwriting

  Example:
    >>> from chromatictools.pickle import pickled_cache
    >>> cache_file: str = ".pickled_example.cache"
    >>> @pickled_cache(cache_file)
    ... def echo(s: str):
    ...   return s
    >>> echo("Alice")
    'Alice'
    >>> echo("Bob")
    'Alice'
    >>> echo.forced("Bob")
    'Bob'
    >>> echo("Alice")
    'Bob'
    >>> import os
    >>> os.remove(cache_file)

  Remove cache for inter-session repeatability (otherwise,
  the second time the example is run, the first `echo("Alice")`
  would return `"Bob"`). In a real scenario, you probably wouldn't
  want to do this, as inter-session memory is the main purpose
  of this decorator
  """
  for c, f in _pickled_cache_funcs:
    if isinstance(filepath, c):
      return f(filepath)
  raise NotImplementedError(
    "No 'pickled_cache' decorator available for filepath of type '{}'".format(
      type(filepath).__name__
    )
  )
