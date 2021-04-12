""" apu.mp: anton python utils multiprocessing module """

__version__ = (0, 0, 2)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.mp.parallel_for import parallel_for
from apu.mp.thread_funcrun import (thread_funcrun,
                                 thread_n_funcrun)

__all__ = ['parallel_for',
           'thread_funcrun',
           'thread_n_funcrun']
