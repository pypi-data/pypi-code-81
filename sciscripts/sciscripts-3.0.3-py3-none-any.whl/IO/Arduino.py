# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to define functions allowing Arduino/Python integration.
"""

import numpy as np
import os
import time

from datetime import datetime
from serial import Serial
from serial.tools.list_ports import comports


## Level 0
def CreateObj(BaudRate):
    Port = comports()
    if Port: Arduino = Serial(Port[-1][0], BaudRate)
    else: Arduino = None

    return(Arduino)


def GetSerialData(FramesPerBuf, ArduinoObj):
    Data = np.zeros((FramesPerBuf, 2), dtype='float32')

    for F in range(FramesPerBuf):
        Line = ArduinoObj.readline()
        while Line in [b'\r\n', b'\n']:
            Line = ArduinoObj.readline()

        Data[F,0] = float(Line)
        Data[F,1] = time.clock()
        time.sleep(0.001)

    return(Data)


def Reset(Obj):
    Obj.setDTR(False)
    Obj.flushInput()
    Obj.setDTR(True)
    return(None)


## Level 1
def CheckPiezoAndTTL(BaudRate=115200, XLim=(0, 192), YLim=(-5, 1028),
                     FramesPerBuf=192):

    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    Arduino = CreateObj(BaudRate)

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
            Temp = Arduino.readline().decode(); Temp = Temp.split()
            if len(Temp) is not 2:
                Temp = [0, 0]
            Data[0][Frame] = Temp[0]; Data[1][Frame] = Temp[1]

        for Index, Plot in enumerate(Plots):
            Plot.set_ydata(Data[Index])

        return tuple(Plots)

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def WriteSerialData(FramesPerBuf, FileName='', Plot=False):
    """
    Grab serial data and continuously write to a .dat file. The shape will be
    in the filename.
    """
    #if Plot: PlotThread()

    ArduinoObj = CreateObj(115200)
    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    DataLen = 0

    try:
        while True:
            Data = GetSerialData(FramesPerBuf, ArduinoObj)
            with open(Date+'.dat', 'ab') as File: File.write(Data.tobytes())
            DataLen += Data.shape[0]

    except KeyboardInterrupt:
        pass

    os.rename(Date+'.dat', FileName+'_'+str(DataLen)+'x2.dat')
    return(None)


def Oscilloscope(BaudRate=115200, XLim=(0, 192), YLim=(-5, 1028),
                       FramesPerBuf=192):

    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    Arduino = CreateObj(BaudRate)

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
            Data.append(Arduino.readline())
        Plot.set_ydata(Data)
        return Plot,

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


