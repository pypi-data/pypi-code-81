import time
import logging


# 计算时间函数
def cost_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        res = func(*args, **kw)
        logging.info('Function [%s] run time cost %.2f s' % (func.__qualname__, time.time() - local_time))

        return res
    return wrapper




