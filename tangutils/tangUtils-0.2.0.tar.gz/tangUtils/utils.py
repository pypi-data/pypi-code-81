from typing import List, Dict, Union
import re, subprocess

Arg = Union[str, int, float]
ListArg = List[Arg]
DictArg = Dict[str, Union[Arg, List[Arg]]]

# forCmd: 将会为含有空格的参数包裹上引号
def toWin(p: str, forCmd=False) -> str:
  winP = re.sub("/", "\\\\", p.strip())
  if forCmd and re.match(r'\S+\s', winP):
    return '"%s"' % winP
  return winP

def callJs(p: str, args: Union[ListArg, DictArg], nodeExePath="node"):
  cmd = [nodeExePath, p]
  if isinstance(args, list):
    cmd.extend(args)
  else:
    for k in args.keys():
      if isinstance(args[k], list):
        for val in args[k]:
          cmd.append("%s" % k)
          cmd.append("%s" % str(val))
      else:
        cmd.append("%s" % k)
        cmd.append("%s" % str(args[k]))
  subprocess.call(" ".join([toWin(s, True) for s in cmd]))

def callPython(p: str, args: Union[ListArg, DictArg], pythonExePath="python"):
  cmd = [pythonExePath, p]
  if isinstance(args, list):
    cmd.extend(args)
  else:
    for k in args.keys():
      if isinstance(args[k], list):
        for val in args[k]:
          cmd.append("%s" % k)
          cmd.append("%s" % str(val))
      else:
        cmd.append("%s" % k)
        cmd.append("%s" % str(args[k]))
  subprocess.call(" ".join([toWin(s, True) for s in cmd]))
