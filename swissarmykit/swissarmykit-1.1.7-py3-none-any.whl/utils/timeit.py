
from functools import wraps
import time

from swissarmykit.conf import *


def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('ET:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return wrap


if __name__ == '__main__':
    import time

    @timeit
    def foo():
        time.sleep(3)

    foo()