""" apu.io anton python utils input output module """

__version__ = (0, 0, 2)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from typing import Any
from pathlib import Path as pp

from apu.io.format.csv import CSV
from apu.io.format.dill import DILL
from apu.io.format.json import (JSON, JSONL)
from apu.io.format.matlab import MAT
from apu.io.format.np import (NPY, NPZ)
from apu.io.format.pickel import PICKLE
from apu.io.format.yaml import YAML
from apu.io.format.h5 import H5
from apu.io.format import supported_format

from apu.io.dill import reconstruct, load
from apu.io.fileformat import FileFormat
from apu.io.hash import _calc_
from apu.io.net import (download, urlread)
from apu.io.path import Path

__all__ = [
    'reconstruct', "load", "FileFormat", "_calc_", "download", "urlread",
    "Path"
]


def read(filepath: str, **kwargs: Any) -> Any:
    """ read data to file """
    supported_formats = supported_format()

    filedatapath = pp(filepath).suffix
    filedata = None

    for suffix, fileformat in supported_format().items():
        if filedatapath in suffix:
            filedata = fileformat(path=filepath, kwargs=kwargs)
            break

    if filedata is not None:
        return filedata.read()

    raise NotImplementedError(f"File '{filepath}' does not end with one "
                              f"of the supported file name extensions. "
                              f"Supported are: {supported_formats.keys()}")


def write(filepath: str, data: Any, **kwargs: Any) -> Any:
    """ write data to file """

    supported_formats = supported_format()

    filedatapath = Path(filepath).suffix
    filedata = None

    for suffix, fileformat in supported_format().items():
        if filedatapath in suffix:
            filedata = fileformat(path=filepath, kwargs=kwargs, data=data)
            break

    if filedata is not None:
        return filedata.write()

    raise NotImplementedError(f"File '{filepath}' does not end with one "
                              f"of the supported file name extensions. "
                              f"Supported are: {supported_formats.keys()}")
