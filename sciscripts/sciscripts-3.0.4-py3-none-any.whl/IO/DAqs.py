#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170904
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
from sciscripts.IO import IO

CalibrationPath = os.environ['DATAPATH']+'/Tests/SoundMeasurements'


## Level 0
def NoCalibrationMsg(System, Setup):
    FullPath = f'{CalibrationPath}/{System}/{Setup}'
    Msg = f'No such file or directory: {FullPath}'+r'''
Calibration files for
    System ''' + System + r'''
    Setup  ''' + Setup + r'''
were not found. You have to calibrate your setup before using it, or manually
provide the voltage amplification factor that will be applied to the speaker
using the SoundAmpF variable.

For more details, read the sciscripts.Exps.SoundMeasurements documentation:
    sciscripts.Exps import SoundMeasurements
    print(SoundMeasurements.__doc__)
'''
    return(Msg)


# Level 1
def CalibrationLoad(Dataset, System, Setup):
    FullPath = f'{CalibrationPath}/{System}/{Setup}/{Dataset}'
    try:
        Data = IO.Bin.Read(FullPath)[0]
    except FileNotFoundError as e:
        raise Exception(NoCalibrationMsg(System,Setup)) from e

    return(Data)


def Normalize(Data, System, Mode=''):
    try:
        AmpF = IO.Txt.Read(CalibrationPath+'/'+System+'/AmpF.txt')
    except FileNotFoundError as e:
        raise Exception(NoCalibrationMsg(System,'')) from e

    if Mode.lower() == 'in': Data *= AmpF['InAmpF']
    elif Mode.lower() == 'out': Data *= AmpF['OutAmpF']
    else: print('"Mode" should be "in" or "out"'); return(None)

    return(Data)


# Level 2
def GetPSD(System, Setup):
    PSD = CalibrationLoad('PSD', System, Setup)
    return(PSD)


def GetSoundIntensity(System, Setup):
    SoundIntensity = CalibrationLoad('SoundIntensity', System, Setup)
    return(SoundIntensity)


def GetSoundRec(System, Setup, Freq=''):
    if Freq: Freq = '/'+Freq
    SoundRec = CalibrationLoad('SoundRec'+Freq, System, Setup)

    if Freq:
        SoundRec = {A.replace('_', '.'): AmpF for A, AmpF in SoundRec.items()}
    else:
        SoundRec = {F: {A.replace('_', '.'): AmpF for A, AmpF in Freq.items()}
                    for F, Freq in SoundRec.items()}

    return(SoundRec)


# Level 3
def dBToAmpF(Intensities, System, Setup):
    print('Converting dB to AmpF...')
    SoundIntensity = GetSoundIntensity(System, Setup)
    SoundIntensity['dB'] = SoundIntensity['dB'][:-1,:]
    SoundIntensity['AmpFs'] = SoundIntensity['AmpFs'][:-1]


    SoundAmpF = {
        Freq: [
            float(min(SoundIntensity['AmpFs'],
                      key=lambda i:
                          abs(SoundIntensity['dB'][SoundIntensity['AmpFs'].tolist().index(i),F]-dB)
            ))
            for dB in Intensities
        ]
        for F,Freq in enumerate(SoundIntensity['Freqs'])
    }

    return(SoundAmpF)

