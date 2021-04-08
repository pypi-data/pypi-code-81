from typing import Union, List, Tuple
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from tangUtils.main import File

from email import encoders
from email.header import Header
from email.utils import formataddr, formatdate, COMMASPACE

from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# str: ip address
# Tuple[str, str]: (username, ip address)
Addr = Union[str, Tuple[str, str]]

DefaultPlainText = "您的客户端无法显示此类型的消息, 请换用其它客户端以查看该超文本内容(text/html)"

def _encode(s: str) -> str:
  return Header(s, "utf-8").encode()


def _decodeAddr(_addr: Addr) -> Tuple[str, str]:
  """
    _addr:
      str: 表示昵称和地址均为该值
      Tuple[str, str]: 等价于(username, ip address)
    return (username, ip address)
  """
  _type = type(_addr)
  if _type == str:
    name = _addr
    addr = _addr
  elif _type == tuple:
    name, addr = _addr
  else:
    raise Exception("arguments type error, accept str or Tuple[str, str], but got", _addr)
  return (name, addr)


def _formatAddr(_addr: Addr):
  """
    返回格式化后的收/发件人
    类似于  username <ip-address@mail.com>
  """
  name, addr = _decodeAddr(_addr)
  encodedName = _encode(name)
  return formataddr((encodedName, addr))


class Mail(object):
  """
    所有类方法都没有加 try/except, 如有需要则自己添加
  """
  # 发件人昵称
  fromName: str
  # 发件人邮箱地址
  fromAddr: str
  # 发件人邮箱授权码
  password: str
  # SMTP服务器地址, 默认为 qq 邮箱: "smtp.qq.com"
  smtpServer: str
  # SMTP服务器端口, 默认为 SMTP_SSL_PORT
  smtpPort: int
  # SMTP_SSL
  server: SMTP_SSL
  # 登录标记
  loginFlag = False

  def __init__(self, fromAddr: Addr, password: str, smtpServer="smtp.qq.com", smtpPort=SMTP_SSL_PORT, debugLevel=0):
    super().__init__()
    self.fromName, self.fromAddr = _decodeAddr(fromAddr)
    self.password = password
    self.smtpServer = smtpServer
    self.smtpPort = smtpPort
    self.setServer(smtpServer, smtpPort, debugLevel)

  def setServer(self, smtpServer="smtp.qq.com", smtpPort=SMTP_SSL_PORT, debugLevel=0):
    print("正在连接邮箱服务器...")
    self.server = SMTP_SSL(self.smtpServer, self.smtpPort)
    self.loginFlag = False
    self.server.set_debuglevel(debugLevel)
    return self

  def login(self):
    print("正在登录邮箱...")
    self.server.login(self.fromAddr, self.password)
    self.loginFlag = True
    return self

  def quit(self):
    self.server.quit()
    self.loginFlag = False
    return self

  def sendTo(self, toAddr: List[Addr], subject="", fallbackText=DefaultPlainText, html="", attachment: List[File] = []):
    print("正在发送消息...")
    if not self.loginFlag:
      self.login()
    # 如果登录之后, 登录标记依旧为否, 则取消消息发送
    if not self.loginFlag:
      raise Exception("登录失败")
    msg = MIMEMultipart("alternative")
    msg["From"] = _formatAddr((self.fromName, self.fromAddr))
    msg["To"] = COMMASPACE.join([_formatAddr(item) for item in toAddr])
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = _encode(subject)

    msg.attach(MIMEText(fallbackText, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    for idx, f in enumerate(attachment):
      with open(f.path, "rb") as fp:
        part = MIMEApplication(fp.read())
      part.add_header("Content-Disposition", "attachment", filename=_encode(f.basename))
      part.add_header("content-ID", "<%s>" % idx)
      msg.attach(part)

    self.server.sendmail(self.fromAddr, [
      _decodeAddr(item)[1] for item in toAddr
    ], msg.as_string())
    return self
