# -*- coding: utf-8 -*-
# Author: TAO Nianze (Augus)
import numpy as np
from decimal import Decimal


class IntervalS:
    def __init__(self,
                 _interval: str):
        # R = IntervalS('(-inf, inf)')
        self.left_c = _interval[0]
        self.right_c = _interval[-1]
        if (self.left_c not in ['(', '[']) \
                or (self.right_c not in [')', ']']):
            raise ValueError
        self.left_b = Decimal(
            _interval.split(',')[0][1:],
        )
        self.right_b = Decimal(
            _interval.split(',')[-1][:-1],
        )
        if self.left_b >= self.right_b:
            raise ValueError

    def contains(self,
                 n):
        num = Decimal(str(n))
        con1, con2, con3 = False, True, True
        if self.left_b <= num <= self.right_b:
            con1 = True
        if self.left_c == '(' and num == self.left_b:
            con2 = False
        if self.right_c == ')' and num == self.right_b:
            con3 = False
        if con1 and con2 and con3:
            return True
        else:
            return False


rgb = (
    [0, 121, 126],
    [5, 154, 99],
    [132, 188, 79],
    [255, 221, 53],
    [255, 184, 46],
    [254, 150, 51],
    [228, 73, 51],
    [200, 1, 58],
    [148, 2, 101],
    [120, 0, 62],
    [79, 0, 24],
)  # colour map
rgb = np.array(rgb)/255.0
_classes = [
    IntervalS('[0, 25]'),
    IntervalS('(25, 50]'),
    IntervalS('(50, 75]'),
    IntervalS('(75, 100]'),
    IntervalS('(100, 125]'),
    IntervalS('(125, 150]'),
    IntervalS('(150, 175]'),
    IntervalS('(175, 200]'),
    IntervalS('(200, 300]'),
    IntervalS('(300, 400]'),
    IntervalS('(400, inf)')
]
defeat_settings = {
    "scatter size": 1,
    "y label size": 15,
    "title size": 15,
    "subtitle size": 20,
    "date format": "%Y-%m-%d",
    "frequency": "5m"
}
