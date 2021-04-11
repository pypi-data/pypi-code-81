#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2019-12-11
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

try:
    from circus.shared.parser import CircusParser
    from circus.shared.files import load_data
except Exception as e:
    raise Exception('SpyKING Circus not available. Please install it before importing this module.') from e

import os
import numpy as np
from glob import glob
from imp import load_source

from sciscripts.Analysis.Units import Units
from sciscripts.IO import IO
from sciscripts.Analysis.Plot import Plot
plt = Plot.Return('plt')


def GetAllClusters(AnalysisPath, Exp='Data_000'):
    # Get parameters
    AnalysisFile = '/'.join(AnalysisPath.split('/')[:-1]) + '/Units/' + AnalysisPath.split('/')[-2]
    InfoFile = glob(AnalysisPath+'/*dict')[0]

    Here = os.getcwd(); os.chdir(AnalysisPath)
    Params = CircusParser(Exp+'.dat'); Params.get_data_file()
    os.chdir(Here)

    SpkWidth = Params.getint('detection', 'N_t')
    SpkWindow = [-(SpkWidth//2)-(SpkWidth%2), SpkWidth//2]
    Results = load_data(Params, 'results')
    RawFiles = sorted(Params.get_data_file().get_file_names())

    PrbFile = AnalysisPath+'/'+Params.get('data', 'mapping')
    Prb = load_source('', PrbFile)
    ChNoTotal = Prb.total_nb_channels
    ChSpacing = Prb.channel_groups['0']['geometry']
    ChSpacing = abs(ChSpacing[0][1] - ChSpacing[1][1])

    Rate = Params.get_data_file().sampling_rate
    Channels = Prb.channel_groups['0']['channels']

    # Info
    DataInfo = IO.Txt.Read(InfoFile)
    Clusters = sorted(Results['spiketimes'].keys(), key=lambda x: int(x.split('_')[-1]))

    DataInfo['Analysis'] = {}
    DataInfo['Analysis']['Channels'] = Channels
    DataInfo['Analysis']['ChNoTotal'] = ChNoTotal
    DataInfo['Analysis']['ChSpacing'] = ChSpacing
    DataInfo['Analysis']['ClusterRecs'] = np.arange(len(RawFiles)).tolist()
    DataInfo['Analysis']['ClusterLabels'] = {Cl: Cluster for Cl, Cluster in enumerate(Clusters)}
    DataInfo['Analysis']['Rate'] = Rate
    DataInfo['Analysis']['RawData'] = RawFiles

    Recs = Units.GetRecsNested(DataInfo)
    ClusterRecs = [b for a in Recs for b in a]

    if ClusterRecs != DataInfo['Analysis']['ClusterRecs']:
        print('Wrong number of recordings! Cannot extract TTLs!')
        DataInfo['Analysis']['RecNoMatch'] = False
    else:
        DataInfo['Analysis']['RecNoMatch'] = True

    DataInfo['Analysis']['RecsNested'] = Recs


    # Get rec lengths and offsets
    RawLengths = []
    for F,File in enumerate(RawFiles):
        Data = np.memmap(File, 'int16')
        Data = Data.reshape((Data.shape[0]//ChNoTotal, ChNoTotal))

        RawLengths.append(Data.shape[0])

    RawOffsets = np.concatenate([[0], np.cumsum(RawLengths)[:-1]])

    DataInfo['Analysis']['RecLengths'] = RawLengths
    DataInfo['Analysis']['RecOffsets'] = RawOffsets

    GetSpkRec = np.vectorize(lambda Spk: np.where(RawOffsets <= Spk)[0][-1])
    # from numba import jit
    # FindRecs = jit(nopython=True)(np.vectorize(lambda Spk: np.where(RawOffsets <= Spk)[0][-1]))


    # Get spk times and clusters
    SpkTimes, SpkClusters = np.array([], 'int16'), np.array([], 'int16')
    for Cl,Cluster in enumerate(Clusters):
        SpkTimes = np.concatenate((SpkTimes, Results['spiketimes'][Cluster]))
        SpkClusters = np.concatenate((SpkClusters, np.array([Cl]*Results['spiketimes'][Cluster].shape[0])))

    # Get spk recs
    SpkRecs = GetSpkRec(SpkTimes)


    # Get all waveforms
    Waveforms = np.zeros((SpkTimes.shape[0], SpkWidth, len(Channels)), dtype='int16')
    for R,Rec in enumerate(RawFiles):
        print(f'Loading rec {R} of {len(RawFiles)}...')
        Data = np.memmap(Rec, 'int16')
        Data = Data.reshape((Data.shape[0]//ChNoTotal, ChNoTotal))

        SpkMask = SpkRecs == R
        SpkIndex = np.where(SpkMask)[0]

        for S,Spk in enumerate(SpkTimes[SpkMask]):
            Window = [Spk+_ for _ in SpkWindow]
            Window = [W-RawOffsets[R] for W in Window]
            if Window[0] < 0: Window = [_-Window[0] for _ in Window]
            Waveforms[SpkIndex[S],:,:] = Data[Window[0]:Window[1],Channels]


    IO.Bin.Write(Waveforms, AnalysisFile + '_' + Exp + '_AllClusters/Waveforms.dat')
    IO.Bin.Write(SpkTimes, AnalysisFile + '_' + Exp + '_AllClusters/SpkTimes.dat')
    IO.Bin.Write(SpkClusters, AnalysisFile + '_' + Exp + '_AllClusters/SpkClusters.dat')
    IO.Bin.Write(SpkRecs, AnalysisFile + '_' + Exp + '_AllClusters/SpkRecs.dat')
    IO.Txt.Write(DataInfo, AnalysisFile + '_' + Exp + '_AllClusters/Info.dict')

    return(None)

