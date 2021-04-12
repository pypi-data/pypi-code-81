""" apu.dp: anton python utils design pattern module """

__version__ = (0, 0, 3)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.dp.null import Null
from apu.dp.iterator import (AlphabeticalOrderIterator,
                            AlphabeticalOrderCollection)
from apu.dp.singleton import (singleton, Singleton)

__all__ = ['Null',
           "AlphabeticalOrderIterator",
           "AlphabeticalOrderCollection",
           "singleton",
           "Singleton"]
