from extended_int import int_inf
from typing import Callable

def heaviside(x: int, sTime: int, eTime: int = int_inf):
    if x >= sTime and x <= eTime:
        return 1
    else:
        return 0

def combineFuncs(a: Callable, b: Callable) -> Callable:
    return lambda x: a(x) + b(x)
