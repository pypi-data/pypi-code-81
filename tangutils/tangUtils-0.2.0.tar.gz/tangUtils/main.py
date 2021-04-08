#!/usr/bin/env python
# coding: utf-8

from typing import Any, List, Tuple, Dict, Callable, TypeVar
import os, random, subprocess, codecs, json, socket, webbrowser, shutil, re, sys, math
from http.server import HTTPServer, SimpleHTTPRequestHandler
""" pillow
  如果没有pillow, 详见 https://pillow.readthedocs.io/en/stable/installation.html
  pip install pillow
"""
from PIL import Image

""" multiprocessing
  from multiprocessing import Pool

  pool = Pool(processes=4)

  def doSomething(i):
    print(i)

  for i in range(100):
    pool.apply_async(doSomething, args=(i,))

  pool.close()
  pool.join()
"""

""" arguments
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("-b", "--boolean", help="some help", action="store_true")
  parser.add_argument("-s", "--string", help="some help")
  parser.add_argument("-i", "--int", type=int, help="some help")

  args = parser.parse_args()

  print(args.string)
"""

""" 路径区别
  os.getcwd(): 程序执行目录(绝对路径)
  sys.path[0]: 主模块所在目录(绝对路径)
  sys.argv[0]: 主模块文件路径(绝对路径 | 相对路径)
  __file__: 作为入口时(__name__ == "__main__"), 是当前文件名, 作为模块被引入时, 是当前文件绝对路径
"""

def resolve(*args: str) -> str:
  """
  返回绝对路径, 并将 "\\" 转为 "/"
  """
  return os.path.abspath(os.path.join(*args)).replace("\\", "/")

def createIfNotExists(dirPath: str) -> "Dir":
  if not os.path.isdir(dirPath):
    os.makedirs(dirPath)
  return Dir(dirPath)

def createHttpServer(host: str=socket.gethostbyname(socket.gethostname()), port: int=8080, webRoot: str=os.getcwd(), page: str="", open: bool=True):
  os.chdir(webRoot)
  httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
  url = "%s://%s:%s/%s" % ("http", host, port, re.sub(r'(\.\/|\/|\.\\|\\)', "", page))
  print("\nserver running on  %s\n" % url)
  if open:
    webbrowser.open(url)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass

def question(q: str, defaultValue: str = None) -> str:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      inputStr = input(qStr).strip()
      if inputStr != "":
        return inputStr
  else:
    assert isinstance(defaultValue, str), "is not string: %s" % defaultValue
    inputStr = input(qStr).strip()
    if inputStr == "":
      return defaultValue
    else:
      return inputStr

def questionInt(q: str, defaultValue: int = None) -> int:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      try:
        return int(input(qStr).strip())
      except Exception:
        pass
  else:
    assert isinstance(defaultValue, int), "wrong type: %s is not int" % defaultValue
    while True:
      inputStr = input(qStr).strip()
      if inputStr == "":
        return defaultValue
      else:
        try:
          return int(inputStr)
        except Exception:
          pass

def questionFloat(q: str, defaultValue: float = None) -> float:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      try:
        return float(input(qStr).strip())
      except Exception:
        pass
  else:
    assert isinstance(defaultValue, float), "wrong type: %s is not float" % defaultValue
    while True:
      inputStr = input(qStr).strip()
      if inputStr == "":
        return defaultValue
      else:
        try:
          return float(inputStr)
        except Exception:
          pass

def questionBool(q: str, defaultValue: bool = False) -> bool:
  qStr = "%s【Y/n】 默认值【%s】" % (q, "Y" if defaultValue else "n")
  assert isinstance(defaultValue, bool), "wrong type: %s is not bool" % defaultValue
  while True:
    inputStr = input(qStr).strip().lower()
    if inputStr == "":
      return defaultValue
    if inputStr == "y":
      return True
    if inputStr == "n":
      return False

class Base(object):
  # 规范路径
  path: str
  # 父目录的路径
  dirname: str
  # 文件名(包括后缀)
  basename: str
  # 文件名(不包括后缀)
  name: str
  # 后缀
  suffix: str
  # 假的无后缀文件名(之所以说是假的, 是因为目录没有后缀)
  fakeName: str
  # 假的后缀(之所以说是假的, 是因为目录没有后缀)
  fakeSuffix: str
  def __init__(self, *p: str):
    super(Base, self).__init__()
    self.path: str = resolve(*p)

  @property
  def dirname(self) -> str:
    return os.path.dirname(self.path)

  @property
  def basename(self) -> str:
    return os.path.basename(self.path)

  @property
  def splitname(self) -> Tuple[str, str]:
    return os.path.splitext(self.basename)

  @property
  def name(self) -> str:
    return self.basename

  @property
  def suffix(self) -> str:
    return ""

  @property
  def fakeName(self) -> str:
    return self.splitname[0]

  @property
  def fakeSuffix(self) -> str:
    return self.splitname[1]

  @property
  def parent(self) -> "Base":
    """
    @warning 警告, 根目录的 parent 是其自身, 但 parents 是一个空数组
    """
    return Base(self.dirname)

  @property
  def parents(self) -> List["Base"]:
    """
    @warning 警告, 根目录的 parent 是其自身, 但 parents 是一个空数组
    """
    p = self.parent
    if self.sameAs(p):
      return []
    parents = [p]
    parents.extend(p.parents)
    return parents

  def childOf(self, *p: str) -> "Base":
    return Base(self.path, *p)

  def siblingOf(self, *p: str) -> "Base":
    return Base(self.dirname, *p)

  def sameAs(self, base) -> bool:
    if not base:
      return False
    if self == base:
      return True
    return self.path == base.path

  @property
  def isImg(self) -> bool:
    _isImg = False
    try:
      with Image.open(self.path) as img:
        _isImg = True
    except Exception:
      pass
    return _isImg

  @property
  def isFile(self) -> bool:
    return os.path.isfile(self.path)

  @property
  def isDir(self) -> bool:
    return os.path.isdir(self.path)

  def toAbsPath(self) -> "Base":
    """
    deprecated
    """
    return self

  def createAsDir(self) -> "Dir":
    if not self.isDir:
      os.makedirs(self.path)
    return Dir(self.path)

  def createAsFile(self) -> "File":
    if not self.isFile:
      self.parent.createAsDir()
      with open(self.path, "w") as f:
        pass
    return File(self.path)

  def asFile(self) -> "File":
    return File(self.path)

  def asDir(self) -> "Dir":
    return Dir(self.path)

class File(Base):
  def __init__(self, *p: str):
    super(File, self).__init__(*p)
    assert self.isFile, "is not file: %s" % self.path

  @property
  def name(self) -> str:
    return self.fakeName

  @property
  def suffix(self) -> str:
    return self.fakeSuffix

  @property
  def parent(self) -> "Dir":
    return Dir(self.dirname)

  def read(self, encoding="UTF-8") -> str:
    result = ""
    with codecs.open(self.path, "r", encoding=encoding) as f:
      result = f.read()
    return result

  def __write(self, s: str, mode: str, encoding="UTF-8") -> "File":
    with codecs.open(self.path, mode, encoding=encoding) as f:
      f.write(s)
    return self

  def write(self, s: str, encoding="UTF-8") -> "File":
    return self.__write(s, "w", encoding=encoding)

  def aWrite(self, s: str, encoding="UTF-8") -> "File":
    return self.__write(s, "a", encoding=encoding)

  def toAbsPath(self) -> "File":
    """
    deprecated
    """
    return self

class Dir(Base):
  def __init__(self, *p: str):
    super(Dir, self).__init__(*p)
    assert self.isDir, "is not dir: %s" % self.path

  @property
  def parent(self) -> "Dir":
    return Dir(self.dirname)

  @property
  def fileNames(self) -> List[str]:
    return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

  @property
  def files(self) -> List["File"]:
    return [File(self.path, f) for f in self.fileNames]

  @property
  def dirNames(self) -> List[str]:
    return [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))]

  @property
  def dirs(self) -> List["Dir"]:
    return [Dir(self.path, d) for d in self.dirNames]

  @property
  def allDirs(self) -> List["Dir"]:
    dirs = [d for d in self.dirs]
    curIdx = 0
    while curIdx < len(dirs):
      dirs.extend(dirs[curIdx].dirs)
      curIdx += 1
    return dirs

  @property
  def allFiles(self) -> List["File"]:
    files = [f for f in self.files]
    for d in self.allDirs:
      files.extend(d.files)
    return files

  def includes(self, dirA: "Dir") -> bool:
    # 当不含有dirA中的文件时，有print提示；
    # 当不含有dirA中的目录时，没有提示
    for f in dirA.files:
      if f.basename not in self.fileNames:
        print("【%s】 not in 【%s】" % (f.basename, self.path))
        return False
    for d in dirA.dirs:
      if d.basename not in self.dirNames:
        return False
      if not Dir(self.path, d.basename).includes(d):
        return False
    return True

  def toAbsPath(self) -> "Dir":
    """
    deprecated
    """
    return self

class Img(File):
  """
  很不成熟, 尽量别用
  除非你真的知道你在干嘛
  """
  obj: Image.Image
  def __init__(self, *p: str):
    super(Img, self).__init__(*p)
    self.obj = Image.open(self.path)
    assert self.isImg, "is not img: %s" % self.path

  @property
  def isJpg(self) -> bool:
    # return self.obj.mode == "RGB" or (self.suffix.lower() == ".jpg" and self.obj.mode.lower() == "p")
    return self.suffix.lower() in [".jpg", ".jpeg"]

  @property
  def isPng(self) -> bool:
    # return self.obj.mode == "RGBA" or (self.suffix.lower() == ".png" and self.obj.mode.lower() == "p")
    return self.suffix.lower() == ".png"

  def close(self):
    self.obj.close()

  def resize(self, size: Tuple[int, int], resample=Image.LANCZOS) -> "Img":
    self.obj = self.obj.resize(size, resample=resample)
    return self

  def toAbsPath(self) -> "Img":
    """
    deprecated
    """
    return self

  # args 是 Image.save 的参数
  def saveAs(self, p="", **args):
    self.obj.save(p or self.path, **args)

class Jpg(Img):
  def __init__(self, *p: str):
    super(Jpg, self).__init__(*p)
    assert self.isJpg, "is not jpg: %s, mode: %s" % (self.path, self.obj.mode)

  def saveAs(self, p="", optimize=True, quality=90, progressive=True, subsampling=1) -> "Jpg":
    self.obj.save(p or self.path, format="JPEG", optimize=optimize, quality=quality, progressive=progressive, subsampling=subsampling)
    return self

  # quality = 0 时，不压缩
  def saveToPng(self, p="", quality=0) -> str:
    p = p or self.path
    base = Base(p)
    base.parent.createAsDir()
    suffix = ".png"
    name = base.fakeName if base.fakeSuffix.lower() == suffix else base.basename
    targetPath = os.path.join(base.dirname, "%s%s" % (name, suffix))
    rgba = self.obj.convert("RGBA")
    rgba.save(targetPath)
    if quality > 0:
      Png(targetPath).saveAs(quality=quality)
    return targetPath

  def toAbsPath(self) -> "Jpg":
    """
    deprecated
    """
    return self

class Png(Img):
  def __init__(self, *p: str):
    super(Png, self).__init__(*p)
    assert self.isPng, "is not png: %s, mode: %s" % (self.path, self.obj.mode)

  def saveAs(self, p="", quality=90) -> "Png":
    tempRoot = Base("/.tangUtils-pngquant-temp").createAsDir()
    p = p or self.path
    qualityStr = "%s-%s" % (quality, quality + 2)
    newPath = tempRoot.childOf("%s-%s.png" % (str(random.random()), str(random.random()))).path
    self.obj.save(newPath)
    subprocess.call("pngquant.exe --force --ext=.png --quality=%s %s" % (qualityStr, newPath))
    shutil.move(newPath, p)
    return self

  def saveToJpg(self, p="", optimize=True, quality=94, progressive=True, subsampling=1) -> str:
    p = p or self.path
    base = Base(p)
    base.parent.createAsDir()
    suffix = ".jpg"
    name = base.fakeName if base.fakeSuffix.lower() == suffix else base.basename
    targetPath = os.path.join(base.dirname, "%s%s" % (name, suffix))
    rgb = self.obj.convert("RGB")
    rgb.save(targetPath, optimize=optimize, quality=quality, progressive=progressive, subsampling=subsampling)
    return targetPath

  def toAbsPath(self) -> "Png":
    """
    deprecated
    """
    return self

class Json(File):
  def readAsJson(self) -> Any:
    s = super(Json, self).read()
    return json.loads(s)

  # indent为零时自动转为None(即不支持indent == 0, 我认为indent == 0不常用, 还不如让indent == None用得舒服点)
  def writeAsJson(self, obj, indent=2, ensure_ascii=False) -> "Json":
    with open(self.path, "w", encoding="UTF-8") as f:
      json.dump(obj, f, indent=indent if indent else None, ensure_ascii=ensure_ascii)
    return self

  def toAbsPath(self) -> "Json":
    """
    deprecated
    """
    return self

def getInputFiles() -> List["File"]:
  files = []
  for arg in sys.argv[1:]:
    base = Base(arg)
    if base.isFile:
      files.append(File(arg))
    elif base.isDir:
      files.extend(Dir(arg).allFiles)
  return files

Callback = Callable[[], None]

class Cmd:
  prompt: str
  callback: Callback
  next: List["Cmd"]

  def __init__(self, prompt: str, callback: Callback=None, next: List["Cmd"]=[]):
    super().__init__()
    self.prompt = prompt
    self.callback = callback
    self.next = next

def runCmdList(cmdList: List[Cmd]) -> bool:
  """
  返回值表示是否正常退出;
  True为正常退出;
  False表示非正常退出, 如"命令列表为空"或者"ctrl+c"退出等
  """
  if len(cmdList) == 0:
    print("命令列表为空")
    return False
  cmdMap: Dict[int, Cmd] = {}
  prompts = ["", "--- 可执行命令列表 ---"]
  i = 0
  for cmd in cmdList:
    i += 1
    cmdMap[i] = cmd
    prompts.append("%s: %s" % (i, cmd.prompt))
  prompts.append("------")
  prompts.append("")
  promptStr = "\n".join(prompts) + "请输入命令编号: "
  result = -1
  try:
    result = questionInt(promptStr)
  except KeyboardInterrupt:
    print("您已取消输入")
    return False
  while result not in cmdMap:
    try:
      result = questionInt("请输入有效命令: ")
    except KeyboardInterrupt:
      print("您已取消输入")
      return False
  if cmdMap[result].callback:
    cmdMap[result].callback()
  if len(cmdMap[result].next) > 0:
    runCmdList(cmdMap[result].next)
  return True

Size = Tuple[int, int]

def resizeWithin(origin: Size, target: Size) -> Size:
  """
  originW / originH == targetW / targetH
  """
  originW, originH = origin
  targetW, targetH = target
  if 0 in [originW, originH, targetW, targetH]:
    raise Exception("尺寸不得含有0")
  if originW < 0 or originH < 0:
    raise Exception("源尺寸必须均大于0")
  # 不允许是其他负数, 是为了防止使用者误输入
  if (targetW < 0 and targetW != -1) or (targetH < 0 and targetH != -1):
    raise Exception("目标尺寸不得为其他负数 (但可以为-1, 表示以另一个正数为标准, 保持比例缩放)")
  if targetW < 0 and targetH < 0:
    raise Exception("目标尺寸不得同时为负数")

  aspect = originW / originH

  if targetW < 0:
    return (math.floor(aspect * targetH), targetH)
  if targetH < 0:
    return (targetW, math.floor(targetW / aspect))
  if aspect < targetW / targetH: # 瘦高, 以高为准
    return (math.floor(aspect * targetH), targetH)
  # 否则以宽为准
  return (targetW, math.floor(targetW / aspect))
