#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20200506
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[IO.Wav] Importing dependencies...')
import os

from scipy.io import wavfile
print('[IO.Wav] Done.')


def Read(File):
    Rate, Data = wavfile.read(File)
    if len(Data.shape) == 1:
        Data = Data.reshape((Data.shape[0], 1))

    return(Data, Rate)

def Write(Data, Rate, File):
    if '.' not in File: File +='.dat'
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)

    wavfile.write(File, Rate, Data)

