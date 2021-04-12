""" apu.encoding.json: anton python utils
encoding module for json"""

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.encoding.json.np import (NumpyEncoder, NumpyDecoder)

__all__ = ['NumpyEncoder',
           'NumpyDecoder']
