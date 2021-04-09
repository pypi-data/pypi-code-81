#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180904
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import os
from pandas import DataFrame

from sciscripts.Analysis.Analysis import SignalIntensity
from sciscripts.IO import DAqs, IO

## Level 0
def GetMeasurements(System, Setup, Rate, MicSens_VPa, Noise=[]):
    print('Calculating PSD, RMS and dBSLP...')
    SoundRecPath = os.environ['DATAPATH']+'/Tests/SoundMeasurements/'+System+'/'+Setup+'/'+'SoundRec'
    Freqs = os.listdir(SoundRecPath)
    Freqs = sorted(Freqs, key=lambda x: int(x.split('-')[1]))

    AmpFs = [_.split('.')[0].replace('_','.')  for _ in os.listdir(SoundRecPath+'/'+Freqs[0]) if '.dat' in _]
    AmpFs = sorted(AmpFs, reverse=True, key=lambda x: float(x))

    PSD = {}
    SoundIntensity = {K: np.zeros((len(AmpFs), len(Freqs)), dtype='float32')
                      for K in ['dB', 'RMS']}

    for F, Freq in enumerate(Freqs):
        FreqBand = [int(_) for _ in Freq.split('-')]
        SoundRec = DAqs.GetSoundRec(System, Setup, Freq)

        if len(Noise):
            NoiseRMS = SignalIntensity(Noise[int(Rate*2):int(Rate*4),0], Rate, FreqBand, 1)[0]
            NoiseRMS = NoiseRMS['RMS']
        else:
            NoiseRMS = None

        for A, AmpF in enumerate(AmpFs):
            if AmpF not in SoundRec: continue

            si, psd = SignalIntensity(SoundRec[AmpF][:,0], Rate, FreqBand, MicSens_VPa, NoiseRMS)
            del(SoundRec[AmpF])
            for K in si.keys(): SoundIntensity[K][A,F] = si[K]
            for K in psd.keys():
                if K not in PSD:
                    PSD[K] = np.zeros((psd[K].shape[0], len(AmpFs), len(Freqs)),
                                      dtype='float32')
                PSD[K][:,A,F] = psd[K]

    SoundIntensity['Freqs'] = Freqs
    SoundIntensity['AmpFs'] = AmpFs
    SoundIntensity['Dimensions'] = ['AmpF', 'Freq']
    PSD['Freqs'] = Freqs
    PSD['AmpFs'] = AmpFs
    PSD['Dimensions'] = ['Data', 'AmpF', 'Freq']

    return(SoundIntensity, PSD)


def TexTableWrite(SoundIntensity, DataPath):
    TexTable = DataFrame([[[float(AmpF)] + [SoundIntensity['dB'][A,F]]
                           for F,Freq in enumerate(SoundIntensity['Freqs'])]
                         for A,AmpF in enumerate(SoundIntensity['AmpFs'])])

    with open(DataPath+'/'+'IntensityTable.tex', 'w') as File:
        # \usepackage{setspace}
        # \usepackage{titlesec}
        # \titleformat{\chapter}{\normalfont\LARGE\bfseries}{\thechapter.}{1em}{}
        # \cleardoublepage
        File.write(
        r"""%% Configs =====
\documentclass[12pt,a4paper]{report}
\usepackage[left=0.5cm,right=0.5cm,top=0.5cm,bottom=0.5cm]{geometry}
\usepackage{longtable}
% Document ======
\begin{document}
\section{Sound measurements}
"""     )
        File.write(TexTable.to_latex(longtable=True))
        File.write(r"""
\end{document}
"""     )

    return(None)


def Run(Rate, MicSens_dB, System, Setup, **Kws):
    DataPath = DAqs.CalibrationPath + '/' + System + '/' + Setup

    MicSens_VPa = 10**(MicSens_dB/20)
    # Noise = IO.Bin.Read(DAqs.CalibrationPath + '/' + System + '/Noise.dat')[0]
    Noise = []
    SoundIntensity, PSD = GetMeasurements(System, Setup, Rate, MicSens_VPa, Noise)

    ## Save analyzed data
    print('Saving analyzed data...')
    IO.DataWriter(SoundIntensity, DataPath+'/SoundIntensity', 'dat')
    IO.DataWriter(PSD, DataPath+'/PSD', 'dat')

    TexTableWrite(SoundIntensity, DataPath)
    print('Done.')
