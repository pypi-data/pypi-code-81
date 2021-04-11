#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210125
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('Loading Analysis.Images dependencies...')
import numpy as np
import matplotlib.pyplot as plt
print('Loaded.')


def Expectation(c):
    E = np.mean(c)
    return(E)


def Normalize(Files, Min=1, Max=99):
    IMGs, IMGsNorm = [], []
    for File in Files:
        IMG = plt.imread(File)
        IMGs.append(IMG)

    AllMax = max([_.max() for _ in IMGs])
    for I,IMG in enumerate(IMGs):
        IMG2 = IMG/AllMax
        IMGMin = np.percentile(IMG2.ravel(), Min)
        IMGMax = np.percentile(IMG2.ravel(), Max)

        IMG2[IMG2<IMGMin] = IMGMin
        IMG2[IMG2>IMGMax] = IMGMax
        IMG2 -= IMGMin
        IMG2 /= IMG2.max()

        IMGsNorm.append(IMG2)
        # plt.imsave(Files[I], IMG2)
        # Fig, Axes = plt.subplots(1,2,figsize=(15,10))
        # Axes[0].imshow(np.flipud(IMG))
        # Axes[1].imshow(np.flipud(IMG2))
        # plt.show()

    return(IMGsNorm)


def OptimalGain(StD):
    OG = 1/StD
    return(OG)


def Variance(c, Gain=1):
    V = Gain*Expectation(c)
    return(V)


