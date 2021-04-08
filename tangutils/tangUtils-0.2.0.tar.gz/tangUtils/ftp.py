# encoding='utf-8'
from typing import List
import os, shutil, re, sys
from ftplib import FTP
from tangUtils.main import resolve, Base, File, Dir, question

def toLatin(p: str):
  return p.encode("utf-8").decode("latin1")

class TangFtp(object):
  host: str
  port: int
  username: str
  password: str
  remoteRoot: str
  localRoot: str
  ftp: FTP = None

  def __init__(self, host="", port=21, username="", password="", remoteRoot="/", localRoot="/"):
    super().__init__()
    self.host = host
    self.port = port
    self.username = username
    self.password = password
    self.remoteRoot = remoteRoot
    self.localRoot = localRoot
    self.__login()

  def __login(self) -> "TangFtp":
    self.__logout()
    self.ftp = FTP()
    self.ftp.connect(host=self.host, port=self.port)
    self.ftp.login(user=self.username, passwd=self.password)
    return self

  def __logout(self) -> "TangFtp":
    if self.ftp:
      self.ftp.close()
    self.ftp = None
    return self

  def __createDirIfNotExists(self, remoteDirPath: str):
    oldDir = self.ftp.pwd()
    if remoteDirPath[0] == "/":
      self.ftp.cwd("/")
    for subName in remoteDirPath.split("/"):
      if bool(subName):
        try:
          self.ftp.cwd(subName)
        except Exception:
          self.ftp.mkd(subName)
          self.ftp.cwd(subName)
    self.ftp.cwd(oldDir)

  def __ftpDownload(self, fromRemotePath: str, toLocalPath: str) -> bool:
    buffSize = 1024
    success = True
    Base(toLocalPath).createAsFile()
    with open(toLocalPath, "wb") as fp:
      try:
        self.ftp.retrbinary("RETR %s" % toLatin(fromRemotePath), fp.write, buffSize)
        self.ftp.set_debuglevel(0)
      except Exception as e:
        print("【ftp download error】")
        print(e)
        success = False
    return success

  def __ftpUpload(self, fromLocalPath: str, toRemotePath: str) -> bool:
    self.__createDirIfNotExists(toLatin(Base(toRemotePath).parent.path))
    buffSize = 1024
    success = True
    # 这儿本地文件必须存在, 本来就是上传文件, 本地没有文件你上传什么? 所以就没判断
    with open(fromLocalPath, "rb") as fp:
      try:
        self.ftp.storbinary("STOR %s" % toLatin(toRemotePath), fp, buffSize)
        self.ftp.set_debuglevel(0)
      except Exception as e:
        print("【ftp upload error】")
        print(e)
        success = False
    return success

  def upload(self, s: List[Base]):
    total = len(s)
    for i, base in enumerate(s):
      print("%s / %s" % (i + 1, total), end="\r")
      relPath = os.path.relpath(base.path, self.localRoot)
      # 两点或者斜杠开头, 都不在目录中
      if re.match(r"^(\.\.|\\|\/)", relPath):
        print("--%s--%s--" % (base.path, relPath))
        print("文件错误: 【%s】不在根目录【%s】中" % (base.path, self.localRoot))
        return self
      remotePath = resolve(self.remoteRoot, relPath)
      if base.isFile:
        self.__ftpUpload(base.path, remotePath)
      elif base.isDir:
        self.upload(Dir(base.path).allFiles)
    return self

  def download(self, s: List[Base]):
    total = len(s)
    for i, base in enumerate(s):
      print("%s / %s" % (i + 1, total), end="\r")
      relPath = os.path.relpath(base.path, self.localRoot)
      # 两点或者斜杠开头, 都不在目录中
      if re.match(r"^(\.\.|\\|\/)", relPath):
        print("文件错误: 【%s】不在根目录【%s】中" % (base.path, self.localRoot))
        return self
      remotePath = resolve(self.remoteRoot, relPath)
      if base.isFile:
        self.__ftpDownload(remotePath, base.path)
      elif base.isDir:
        self.download(Dir(base.path).allFiles)
    return self

if __name__ == "__main__":
  try:
    ftp = TangFtp()
    tar = [Base(p) for p in sys.argv[1:]]
    ftp.upload(tar)
  except Exception as e:
    print(e)
    question("输入 任意字符 以退出", "Y")
