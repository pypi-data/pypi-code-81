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
def GetPSD(System, Setup):
    PSD = IO.Bin.Read(CalibrationPath+'/'+System+'/'+Setup+'/PSD')[0]
    return(PSD)


def GetSoundIntensity(System, Setup):
    SoundIntensity = IO.Bin.Read(CalibrationPath+'/'+System+'/'+Setup+'/SoundIntensity')[0]
    return(SoundIntensity)


def GetSoundRec(System, Setup, Freq=''):
    if Freq: Freq = '/'+Freq
    SoundRec = IO.Bin.Read(CalibrationPath+'/'+System+'/'+Setup+'/SoundRec'+Freq)[0]

    if Freq:
        SoundRec = {A.replace('_', '.'): AmpF for A, AmpF in SoundRec.items()}
    else:
        SoundRec = {F: {A.replace('_', '.'): AmpF for A, AmpF in Freq.items()}
                    for F, Freq in SoundRec.items()}

    return(SoundRec)


def Normalize(Data, System, Mode=''):
    AmpF = IO.Txt.Read(CalibrationPath+'/'+System+'/AmpF.txt')
    if Mode.lower() == 'in': Data *= AmpF['InAmpF']
    elif Mode.lower() == 'out': Data *= AmpF['OutAmpF']
    else: print('"Mode" should be "in" or "out"'); return(None)

    return(Data)


## Level 1
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

    # Tmp override
    SoundAmpF50_45 = {
        '8000-10000': [0.0017635, 0.00088175],
        '8000-18000': [0.0002105, 0.00010525],
        '9000-11000': [0.0014025, 0.00070125],
        '10000-12000': [0.000979, 0.0004895],
        '12000-14000': [0.001045, 0.0005225],
        '14000-16000': [0.0014025, 0.00070125],
        '16000-18000': [0.0021455, 0.00107275]
    }

    for db,dB in enumerate([50, 45]):
        if dB in Intensities:
            Ind = Intensities.index(dB)

            for F,Freq in SoundAmpF.items():
                Freq[Ind] = SoundAmpF50_45[F][db]
                SoundAmpF[F] = Freq

    return(SoundAmpF)

