"""
@author  : MG
@Time    : 2021/4/7 9:11
@File    : func.py
@contact : mmmaaaggg@163.com
@desc    : 用于保持一些常用函数工具
"""
import numpy as np


def is_cross(price1: np.ndarray, price2: np.ndarray) -> int:
    """
    判断 price1 price2 两个价格序列是否交叉。price1 上传 price2 返回 1；下穿返回-1，否则返回 0
    :param price1:
    :param price2:
    :return:
    """
    if price1[-2] < price2[-2] and price1[-1] >= price2[-1]:
        return 1
    elif price1[-2] > price2[-2] and price1[-1] <= price2[-1]:
        return -1
    else:
        return 0


if __name__ == "__main__":
    pass
