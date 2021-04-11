# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to define functions allowing Arduino/Python integration.
"""

print('[IO.Arduino] Loading dependencies...')
import numpy as np
import time

from serial import Serial
from serial.tools.list_ports import comports
print('[IO.Arduino] Done.')


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
        Data[F,1] = time.perf_counter()
        time.sleep(0.001)

    return(Data)


def Reset(Obj):
    Obj.setDTR(False)
    Obj.flushInput()
    Obj.setDTR(True)
    return(None)


