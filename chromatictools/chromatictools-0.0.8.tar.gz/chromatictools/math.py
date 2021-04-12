"""Math utilities"""
import numpy as np


def mantissa(x: np.array) -> np.ndarray:
  """Remove order of magnitude from array

  Args:
  x (array): Inputs

  Returns:
    array: Rescaled array"""
  y = np.log10(np.abs(x))
  return np.sign(x) * np.power(10., (y - np.floor(np.max(y))))


def rmse(x: np.ndarray, y: np.ndarray) -> float:
  """Compute the root-mean-squared error

  Arguments:
    x (array): First array
    y (array): Second array

  Returns:
    (float): The RMSE between x and y"""
  return np.sqrt(np.mean(np.abs(x - y)**2))
