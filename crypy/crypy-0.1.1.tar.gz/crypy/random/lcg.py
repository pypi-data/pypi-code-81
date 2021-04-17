from functools import reduce
import math


class LCG:
    def __init__(self, a=None, c=None, m=None, s=None):
        if (a is None) and (c is None) and (m is None) and (type(s) == list) and (len(s) >= 4):
            diffs = [s1 - s0 for s0, s1 in zip(s, s[1:])]
            zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
            m = abs(reduce(math.gcd, zeroes))

        if (a is None) and (c is None) and (m is not None) and (type(s) == list) and (len(s) >= 3):
            a = (s[2]-s[1]) * pow(s[1]-s[0], -1, m) % m

        if (a is not None) and (c is None) and (m is not None) and (type(s) == list) and (len(s) >= 2):
            c = (s[1] - a*s[0]) % m
        elif (a is None) and (c is not None) and (m is not None) and (type(s) == list) and (len(s) >= 2):
            a = (s[1] - c) * pow(s[0], -1, m)

        if type(s) == list:
            s = s[-1]

        self.a = a
        self.c = c
        self.m = m
        self.s = s

    def __iter__(self):
        return self

    def __next__(self):
        self.s = (self.a * self.s + self.c) % self.m
        return self.s

    def next(self):
        return self.next()
