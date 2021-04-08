import os
import sys

from anoptions import Parameter, Options
from .template import Template
from .processor import Processor


def file_exists(filename):
  return filename is not None and os.path.exists(filename) and os.path.isfile(filename)  


def load_json(filename, default=None):
  import json
  if filename == '-':
    import sys
    f = sys.stdin
  elif file_exists(filename):
    f = open(filename) 
  else:
    return default
  with f as json_file:
    data = json.load(json_file)
  return data


def usage():
  print("USAGE: python3 -m antp -t|--template <templatefile> [-o|--output <outputfile>] [-d|--data <json_datafile1,json_datafile2,...,json_datafileN]")
  sys.exit(1)


def main(args):
  parameters = [
    Parameter("template", str, "template", default='-'),
    Parameter("output", str, "output", default='-'),
    Parameter("data", str, "data"),
    Parameter("help", Parameter.flag, "help")
  ]

  opt = Options(parameters, args, 'antp')
  d = opt.eval()

  if d["help"] is True:
    usage()

  required = ["template"]
  for x in required:
    if x not in d:
      usage()

  if "data" in d:
    d["data"] = d["data"].split(',')

  check_files = ["template", "output", "data"] 
  for _x in check_files:
    if _x not in d:
      continue  
    y = d[_x] if isinstance(d[_x], list) else [d[_x]]
    for fname in y:
      if not file_exists(fname) and fname != '-':
        print("File {} does not exist -- exiting".format(fname))
        sys.exit(66)

  template_data = { 
    "data": {},
    "env": os.environ
  } 

  if "data" in d:
    _data = {}
    for fname in d["data"]:
      _data = { **_data, **load_json(fname, {}) }
    template_data["data"] = _data

  t = Template(filename=d["template"])
  Processor.process(t, d["output"], data=template_data)


if __name__ == "__main__":
  main(sys.argv[1:])