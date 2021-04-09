
import time
import logging
logger = logging.getLogger(__file__)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.debug(f"{method.__name__}  {(te - ts) * 1000} ms")
        return result
    return timed
