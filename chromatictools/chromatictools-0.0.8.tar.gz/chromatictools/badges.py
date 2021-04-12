"""Generate badge URLs from reports

Example:

.. code:: bash

  python -m coverage run --source <module> -m unittest
  python -m coverage json
  python -m chromatictools.badges coverage"""
from chromatictools import colors, cli
import argparse
import json
from typing import Union
import sys


class HuePercentBadge:
  """Badge URL generator class based on mapping percentage to hue

  Args:
    filename (str): File to read for informtion
    label (str): Badge label
    hue_0 (float): Hue at 0 percent. Default is 0 (red)
    hue_100 (float): Hue at 100 percent. Default is 130 (green)
    hue_gamma (float): Gamma exponent for hue scale correction
    saturation (float): Color saturation
    value (float): Color value
    fmt (str): URL format string with placeholders for :data:`label`,
      :data:`message` and :data:`color`"""
  def __init__(
    self,
    filename: str,
    label: str,
    hue_0: float = 0,
    hue_100: float = 130,
    hue_gamma: float = 1,
    saturation: float = 1,
    value: float = 0.85,
    fmt: str = "https://img.shields.io/badge/{label}-{message}-{color}",
  ):
    self.filename = filename
    self.label = label
    self.hue_0 = hue_0
    self.hue_100 = hue_100
    self.hue_gamma = hue_gamma
    self.saturation = saturation
    self.value = value
    self.fmt = fmt

  @property
  def percent(self) -> Union[str, float]:
    """Percentage score"""
    return "N/A"

  @property
  def message(self) -> str:
    """Badge message"""
    p = self.percent
    if not isinstance(p, str):
      p = "{:.0f}%25".format(p)
    return p

  @property
  def hue(self) -> float:
    """Color hue for the badge"""
    p = self.percent
    if isinstance(p, str):
      return self.hue_0
    p = (p / 100) ** self.hue_gamma
    return p * self.hue_100 + (1 - p) * self.hue_0

  @property
  def color(self) -> str:
    """Hexadecimal color string for the badge"""
    return colors.rgb2hex(
      *colors.hsv2rgb(
        self.hue,
        self.saturation,
        self.value
      )
    )

  @property
  def url(self) -> str:
    """Badge URL string"""
    return self.fmt.format(
      label=self.label,
      message=self.message,
      color=self.color,
    )

  def __str__(self) -> str:
    """Get badge URL"""
    return self.url


class CoverageBadge(HuePercentBadge):
  """Coverage badge utility class

  Args:
    filename (str): Coverage report JSON file
    label (str): Badge label. Default is :data:`"coverage"`
    hue_gamma (float): Gamma exponent for hue scale correction.
      Default is :data:`6`
    kwargs: Keyword arguments for :class:`HuePercentBadge`"""
  def __init__(
    self,
    filename: str,
    label: str = "coverage",
    hue_gamma: float = 6,
    **kwargs,
  ):
    super().__init__(
      filename=filename,
      label=label,
      hue_gamma=hue_gamma,
      **kwargs
    )

  @property
  def report(self) -> dict:
    """Coverage report dictionary"""
    try:
      with open(self.filename, "r") as f:
        d = json.load(f)
    except FileNotFoundError:
      d = {}
    return d

  @property
  def percent(self) -> Union[str, float]:
    """Coverage percentage if found in file, else :data:`"N/A"`"""
    p = self.report.get("totals", {}).get("percent_covered", None)
    if p is None:
      p = super().percent
    return p


class PylintBadge(HuePercentBadge):
  """Pylint badge utility class

  Args:
    filename (str): Text file output of pylint
    label (str): Badge label. Default is :data:`"pylint"`
    kwargs: Keyword arguments for :class:`HuePercentBadge`"""
  def __init__(
    self,
    filename: str,
    label: str = "pylint",
    **kwargs,
  ):
    super().__init__(
      filename=filename,
      label=label,
      **kwargs
    )
    self.filename = filename

  @property
  def report(self) -> str:
    """Pylint report text file"""
    try:
      with open(self.filename, "r") as f:
        s = f.read()
    except FileNotFoundError:
      s = ""
    return s

  @property
  def percent(self) -> Union[str, float]:
    """Pylint rating (out of 100) if found in file, else :data:`"N/A"`"""
    s = self.report
    prefix = "Your code has been rated at "
    if prefix not in s:
      return super().percent
    return float(s.split(prefix, 1)[-1].split("/", 1)[0]) * 10

  @property
  def message(self) -> str:
    """Badge Message"""
    p = self.percent
    if not isinstance(p, str):
      p = "{:.2f}%2F10".format(p / 10)
    return p


@cli.main(__name__, *sys.argv[1:])
def main(*argv):
  """CLI launcher function

  Args:
    argv: Command-line arguments

  Returns:
    int: Exit code"""
  cmds = {
    "coverage": lambda a: CoverageBadge(a.coverage),
    "pylint": lambda a: PylintBadge(a.pylint),
  }
  parser = argparse.ArgumentParser(description=globals()["__doc__"])
  parser.add_argument(
    "badge",
    help="Which badge to use. Should be in {}".format(list(cmds.keys()))
  )
  parser.add_argument(
    "-c",
    metavar="filename",
    dest="coverage",
    default="coverage.json",
    required=False,
    help="JSON coverage report filepath",
  )
  parser.add_argument(
    "-l",
    metavar="filename",
    dest="pylint",
    default="pylint.txt",
    required=False,
    help="Pylint report filepath",
  )
  args = parser.parse_args(argv)
  print(cmds[args.badge](args))
  return 0
