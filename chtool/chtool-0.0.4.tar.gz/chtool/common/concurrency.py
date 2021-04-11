from queue import Queue
from multiprocessing import Manager
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor, wait ,as_completed
import logging

def function():
    logging.info("print something to monitor the process")

# logging.basicConfig(level=logging.INFO)
# function()
# logging.basicConfig(leve=logging.WARNING)
# function()

import copy



class threadpool:
    """
    有返回结果
    """
    def __init__(self, arr, func,isresult=False,var_type='single',log_level='logging.INFO'):
        """

        :param arr:
        :param func:
        :param isresult:
        :param var_type: func 参数 位数: single / double
        :param log_level:  DEBUG < INFO < WARNING < ERROR < CRITICAL
        """
        self.sema = Semaphore(1)

        self.q = Queue()
        for w in arr:self.q.put(w)

        self.func = func
        self.i = 0
        self.result_q = Queue()
        self.isresult = isresult
        self.var_type = var_type

        LOG_FORMAT = "%(asctime)s >> %(message)s"
        logging.basicConfig(level=eval(log_level), format=LOG_FORMAT)


    def task(self):

        while not self.q.empty():
            word = self.q.get(block=False)

            self.sema.acquire()
            self.i += 1
            self.sema.release()

            if self.var_type == "double":
                if isinstance(word, (int, float, str, bytes)):
                    word = (word,)
                result = self.func(*word)

            else:
                result = self.func(word)

            if self.isresult:
                self.result_q.put(result)

            if self.q.empty():break

            logging.info('%s - %s' % (str(self.i), str(word)))

    def run(self, num):
        with ThreadPoolExecutor(max_workers=num) as pool:
            ec_list = [pool.submit(self.task) for _ in range(num)]

        wait(ec_list)


class processpool:

    def __init__(self, arr, func,isresult=False):
        self.q = Manager().Queue()
        for w in arr:
            self.q.put(w)
        self.func = func
        self.result_q = Manager().Queue()
        self.isresult = isresult

    def task(self):
        while not self.q.empty():

            word = self.q.get(block=False)


            if isinstance(word,(int,float,str,bytes)):
                word=(word,)
            result = self.func(*word)
            if self.isresult:
                self.result_q.put(result)


    def run(self, num):

        with ProcessPoolExecutor(max_workers=num) as pool:
            ec_list = [pool.submit(self.task) for _ in range(num)]

            wait(ec_list)




if __name__ == '__main__':
    arr=[1,2,3,4,5,6,7,8,9,0]

    def test(num):
        return num*2

    threadpool(arr,test,log_level='logging.INFO').run(1)

    # logging.info('over')
    print('over')