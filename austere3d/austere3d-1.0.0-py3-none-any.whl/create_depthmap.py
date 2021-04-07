#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.misc
from math import atan, cos, exp, pi, sin, sqrt

depthxSize = 1400; depthySize = 1050 # 4:3 aspect ratio
wallpaperxSize = 100 # horizontal shift of depth image

##############################################################################

def make_depthmap(function):

    NColors = 256
    print function
    depthmap_picture = np.zeros((depthySize,depthxSize))

    for irow in range(depthySize):
        for icol in range(depthxSize):
            # x,y are roughly in the range -1, ..., +1:
            x = 1.1 * (2.*icol+0.5*wallpaperxSize-depthxSize) / depthySize
            y = 1.1 * (depthySize-2.*irow)                    / depthySize
            r2 = x**2 + y**2
            if (function == 'blackhole'):
                depth = (NColors-1 - int((NColors-1) * exp(-2*r2) + 0.5))
            if (function == 'bumps'):
                depth = sin(5*x)*cos(5*y)
            if (function == 'donut'):
                inner = 0.4
                outer = 0.95
                if r2 < outer**2 and r2 > inner**2:
                    tmp = (2*sqrt(r2)-inner-outer) / (outer-inner)
                    depth = (NColors/2 + int((NColors/2-1) * sqrt(1-tmp**2) + 0.5))
                else:
                    depth = 0
            if (function == 'ripples'):
                depth = (NColors/2) + (NColors/2) * cos(10*sqrt(r2)) * max(1-0.3*r2,0)
            if (function == 'sombrero'):
                depth = NColors * abs(1.5*r2-1)
                if (r2>1.7): depth = 0
                if ((1.5*r2>1) and (depth>0.4*NColors)):
                    depth = 0.4*NColors
            if (function == 'upanddown'):
                depth = NColors * (x + y) * exp(-4.*r2)
                if (depth<-NColors): depth = -NColors
                if (depth>NColors):  depth = NColors
            if (function == 'vortex'):
                if (x==0):
                    angle = 3*pi/2 if (y<0) else pi/2
                else:
                    angle = atan(y / x)
                if (x<0):
                    angle += pi
                gauss = exp(-2*r2)
                depth = int(0.5 + (NColors-1) * (1 - gauss**2) *
                    (1 + 0.5 * gauss * (sin(5 * (3*r2*pi/4-angle)))) - 1)
            depthmap_picture[irow,icol] = depth

    # produce grayscale image:
    scipy.misc.imsave('depthmap/' + function + '.png', depthmap_picture)

##############################################################################

if __name__ == '__main__':

    make_depthmap('blackhole')
    make_depthmap('bumps')
    make_depthmap('donut')
    make_depthmap('ripples')
    make_depthmap('sombrero')    
    make_depthmap('upanddown')
    make_depthmap('vortex')

##############################################################################
