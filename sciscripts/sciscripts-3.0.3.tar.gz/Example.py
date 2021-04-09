#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 20210409
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from sciscripts.IO import IO
from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Plot import Plot


# Load data
Folder = 'DataSet/2018-08-13_13-25-45_1416'
Data, Rate = IO.DataLoader(Folder)
Rec0 = Data['100']['0']['0'][:,:16]
Rate0 = Rate['100']['0']
Time0 = np.arange(Rec0.shape[0])/Rate0


# Plot 50ms of all channels
Plot.AllCh(Rec0[:int(Rate0*0.05),:], Save=True, File='Plot1', Ext=['png'])


# Filtering
Rec0Theta = Analysis.FilterSignal(Rec0, Rate0, Frequency=[4,12], FilterOrder=2)
Rec0Gamma = Analysis.FilterSignal(Rec0, Rate0, Frequency=[30,100], FilterOrder=3)


# Plot raw, theta and gamma
Window = int(Rate0)
plt = Plot.Return('plt')
Fig, Axes = plt.subplots(1,3)
Axes[0] = Plot.AllCh(Rec0[:Window,:], Time0[:Window], Ax=Axes[0], lw=0.7)
Axes[1] = Plot.AllCh(Rec0Theta[:Window,:], Time0[:Window], Ax=Axes[1], lw=0.7)
Axes[2] = Plot.AllCh(Rec0Gamma[:Window,:], Time0[:Window], Ax=Axes[2], lw=0.7)

AxArgs = {'xlabel': 'Time [s]'}
for Ax in Axes: Plot.Set(Ax=Ax, AxArgs=AxArgs)

Axes[0].set_ylabel('Voltage [µv]')
Axes[0].set_title('Raw signal')
Axes[1].set_title('Theta [4-12Hz]')
Axes[2].set_title('Gamma [30-100Hz]')

Plot.Set(Fig=Fig)
Fig.savefig('Plot2.png')
plt.show()
