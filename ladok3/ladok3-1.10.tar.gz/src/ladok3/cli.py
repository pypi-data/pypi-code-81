#!/bin/env python3
"""A command-line interface for LADOK 3"""

import appdirs
import argcomplete, argparse
import json
import os
import pickle
import re
import sys
import traceback

import ladok3.data
import ladok3.report

dirs = appdirs.AppDirs("ladok", "dbosk@kth.se")

def err(rc, msg):
  print(f"{sys.argv[0]}: error: {msg}", file=sys.stderr)
  traceback.print_exc(file=sys.stderr)
  sys.exit(rc)

def warn(msg):
  print(f"{sys.argv[0]}: {msg}", file=sys.stderr)
def store_ladok_session(ls):
  if not os.path.isdir(dirs.user_cache_dir):
    os.mkdir(dirs.user_cache_dir)

  file_path = dirs.user_cache_dir + "/LadokSession"

  with open(file_path, "wb") as file:
    pickle.dump(ls, file)
  
def restore_ladok_session():
  file_path = dirs.user_cache_dir + "/LadokSession"

  if os.path.isfile(file_path):
    with open(file_path, "rb") as file:
      return pickle.load(file)

  return None
def load_credentials(filename):
  """Load credentials from environment or file named filename"""
  try:
    user = os.environ["LADOK_USER"]
    passwd = os.environ["LADOK_PASS"]
    return user, passwd
  except:
    pass

  try:
    with open(filename) as conf_file:
      config = json.load(conf_file)
    return config["username"], config["password"]
  except:
    raise Exception("Cannot find credentials.")
def clear_cache(ls, args):
  os.remove(dirs.user_cache_dir + "/LadokSession")
  sys.exit(0)
def main():
  """Run the command-line interface for the ladok command"""
  argp = argparse.ArgumentParser(
    description="Command-line interface for LADOK3",
    epilog="Web: https://github.com/dbosk/ladok3"
  )
  argp.add_argument("-f", "--config-file",
    default=f"{dirs.user_config_dir}/config.json",
    help="Path to configuration file "
      f"(default: {dirs.user_config_dir}/config.json) "
      "or set LADOK_USER and LADOK_PASS environment variables.")
  subp = argp.add_subparsers(
    title="commands",
    dest="command",
    required=True
  )
  cache_parser = subp.add_parser("cache",
    help="Manage cache",
    description="Manages the cache of LADOK data"
  )
  cache_subp = cache_parser.add_subparsers(
    title="subcommands",
    dest="subcommand",
    required=True
  )
  cache_clear = cache_subp.add_parser("clear",
    help="Clear the cache",
    description="Clears everything from the cache"
  )
  cache_clear.set_defaults(func=clear_cache)
  ladok3.data.add_command_options(subp)
  ladok3.report.add_command_options(subp)
  argcomplete.autocomplete(argp)
  args = argp.parse_args()
  LADOK_USER, LADOK_PASS = load_credentials(args.config_file)
  ls = restore_ladok_session()
  if not ls:
    ls = ladok3.LadokSessionKTH(LADOK_USER, LADOK_PASS)
  if "func" in args:
    args.func(ls, args)
  store_ladok_session(ls)

if __name__ == "__main__":
  try:
    main()
    sys.exit(0)
  except Exception as e:
    err(-1, e)
