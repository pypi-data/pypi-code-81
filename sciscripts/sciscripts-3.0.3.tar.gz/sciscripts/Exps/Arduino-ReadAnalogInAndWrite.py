#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180206
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
from datetime import datetime

from sciscripts.IO import Arduino


def Run(FramesPerBuf, FileName='', Plot=False):
    """
    Grab serial data and continuously write to a .dat file.
    The shape will be in the filename.
    """
    #if Plot: PlotThread()

    ArduinoObj = Arduino.CreateObj(115200)
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

if __name__ == "__main__":
    Run(256, 'Test')

