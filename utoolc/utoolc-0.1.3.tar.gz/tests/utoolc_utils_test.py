import sys
import time
from utoolc.utils import utils
# 以下两种使用PrintLogger均可
# pml.PrintLogger()
from utoolc.utils import print_msg_to_log_model as pml
# PrintLogger()
from utoolc.utils.print_msg_to_log_model import PrintLogger as PrintLogger2

from utoolc.utils.start_to_end_time_consuming import start_and_end


def test():
    utils.print_a_line()
    utils.print_a_line(0)
    utils.print_a_line(50, 100)
    utils.print_a_line(100)


def test2():
    utils.print_a_line(100)
    sys.stdout = pml.PrintLogger('utoolc_utils_test.py.log')  # 监听所有的print到log日志 封装类 如不需要打印所有输出print的log日志，隐掉这段即可
    utils.print_a_line(100)
    utils.print_a_line(100)


def test3():
    utils.print_a_line(100)
    sys.stdout = PrintLogger2('utoolc_utils_test.py.2.log')  # 监听所有的print到log日志 封装类 如不需要打印所有输出print的log日志，隐掉这段即可
    utils.print_a_line(100)
    utils.print_a_line(100)


def test4():
    start_and_end(True, 1)
    print('...执行中...')
    time.sleep(3)
    start_and_end(True, 1)


if __name__ == '__main__':
    test()
    # test2()
    # test3()
    test4()
