"""Mixin classes for unittests"""
from chromatictools import math
import functools
import contextlib
import numpy as np
import io


class AssertPrintsMixin:
  """Mixin class for print assertion"""
  @contextlib.contextmanager
  def assert_prints(self, target: str):
    """Assert that contextual code prints the target string.
    Use as context manager

    Args:
      target (str): Print expectation"""
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
      yield
      printed = buf.getvalue()
    self.assertEqual(printed, target)


class AssertDoesntRaiseMixin:
  """Mixin class for "doesn't-raise" assertion"""
  @contextlib.contextmanager
  def assert_doesnt_raise(self):
    """Assert that contextual code doesn't raise any exception
    Use as context manager"""
    try:
      yield
    except Exception as e:
      raise AssertionError from e


class SignificantPlacesAssertMixin:
  """Mixin class for assertions based on singificant places"""
  def assert_almost_equal_significant(
    self,
    first,
    second,
    places=0,
    msg=None,
    delta=None
  ):
    """Fail if the two objects are unequal as determined by their
    difference rounded to the given number of significant decimal places
    (default 0)"""
    return self.assertAlmostEqual(
      *math.mantissa([first, second]),
      places=places,
      msg=msg,
      delta=delta
    )


class RMSEAssertMixin:
  """Mixin class for assertions based on the RMSE"""
  def _assert_rmse(
    self,
    x: np.ndarray,
    y: np.ndarray,
    almost: bool,
    *args,
    rmse: float = 0,
    **kwargs
  ):
    """Assert that the RMSE is equal to a given value

    Arguments:
      x (array): First array
      y (array): Second array
      almost (bool): If True, then assert that the RMSE is almost zero
      rmse (float): RMSE value. Defaults to 0
      *args: Positional arguments for :func:`unittest.TestCase.assertEqual`
        or :func:`unittest.TestCase.assertAlmostEqual`
      **kwargs: Keyword arguments for :func:`unittest.TestCase.assertEqual`
        or :func:`unittest.TestCase.assertAlmostEqual`"""
    return (self.assertAlmostEqual if almost else self.assertEqual)(
      math.rmse(x, y), rmse,
      *args, **kwargs,
    )

  assert_equal_rmse = functools.partialmethod(_assert_rmse, almost=False)
  assert_almost_equal_rmse = functools.partialmethod(_assert_rmse, almost=True)
