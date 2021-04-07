
import time
from swissarmykit.utils.timeit import timeit

@timeit
def foo():
    time.sleep(4)

foo()