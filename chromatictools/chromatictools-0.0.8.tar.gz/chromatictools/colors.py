"""Utilities for color handling"""
from typing import Tuple


def hsv2rgb(h: float , s: float, v: float) -> Tuple[int, int, int]:
  """Convert HSV to RGB

  Args:
    h (float): Hue (degrees)
    s (float): Saturation (between 0 and 1)
    v (float): Value (between 0 and 1)

  Returns
    tuple of int: RGB values (between 0 and 255)"""
  h = h % 360
  c = v * s
  x = c * (1 - abs((h / 60) % 2 - 1))
  m = v - c
  t = (
    (c, x, 0),
    (x, c, 0),
    (0, c, x),
    (0, x, c),
    (x, 0, c),
    (c, 0, x),
  )[int(h) // 60]
  return tuple(
    int((i + m) * 255)
    for i in t
  )


def rgb2hex(r: int, g: int, b: int) -> str:
  """Convert RGB integers to hexadecimal string

  Args:
    r (int): Red (between 0 and 255)
    g (int): Green (between 0 and 255)
    b (int): Blue (between 0 and 255)

  Returns
    str: Hexadecimal string"""
  return "".join(
    hex(v)[2:].rjust(2, "0")
    for v in (r, g, b)
  )
