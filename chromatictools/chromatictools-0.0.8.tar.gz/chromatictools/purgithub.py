"""Purge GitHub page image caches"""
from chromatictools import cli
import argparse
import requests
import subprocess
import sys
import re


@cli.main(__name__, *sys.argv[1:])
def main(*argv):
  """CLI launcher function

  Args:
    argv: Command-line arguments

  Returns:
    int: Exit code"""
  parser = argparse.ArgumentParser(description=globals()["__doc__"])
  parser.add_argument("url", help="GitHub URL")
  parser.add_argument(
    "-p", "--pattern",
    metavar="pattern",
    dest="pattern",
    default="<img src=\"https://camo\\.githubusercontent\\.com.*\"",
    help="Pattern for image search"
  )
  parser.add_argument(
    "-q", "--quiet",
    dest="verbose",
    action="store_false",
  )
  parser.add_argument(
    "-l", "--left",
    metavar="delimiter",
    dest="left",
    default="\"",
    help="Left delimiter to clean pattern"
  )
  parser.add_argument(
    "-r", "--right",
    metavar="delimiter",
    dest="right",
    default="\"",
    help="Right delimiter to clean pattern"
  )
  args = parser.parse_args(argv)

  r = requests.get(args.url)
  urls = map(
    lambda s: s.split(args.left, 1)[1].split(args.right, 1)[0],
    re.findall(args.pattern, r.text)
  )
  cmd = ("curl", "-X", "PURGE")
  for url in urls:
    if args.verbose:
      print(*cmd, url)
    with subprocess.Popen(
      [*cmd, url],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
    ) as p:
      s = p.stdout.read().decode()
    if args.verbose:
      print(s, "\n")
