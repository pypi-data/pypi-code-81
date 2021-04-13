# -*- coding: utf-8 -*-

# This code is part of ESVG.
#
# (C) Copyright Easygraph 2020.
#
"""
ESVG class for defining easing functions
"""
import math

def poly5(*args):
    v = 0
    if len(args) > 0 and args[0] is not None:
        v = args[0]
    return (lambda t: 240/7 * (1 - v) * ((t-.5)**3 / 6 - (t-.5)**5/5) + v*(t-.5) + 1/2)

def circ_quarter(*args):
    p = 2
    if len(args) > 0 and args[0] is not None:
        v = args[0]
    return (lambda t: (1 - (1-t)**p)**(1/p))

def _spring(a, m, k, c, t):
    if t == 1:
        return 1
    z = 1/(1-t) - 1
    if c**2 > 4*m*k:
        D = (c**2-4*m*k)**(1/2)
        return a * (math.exp(z*(-c + D)/(2*m)) + math.exp(z*(-c - D)/(2*m)))
    elif c**2 < 4*m*k:
        w = (4*m*k - c**2)**(1/2) / (2*m)
        return a * math.exp(-c*z/(2*m)) * math.sin(w*z)
    else:
        return a * z * math.exp(-c*z/(2*m))

def spring(*args):
    a = 1.4
    m = 0.05
    k = 4
    c = 0.2
    n_args = len(args)

    if n_args > 0 and args[0] is not None:
        a = args[0]
    if n_args > 1 and args[1] is not None:
        m = args[1]
    if n_args > 2 and args[2] is not None:
        k = args[2]
    if n_args > 3 and args[3] is not None:
        c = args[3]

    return (lambda t: _spring(a, m, k, c, t))
