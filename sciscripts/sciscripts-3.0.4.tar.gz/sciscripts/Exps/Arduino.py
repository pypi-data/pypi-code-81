#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210410
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Exps.Arduino] Loading dependencies...')
import os
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime

from sciscripts.IO import Arduino
print('[Exps.Arduino] Done.')


def CheckPiezoAndTTL(XLim=(0, 192), YLim=(-5, 1028), FramesPerBuf=192, BaudRate=115200):
    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)

    Plots = [[], []]
    Plots[0] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]
    Plots[1] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        for Plot in Plots:
            Plot.set_ydata([])
        return Plots

    def PltUp(n):
        Data = [[0]*FramesPerBuf, [0]*FramesPerBuf]
        for Frame in range(FramesPerBuf):
            Temp = ArduinoObj.readline().decode(); Temp = Temp.split()
            if len(Temp) is not 2:
                Temp = [0, 0]
            Data[0][Frame] = Temp[0]; Data[1][Frame] = Temp[1]

        for Index, Plot in enumerate(Plots):
            Plot.set_ydata(Data[Index])

        return tuple(Plots)

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def Oscilloscope(XLim=(0, 192), YLim=(-5, 1028), FramesPerBuf=192, BaudRate=115200):

    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)
    Plot = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        Data = []
        Plot.set_ydata(Data)
        return Plot,

    def PltUp(n):
        Data = []
        for Frame in range(FramesPerBuf):
            Data.append(ArduinoObj.readline())
        Plot.set_ydata(Data)
        return Plot,

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def ReadAnalogIn(FramesPerBuf, BaudRate=115200, FileName=''):
    """
    Grab serial data and continuously write to a .dat file.

    The shape will be in the filename.
    """

    ArduinoObj = Arduino.CreateObj(BaudRate)
    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    DataLen = 0

    try:
        while True:
            Data = Arduino.GetSerialData(FramesPerBuf, ArduinoObj)
            with open(Date+'.dat', 'ab') as File: File.write(Data.tobytes())
            DataLen += Data.shape[0]

    except KeyboardInterrupt:
        pass

    os.rename(Date+'.dat', FileName+'_'+str(DataLen)+'x2.dat')


