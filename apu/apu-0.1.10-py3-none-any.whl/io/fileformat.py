""" working with file formates """
from typing import Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path

import tzlocal

from apu.io.hash import DIGITS

# pylint: disable=C0103,W0702
with_magic = False
try:
    import magic
    with_magic = True
except:
    print("cannot use magic")



# pylint: disable=W0311
class FileFormat(ABC):
    """ base class. so each object implements the same functions """
    def __init__(self, path: str,
                kwargs:Dict = None,
                data:Any = None) -> None:
        """ Set the informations """
        self._filepath = Path(path).absolute()

        if not self._filepath.exists():
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            self._filepath.touch(mode=0x755, exist_ok=True)

        self._args = kwargs if kwargs is not None else {}
        self.data = data

    @classmethod
    def suffix(cls):
        """ file extentions """
        return tuple()

    @abstractmethod
    def read(self):
        """ read information from file into data buffer """

    @abstractmethod
    def write(self, sink:str, create: bool = True) -> None:
        """ write buffer into file"""

    def __exists(self, create: bool = False) -> bool:
        """ does the file exists? if not exists, we can create the file """
        if self._filepath.exists():
            return True

        if create:
             self._filepath.touch("755", exist_ok=True)
        else:
            raise FileNotFoundError(f"cannot find {self._filepath}")

        return False or create

    @property
    def creation_time(self):
        """ date of creation """
        timezone = tzlocal.get_localzone()
        #not tested on windows
        return datetime.fromtimestamp(
            self._filepath.lstat().st_ctime).replace(tzinfo=timezone)

    @property
    def modification_time(self):
        """ date of modification """
        timezone = tzlocal.get_localzone()
        return datetime.fromtimestamp(
            self._filepath.lstat().st_mtime).replace(tzinfo=timezone)

    @property
    def access_time(self):
        """ date of last access """
        timezone = tzlocal.get_localzone()
        return datetime.fromtimestamp(
            self._filepath.lstat().st_atime).replace(tzinfo=timezone)

    def meta(self) -> Any:
        """ aditional meta informations """
        meta: Dict[str, Any] = {
            "filepath": self._filepath.absolute(),
            "creation_data": self.creation_time,
            "modification_time": self.modification_time,
            "access_time": self.access_time
        }

        if with_magic:
            try:
                f_mime = magic.Magic(mime=True, uncompress=True)
                f_other = magic.Magic(mime=False, uncompress=True)
                meta["mime"] = f_mime.from_file(meta["filepath"])
                meta["magic-type"] = f_other.from_file(meta["filepath"])
            except ImportError:
                pass
        else:
            meta["mime"] = "null"
            meta["magic-type"] = "null"


        return meta

    def fingerprint(self, method:str="sha1"):
        """ build file fingerprint """
        method = method.lower()
        assert (method in DIGITS.keys()
            ), f"cannot find the hashmethod. \
                please select on of {DIGITS.keys()}"
        assert (self.__exists(create=False)), f"{self._filepath} is not a file!"

        # retrun hashed file
        return DIGITS[method](self._filepath)

    def compair(self, fileformat, method="sha1"):
        """ compair two files utilizing the fingerprint """
        return str(self.fingerprint(method=method).hexdigest()) == \
                    str(fileformat.fingerprint(method=method).hexdigest())
