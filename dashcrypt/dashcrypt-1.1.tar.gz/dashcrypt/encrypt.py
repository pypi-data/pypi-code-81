import hashlib
import base64
import zlib

from .error import ValueException
from .error import ModeException
from .utils import alphabet
from .utils import _binnary

class Encrypt:
    def __init__(self, s=None):
        super().__init__()

        self.s = s
        self.automode = True
        self.mode = 0
        self.algorithm = ["md5", "sha1", "sha224", "sha512", "blake2b"]

        self.checkByte()

    def _length(self):
        if self.s is None:
            raise ValueException
        else:
            length = len(self.s)
            if length == 0:
                raise ValueException("String cannot be empty")
            return length

    def checkByte(self):
        if isinstance(self.s, bytes):
            return True
        else:
            raise ValueException("String must be bytes")

    def setMode(self, value):
        if isinstance(value, bool):
            self.automode = value
        else:
            self.automode = False
            raise ValueException("argument must be boolean")
        
    def generateHash(self):
        if self.automode is True:
            length = self._length()
            if length <= 10:
                self.mode = 0
            elif length <= 30:
                self.mode = 1
            elif length <= 50:
                self.mode = 2
            elif length <= 70:
                self.mode = 3
            else:
                self.mode = 4
        else:
            if self.mode > 4:
                raise ModeException("There are 4 kinds of modes")
        hashes = hashlib.new(self.algorithm[self.mode])
        hashes.update(self.s)
        return hashes.hexdigest()

    def modifyText(self, text):
        res, index = _binnary()
        for s in text:
            res += alphabet[s]
        return res.encode()

    def crypt(self, mode=None):
        if mode is None:
            self.automode = True
        else:
            self.mode = mode
        hashes = self.generateHash()
        hash_modify = self.modifyText(hashes)
        return hash_modify