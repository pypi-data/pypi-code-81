from textwrap import wrap
class cipher():
  def __init__(self, chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[]\{}|;':\",./<>?\n ", keylen=2, offset=0):
    self.chars = chars
    self.keylen = keylen
    self.offset = offset
    con = {}
    for n in range(len(chars)):
      y = ""
      for x in range(1, keylen+1):
        y += chars[n-(x+offset)]
      con[chars[n]] = y
    self.cipherdex = con
  def cipher(self, string):
    o = ""
    for n in range(len(string)):
      o += self.cipherdex[string[n]]
    return o
  def decipher(self, citext):
    citext = wrap(citext, self.keylen)
    con = ""
    for n in range(len(citext)):
      con+=self.cipherdex[list(self.cipherdex).index(citext[n][0])+1]
    return con
  def __str__(self):
    e = "\n"
    re = "\‌n"
    return f'Cipher with chars "{self.chars.replace(e, re)}", keylen as "{self.keylen}" and offset as "{self.offset}"'