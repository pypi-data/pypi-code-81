""" MapMatching4GMNS

Based on input network and given GPS trajectory data, the map-matching program
of Matching2Route aims to find most likely route in terms of node sequence in
the underlying network, with the following data flow chart.

The code is adopted and modified from
https://github.com/asu-trans-ai-lab/MapMatching4GMNS
"""

import ctypes
import collections
import heapq
import os.path
from sys import platform
import time

print("To avoid complex data folder settings, please always first put the input data on the current directory.")
print('call MapMatching4GMNS  dynamic library')
if platform.startswith('win32'):
    _dll_file = os.path.join(os.path.dirname(
        __file__), 'bin/MapMatching4GMNS.dll')
elif platform.startswith('linux'):
    _dll_file = os.path.join(os.path.dirname(
        __file__), 'bin/MapMatching4GMNS.so')
elif platform.startswith('darwin'):
    _dll_file = os.path.join(os.path.dirname(
        __file__), 'bin/MapMatching4GMNS.dylib')
else:
    raise Exception('Please build the shared library compatible to your OS\
                    using source files in engine_cpp!')


_cdll = ctypes.cdll.LoadLibrary(_dll_file)
_cdll.MapMatching4GMNS.argtypes = [ctypes.c_int]
agent_compu = _cdll.MapMatching4GMNS


def _optimal_MapMatching4GMNS_CAPI(mode):
    _cdll.MapMatching4GMNS(mode)


'''Two modes:
    modes 0: reading trace.csv, then automaticically generate input_agent.csv and output agent.csv
    model 1: reading input_agent.csv, then output agent.csv and link_performance.csv
'''
if __name__ == "__main__":
    start = time.time()
    _optimal_MapMatching4GMNS_CAPI(0)
    end = time.time()
    print('MapMatching4GMNS time cost: %.6f seconds' % (end - start))
    print("The output data is generated!")
