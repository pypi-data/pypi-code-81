#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20190428
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Analysis of evoked response potentials (ERPs) during the paired-click
behavioural paradigm. Still under development, so far the functions here are
super specific for a very customized experimental setup. Be careful.
"""

import numpy as np
import os
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.IO import IO


def Load(Folder, ImpedanceFile='', InfoFile=''):
    if 'Control_03' in Folder:
        ExtraCh = [33] if 'Treadmill' in Folder else [33,34]
        ChMap = [9, 13, 15, 18, 20, 6, 4, 5, 32, 1, 31, 29, 28, 27, 25, 26] + ExtraCh
    elif 'int' in [_.split('.')[-1] for _ in glob(Folder+'/*')]:
        ChMap = Analysis.RemapCh('CM16', 'RHAOM') + [17]
    else:
        if InfoFile:
            Info = IO.Txt.Read(InfoFile)
            ExtraCh = [Info['DAqs']['StimCh'], Info['DAqs']['TTLCh']]
        else:
            ExtraCh = [17] if 'Treadmill' in Folder else [17,18]
        ChMap = Analysis.RemapCh('Ciralli', 'None16') + ExtraCh

    Data, Rate = IO.DataLoader(Folder, ChannelMap=ChMap, ImpedanceFile=ImpedanceFile)
    if 'int' in [_.split('.')[-1] for _ in glob(Folder+'/*')]:
        D = np.vstack([Data[_] for _ in sorted(Data.keys(), key=lambda x: int(x))])
        Data = {'100': {'0': {'0': D}}}
        Rate = {'100': {'0': Rate}}

    Key = list(Data.keys())[0]
    Rec = sorted(Data[Key]['0'].keys(), key=lambda x: [int(i) for i in x])[0]
    Data, Rate = Data[Key]['0'][Rec], Rate[Key]['0']

    return(Data, Rate)


def GetTTLs(Signal, Folder):
    if 'SLFull' in Folder or 'SLFast' in Folder:
        L = Analysis.QuantifyTTLsPerRec(True, Signal, 0.6)
        S = Analysis.QuantifyTTLsPerRec(True, Signal, 0.15)
        TTLs = [s for s in S if True not in [l in L for l in np.arange(s-1, s+2)]]
        Bad = np.where((np.diff(TTLs) < 15000))[0]
        if len(Bad): del(TTLs[Bad[-1]])
    else:
        TTLs = Analysis.QuantifyTTLsPerRec(True, Signal, 4)
        if len(TTLs) == 101:
            Diff = np.diff(TTLs)[::2]
            Wrong = np.where(~((12000<Diff)*(Diff<18000)))[0][0]*2
            TTLs = np.concatenate((TTLs[:Wrong], TTLs[Wrong+1:]))

    return(TTLs)


def PairedERP(Data, Rate, TTLs, FilterFreq, FilterType, ERPWindow,
              File='PairedERP', Save=False):
    ChNo = Data.shape[1]
    TrialNo = len(TTLs)//2

    DataERPs = Analysis.FilterSignal(Data, Rate, FilterFreq, FilterOrder=2, Type=FilterType)
    ERPs = np.zeros((int(abs(ERPWindow[0])*Rate) + int(abs(ERPWindow[1])*Rate), TrialNo, ChNo),
                    DataERPs.dtype)
    for Ch in range(ChNo):
        ERPs[:,:,Ch] = Analysis.SliceData(
            DataERPs[:,Ch], TTLs[::2], int(abs(ERPWindow[0])*Rate), int(abs(ERPWindow[1])*Rate), True
        )

    X = np.linspace(ERPWindow[0], ERPWindow[1], ERPs.shape[0])

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        IO.Bin.Write(ERPs, File+'.dat')
        IO.Bin.Write(X, File+'_X.dat')

    return(ERPs, X)


def GetSxx(Data, Rate, Window):
    DataSxx = []
    for C in range(Data.shape[1]):
        Fxx, txx, Sxx = Analysis.Spectrogram(Data[:,C], Rate, int(Window*Rate), Overlap=int(Window*Rate)//1.25)
        if not len(DataSxx):
            DataSxx = np.zeros((Fxx.shape[0], txx.shape[0], Data.shape[1]), Sxx.dtype)

        DataSxx[:,:,C] = Sxx

    return(Fxx, txx, DataSxx)


def GetTFD(DataSxx, DataFxx, FreqBands):
    DataTFD = {F: np.zeros((DataSxx.shape[1], DataSxx.shape[2]))
               for F in FreqBands}

    for F, Freq in FreqBands.items():
        FreqFxx = (DataFxx > Freq[0]) * (DataFxx < Freq[1])
        DataTFD[F] = DataSxx[FreqFxx,:,:].mean(axis=0)

    return(DataTFD)


