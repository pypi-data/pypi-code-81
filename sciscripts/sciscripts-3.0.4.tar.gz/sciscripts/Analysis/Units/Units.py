#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Units.Units] Importing dependencies...')

import os
import numpy as np
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.IO import IO

print('[Analysis.Units.Units] Done.')


## Level 0
def FiringRate(SpkTimes, RecLen, Offset=0):
    Spks = SpkTimes-Offset
    FR = np.array([len(Spks[(Spks >= Sec) * (Spks < Sec+1)]) for Sec in range(RecLen)], dtype=int)
    return(FR)


def GetBestCh(Spks):
    # ChAmp = (Spks.mean(axis=0)**2).mean(axis=0)**0.5    # RMS - account for broadness
    ChAmp = abs(Spks.mean(axis=0)).max(axis=0)            # Max abs ampl
    BestCh = ChAmp.argmax()
    return(BestCh)


def GetRecsNested(DataInfo):
    Recs = [np.arange(len(DataInfo['Audio']['Intensities']))
            if V['Hz'] != 'Baseline' else np.array([0])
            for K,V in enumerate(DataInfo['ExpInfo'].values())]

    Recs = [len(_) for _ in Recs]

    Prev = 0
    for R,Rec in enumerate(Recs):
        Prev = Prev+len(Recs[R-1]) if R else 0
        Recs[R] = np.arange(Rec) + Prev

    return(Recs)


def ISI(SpkTimes, ISISize, Rate):
    ISIY = np.histogram(np.diff(SpkTimes), bins=np.arange(0, ISISize, 1/Rate))[0]
    return(ISIY)


def MergeUnits(UnitRec, UnitsFile='UnitRec.asdf', Save=False, Return=True):
    TotalNo = UnitRec['UnitId'].shape[0]
    StimNo = len(np.unique(UnitRec['StimType']))
    UnitNo = len(np.unique(UnitRec['UnitId']))
    RecNo = (TotalNo//UnitNo)//StimNo

    ## Ideal way - not working because, you know, it's not a spherical neuron in the vacuum :)
    # MergeList = [np.where((((
    #     (UnitRec['UnitId'] == Id) * (UnitRec['StimType'] == UnitRec['StimType'][I])) *
    #     (UnitRec['Freq'] == UnitRec['Freq'][I])) *
    #     # (UnitRec['StimType'] == UnitRec['StimType'][I])) *
    #     (UnitRec['dB'] == UnitRec['dB'][I])) *
    #     (UnitRec['DV'] == UnitRec['DV'][I]))[0].tolist()
    #     for I, Id in enumerate(UnitRec['UnitId'])
    # ]

    # MergeList = np.unique(MergeList).reshape(np.unique(MergeList).shape[0], 1).tolist()

    MergeList = []
    for R in range(0,TotalNo,UnitNo*RecNo):
        MergeList += np.reshape(range(R, RecNo*UnitNo+R), (RecNo, UnitNo)).T.tolist()

    ## ==========


    Merge = {}

    for K in ['UnitId', 'Freq', 'dB', 'StimType', 'DV']:
        if K in UnitRec.keys():
            Merge[K] = np.zeros(TotalNo//RecNo, UnitRec[K].dtype)

    for K in ['PSTH', 'Raster', 'Spks', 'FiringRate']:
        if K in UnitRec.keys():
            Merge[K] = [[] for _ in range(TotalNo//RecNo)]

    for K in ['PSTHX', 'RasterX']:
        if K in UnitRec.keys():
            Merge[K] = np.zeros((UnitRec[K].shape[0], TotalNo//RecNo), UnitRec[K].dtype)


    for L,List in enumerate(MergeList):
        for K in ['UnitId', 'Freq', 'dB', 'StimType', 'DV']:
            if K in UnitRec.keys():
                Merge[K][L] = UnitRec[K][List[0]]

        for K in ['PSTHX', 'RasterX']:
            if K in UnitRec.keys():
                Merge[K][:,L] = UnitRec[K][:,List[0]]

        for K in ['PSTH', 'Raster']:
            if K in UnitRec.keys():
                Key = [
                    IO.Bin.Read(UnitRec[K][_])[0] for _ in List
                ] if 'str' in str(type(UnitRec[K][0])) else [
                    UnitRec[K][_] for _ in List
                ]

                Merge[K][L] = np.concatenate(Key, axis=1)

        for K in ['Spks', 'FiringRate']:
            if K in UnitRec.keys():
                Key = [
                    IO.Bin.Read(UnitRec[K][_])[0] for _ in List
                ] if 'str' in str(type(UnitRec[K][0])) else [
                    UnitRec[K][_] for _ in List
                ]

                Merge[K][L] = np.concatenate([Key for _ in List])


    if Save:
        AnalysisPrefix = '/'.join(UnitsFile.split('/')[:-2]) + '/Units/'+ UnitsFile.split('/')[-3]
        Exp = UnitsFile.split('/')[-1][:-4]
        AnalysisPrefix += '_' + Exp + '_AllUnits'

        for K,Key in Merge.items():
            if K in ['ISI', 'PSTH', 'Raster', 'Spks', 'FiringRate']:
                for El,Val in enumerate(Key):
                    IO.Bin.Write(Val, AnalysisPrefix+'/'+K+'/'+K+'_'+str(El)+'.dat')
            else:
                IO.Bin.Write(Merge[K], AnalysisPrefix+'/'+K)

    if Return: return(Merge)


def PSTH(Spks, TTLs, Rate, PSTHX, Offset=0):
    PSTHY = np.array([])
    for TTL in TTLs:
        Firing = ((Spks-Offset)*1000/Rate) - (TTL*1000/Rate)
        Firing = Firing[(Firing >= PSTHX[0]) * (Firing < PSTHX[-1])]

        PSTHY = np.concatenate((PSTHY, Firing)); del(Firing)

    PSTHY, PSTHX = np.histogram(PSTHY, PSTHX)
    return(PSTHX, PSTHY)


def PSTHLine(Spks, TTLs, PSTHX, Offset=0, Output='all'):
    """ Output: 'all', 'mean', 'norm'"""

    PSTHY = np.zeros((len(PSTHX)-1, len(TTLs)), dtype='int32')
    for T, TTL in enumerate(TTLs):
        Firing = (Spks - Offset - TTL)
        Firing = Firing[(Firing >= PSTHX[0]) * (Firing < PSTHX[-1])]

        PSTHY[:,T] = np.histogram(Firing, PSTHX)[0]; del(Firing)

    BinSize = PSTHX[1] - PSTHX[0]
    if Output.lower() == 'all': return(PSTHY)
    elif Output.lower() == 'mean': return(PSTHY.mean(axis=1))
    elif Output.lower() == 'norm': return(PSTHY.sum(axis=1)/(len(TTLs)*BinSize))
    else: print('Output should be "all", "mean" or "norm".'); return(None)


def Raster(Spks, TTLs, Rate, RasterX, Offset=0):
    RasterY = np.zeros((len(RasterX)-1, len(TTLs)), dtype='float32')

    for T, TTL in enumerate(TTLs):
        Firing = ((Spks-Offset)*1000/Rate) - (TTL*1000/Rate)
        Firing = Firing[(Firing >= RasterX[0]) * (Firing < RasterX[-1])]

        RasterY[:,T] = np.histogram(Firing, RasterX)[0]; del(Firing)

    RasterY[RasterY == 0] = np.nan

    return(RasterY)


def SpkResp(PSTHY, PSTHX):
    """
        This function returns the difference between the RMS of values after
        zero (PSTHX>0) and before zero (PSTHX<0). The returned value is a
        'baseline-corrected' event count.
    """
    # BLRMS = np.zeros(PSTHY.shape)
    # BLRMS[:,:] = PSTHY[:,:]
    # BLRMS = BLRMS.sum(axis=1)

    # BL = PSTHY[PSTHX[:-1]<0,:].sum()
    # BLRMS[BLRMS>BL] = BL

    # SpkResp = ((sum(PSTHY.sum(axis=1)[PSTHX[:-1]>0]) * 2)**0.5) - \
    #           ((sum(BLRMS[PSTHX[:-1]>0]) * 2)**0.5)

    RespRMS = PSTHY.mean(axis=1)[PSTHX[:-1]>0]
    # RespRMS = PSTHY.mean(axis=1)[PSTHX[:-1]>-10]
    RespRMS = ((RespRMS**2).mean())**0.5

    BLRMS = PSTHY.mean(axis=1)[PSTHX[:-1]<0]
    # BLRMS = PSTHY.mean(axis=1)[PSTHX[:-1]<-30]
    BLRMS = ((BLRMS**2).mean())**0.5

    SpkRespRMS = RespRMS - BLRMS
    return(SpkRespRMS)


def UnitRecLoad(Folder):
    UnitFiles = [_ for _ in glob(Folder+'/*') if '.dat' in _ and 'Info' not in _]
    Keys = [_.split('/')[-1].split('.')[0] for _ in UnitFiles]
    UnitRec = {Key: IO.Bin.Read(UnitFiles[K])[0] for K, Key in enumerate(Keys)}

    UnitFiles = {
        K: [_ for _ in glob(Folder+'/'+K+'/*') if 'Info' not in _]
        for K in ['PSTH', 'Raster', 'Spks', 'FiringRate']
    }

    UnitFiles = {
        K: np.array(sorted(V, key=lambda x: int(x.split('_')[-1].split('.')[0])))
        for K,V in UnitFiles.items()
    }

    UnitRec = {**UnitRec, **UnitFiles}
    return(UnitRec)


## Level 1
def GetAllUnits(ClustersPath, TimeWindow, ISISize=0.01, TTLCh=None, BinSize=None, AnalogTTLs=True, Save=True, Return=True, **Kws):
    AnalysisPath = '_'.join(ClustersPath.split('_')[:-1])+'_AllUnits'
    SpkClusters = IO.Bin.Read(ClustersPath+'/SpkClusters.dat')[0]
    SpkRecs = IO.Bin.Read(ClustersPath+'/SpkRecs.dat')[0]
    SpkTimes = IO.Bin.Read(ClustersPath+'/SpkTimes.dat')[0]
    Waveforms = IO.Bin.Read(ClustersPath+'/Waveforms.dat')[0]

    Info = IO.Txt.Read(ClustersPath+'/Info.dict')
    Rate = Info['Analysis']['Rate']
    Channels = Info['Analysis']['Channels']
    ChNo = len(Channels)
    ChNoTotal = Info['Analysis']['ChNoTotal']
    Offsets = Info['Analysis']['RecOffsets']
    ClusterLabels = Info['Analysis']['ClusterLabels']
    if Info['Analysis']['RecNoMatch']: ClusterRecs = Info['Analysis']['ClusterRecs']
    Good = [Id for Id,Key in ClusterLabels.items() if Key == 'good' or 'temp_' in Key]

    if not Good:
        print('No good units in this file :(')
        return(None)

    RecLengths = (np.array(Info['Analysis']['RecLengths'])//Rate).astype('int16')

    #== Verify noise units
    # RealGood = Good[:]
    # Good = [[Id,Key] for Id,Key in Clusters.cluster_groups.items() if Id not in RealGood]
    # GoodK = [_[1] for _ in Good]
    # Good = [_[0] for _ in Good]
    #==

    if not BinSize: BinSize = 1000/Rate
    PSTHX = np.arange(TimeWindow[0], TimeWindow[1], BinSize)
    RasterX = np.arange(PSTHX[0], PSTHX[-1], 1000/Rate)

    UnitRec = {}
    for K in ['UnitId', 'DV']: UnitRec[K] = np.zeros((len(Good)*len(ClusterRecs)), dtype=np.int16)
    for K in ['dB', 'Amp']: UnitRec[K] = np.zeros((len(Good)*len(ClusterRecs)), dtype=np.float32)
    for K in ['Freq', 'StimType']: UnitRec[K] = ['0' for _ in range(len(Good)*len(ClusterRecs))]

    UnitRec['PSTHX'] = np.zeros((len(PSTHX),len(Good)*len(ClusterRecs)), dtype=np.float32)
    UnitRec['RasterX'] = np.zeros((len(RasterX),len(Good)*len(ClusterRecs)), dtype=np.float32)

    if not TTLCh: TTLCh = Info['DAqs']['TTLCh']

    for K,V in Info['ExpInfo'].items():
        if 'Hz' not in V.keys():
            Info['ExpInfo'][K]['Hz'] = 'Baseline'

    if 'ChSpacing' not in Info['Analysis'].keys():
        Info['Analysis']['ChSpacing'] = 50

    Recs = [np.array(_) for _ in Info['Analysis']['RecsNested']]

    if 'Prevention/20170803-Prevention_04-UnitRec' in ClustersPath:
        Recs += [np.array([5])]
        Info['Analysis']['RawData'] = Info['Analysis']['RawData'][:-1] + [Info['Analysis']['RawData'][3]] + [Info['Analysis']['RawData'][-1]]
        Info['ExpInfo']['05'] = Info['ExpInfo']['04']

    Valid = np.ones((len(Good)*len(ClusterRecs)), dtype='bool')

    for rec, Rec in enumerate(ClusterRecs):
        # if rec < 59: continue
        RawRecExp = [Rec in _ for _ in Recs].index(True)
        RawRecdB = str(Recs[RawRecExp].tolist().index(Rec))
        RawRec = Info['Analysis']['RawData'][RawRecExp]
        RawRecExp = "{0:02d}".format(RawRecExp)

        RecTTLs = True
        if Info['ExpInfo'][RawRecExp]['Hz'] == 'Baseline':
            print('Baseline recordings have no TTLs.')
            RecTTLs = False

        if Info['Analysis']['RecNoMatch'] and RecTTLs:
            DataFile = Info['Analysis']['RawData'][rec]

            if 'home/Data/Malfatti' in DataFile or 'home/cerebro/Malfatti' in DataFile:
                DataFile = os.environ['ANALYSISPATH'] + '/' + '/'.join(DataFile.split('/')[5:])

            TTLFile = '/'.join(ClustersPath.split('/')[:-2])
            TTLFile += '/TTLs/' + DataFile.split('/')[-1].split('.')[0]
            if '_Rec' in TTLFile:
                TTLFile += '_TTLs.dat'
            else:
                TTLFile += '_Rec' + "{0:02d}".format(rec)+'_TTLs.dat'

            print(ClustersPath.split('/')[-1], 'rec', rec)
            print('Loading TTLs... ')
            if not glob(TTLFile):
                TTLs = IO.DataLoader(RawRec, Unit='int16', Recording=RawRecdB)[0]
                if type(TTLs) == dict:
                    _, Proc = IO.OpenEphys.GetChNoAndProcs(RawRec+'/settings.xml')
                    TTLs = TTLs[Proc]['0'][RawRecdB]
                elif type(TTLs) == np.memmap:
                    TTLs = TTLs.reshape((TTLs.shape[0]//ChNoTotal, ChNoTotal))

                print('Quantifying... ')
                TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, TTLs[:,TTLCh-1], 1)
                if type(TTLs) == tuple: TTLs = TTLs[0]
                if type(TTLs) != np.ndarray: TTLs = np.array(TTLs)
                print('Saving TTLs to', TTLFile, '...')
                IO.Bin.Write(TTLs, TTLFile)
            else:
                TTLs = IO.Bin.Read(TTLFile)[0]
            print('Done.')

        for I, Id in enumerate(Good):
            Ind = I + (len(Good)*rec)

            # Find the unit in this rec
            SpksId = (SpkClusters == Id) & (SpkRecs == Rec)
            if not True in SpksId:
                Valid[Ind] = False
                continue

            UnitTimes = SpkTimes[SpksId]

            # PSTH
            if Info['Analysis']['RecNoMatch'] and RecTTLs:
                UnitPSTH = PSTHLine(UnitTimes, TTLs, Rate, PSTHX, Offsets[rec])
                UnitRaster = Raster(UnitTimes, TTLs, Rate, RasterX, Offsets[rec])
            else:
                UnitPSTH, UnitRaster = np.zeros((PSTHX.shape[0], 1)), np.zeros((RasterX.shape[0], 1))*np.nan

            # Waveforms
            Spks = Waveforms[SpksId]

            # Firing rate
            UnitFiringRate = FiringRate(UnitTimes/Rate, RecLengths[rec], Offsets[rec]/Rate)

            # ISI
            UnitISI = ISI(UnitTimes/Rate, ISISize, Rate)

            # Unit info
            BestCh = GetBestCh(Spks)
            ChSpacing = Info['Analysis']['ChSpacing']
            DV = Info['ExpInfo'][RawRecExp]['DV']
            if not DV: DV = (Channels[-1]+1)*ChSpacing
            DV = int(DV) - ((ChNo-BestCh+1) * ChSpacing)

            if Info['ExpInfo'][RawRecExp]['Hz'] != 'Baseline':
                dB = Info['Audio']['Intensities'][int(RawRecdB)]
                Freq = Info['ExpInfo'][RawRecExp]['Hz']
                StimType = Info['ExpInfo'][RawRecExp]['StimType']
                if type(StimType) == list: StimType = '_'.join(StimType)
            else:
                dB, Freq, StimType = 0, '', ''

            Amp = Spks.mean(axis=0)[:,BestCh]
            while Amp.argmax() < Amp.argmin(): Amp[Amp.argmax()] = Amp.mean()
            Amp = Amp.max() - Amp.min()

            UnitRec['UnitId'][Ind] = Id
            UnitRec['DV'][Ind] = DV
            UnitRec['Freq'][Ind] = Freq
            UnitRec['dB'][Ind] = dB
            UnitRec['Amp'][Ind] = Amp
            UnitRec['StimType'][Ind] = StimType
            UnitRec['PSTHX'][:,Ind] = PSTHX
            UnitRec['RasterX'][:,Ind] = RasterX

            Keys = {'ISI':UnitISI, 'PSTH':UnitPSTH, 'Raster':UnitRaster, 'Spks':Spks, 'FiringRate':UnitFiringRate}
            for K,V in Keys.items():
                IO.Bin.Write(V, AnalysisPath+'/'+K+'/'+K+'_'+str(Ind)+'.dat')

            del(Spks, UnitPSTH, UnitRaster, UnitISI, UnitFiringRate, Keys)

            # UnitInfo = '_'.join(['Unit'+"{0:04d}".format(Id), StimType,
            #                      str(DV)+'DV', Freq, dB])

            # FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
            # Plot.WF_Raster_PSTH(Spks, Raster, RasterX, PSTH, PSTHX, RMSs, SpksToPlot, Rate, FigFile, Ext, Save, Show)

    # Cleaning
    # ValidIds = UnitRec['UnitId'] != 0

    for Key in ['Freq', 'StimType']: UnitRec[Key] = np.array(UnitRec[Key])

    for Key in ['UnitId', 'DV', 'dB', 'Freq', 'StimType']:
        UnitRec[Key] = UnitRec[Key][Valid]

    for Key in ['PSTHX', 'RasterX']:
        UnitRec[Key] = UnitRec[Key][:,Valid]

    if Save:
        if UnitRec['UnitId'].size:
            IO.Bin.Write(UnitRec, AnalysisPath)

    if Return:
        return(UnitRec)
    else:
        del(UnitRec)
        return(None)


def SpkRespPVal(PSTHY, PSTHX, N=None):
    """
        Implemented as described in Parras et al., 2017.

        This function generates a sample of N histograms with the same size
        of PSTH containing random values in a poisson distribution, with lambda
        equal to the PSTH baseline firing rate (mean of values when PSTHX<0).
        Then, it corrects the spike count after stimulus using the mean of
        values before stimulus for both the original and simulated PSTHYograms.
        Finally, it calculates the p-value as p = (g+1)/(N+1), where g is
        the number of simulated PSTHYograms with spike count >= than the
        original spike count. Therefore, the returned p-value represents the
        probability of the cell firing NOT be affected by stimulation.
    """
    if not N: N = PSTHY.shape[1]
    BL = PSTHY.mean(axis=1)[PSTHX[:-1]<0].mean()
    SimPSTH = [np.random.poisson(BL, (PSTHY.shape[0],1)) for _ in range(N)]
    SimPSTH = [SpkResp(_, PSTHX) for _ in SimPSTH]
    SpikeCount = SpkResp(PSTHY, PSTHX)

    # abs() is used because cells can also stop firing in response to stimulation :)
    g = len([_ for _ in SimPSTH if abs(_) >= abs(SpikeCount)])
    p = (g+1)/(N+1)

    return(p)


## Level 2
def GetCellsResponse(UnitRec, AnalysisFile='', Save=False, Return=True):
    CellsResponse = {}
    for K in ['SpkResp', 'SpkCount']:
        CellsResponse[K] = np.zeros(len(UnitRec['PSTH']), dtype=np.float32)

    for U in range(len(UnitRec['PSTH'])):
        # print(f"Processing unit {UnitRec['UnitId'][U]}...")
        PSTH = UnitRec['PSTH'][U]
        if 'str' in str(type(PSTH)):
            PSTH = IO.Bin.Read(PSTH)[0]

        TrialNo = PSTH.shape[1]
        if PSTH.sum() < TrialNo*0.03:
            # if too few spikes in PSTH
            CellsResponse['SpkResp'][U] = 1
            CellsResponse['SpkCount'][U] = 0
        else:
            CellsResponse['SpkResp'][U] = SpkRespPVal(PSTH,
                                                      UnitRec['PSTHX'][:,U],
                                                      N=TrialNo)
            CellsResponse['SpkCount'][U] = SpkResp(PSTH,
                                                       UnitRec['PSTHX'][:,U])

    if Save: IO.Bin.Write(CellsResponse, AnalysisFile)

    if Return:
        return(CellsResponse)
    else:
        del(CellsResponse)
        return(None)


def GetUnitsParameters(UnitRec, CellsResponse, AnalysisFile, Save=True, Return=True):
    UnitsId = np.unique(UnitRec['UnitId'])
    Stims = np.unique(UnitRec['StimType'])
    Intensities = np.unique(UnitRec['dB'])
    Freqs = sorted(np.unique(UnitRec['Freq'][UnitRec['Freq'] != '']), key=lambda x: int(x.split('-')[0]))
    Freqs = np.array(Freqs)

    Cells = {
        'Freqs': Freqs,
        'Intensities': Intensities,
        'UnitId': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['UnitId'].dtype),
        'StimType': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['StimType'].dtype),
        'RespMax': np.zeros((Stims.size * UnitsId.size), dtype=CellsResponse['SpkResp'].dtype),
        'FreqMax': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['Freq'].dtype),
        'FreqBest': np.zeros((Intensities.size, Stims.size * UnitsId.size), dtype=UnitRec['Freq'].dtype),
        'FreqSharpness': np.zeros((Intensities.size, Stims.size * UnitsId.size), dtype='float32'),
        'dBMax': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'dBBest': np.zeros((Freqs.size, Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'dBSharpness': np.zeros((Freqs.size, Stims.size * UnitsId.size), dtype='float32'),
        # 'dBLowest': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'FR_HzdBStim': np.zeros((Intensities.size, Freqs.size, Stims.size * UnitsId.size), dtype='float32')
    }

    Invalid = []

    for U,Unit in enumerate(UnitsId):
        for S,Stim in enumerate(Stims):
            UInd = S + (len(Stims)*U)

            print('Unit', U, 'Stim', Stim)
            FreqdB = np.zeros((len(Intensities),len(Freqs)), dtype='float32')

            for I,Intensity in enumerate(Intensities):
                for F,Freq in enumerate(Freqs):
                    Ind = (
                        UnitRec['UnitId'] == Unit) * (
                        UnitRec['dB'] == Intensity) * (
                        UnitRec['Freq'] == Freq) * (
                        UnitRec['StimType'] == Stim
                    )

                    if not True in Ind:
                        FreqdB[I,F] = 0
                        continue

                    while UnitRec['FiringRate'][Ind].shape[0] > 1:
                        Ind[np.where((UnitRec['FiringRate'] == UnitRec['FiringRate'][Ind][1]))[0]] = False

                    FR = IO.Bin.Read(UnitRec['FiringRate'][Ind][0])[0]
                    FreqdB[I,F] = FR.mean()

            # Peak and sharpness
            FRPerFreqPerdB = Analysis.Normalize(FreqdB.T)
            FreqSharpness, FreqBest = FRPerFreqPerdB.mean(axis=0), Freqs[FRPerFreqPerdB.argmax(axis=0)]

            FRPerdBPerFreq = Analysis.Normalize(FreqdB)
            dBSharpness, dBBest = FRPerdBPerFreq.mean(axis=0), Intensities[FRPerdBPerFreq.argmax(axis=0)]

            RespMax = FreqdB.max()
            FreqMax = np.where((FreqdB == RespMax))
            # dBMin = FreqdB[:,FreqMax[1][0]].min()
            # dBMin =
            dBMax, FreqMax = Intensities[FreqMax[0][0]], Freqs[FreqMax[1][0]]

            Cells['UnitId'][UInd] = Unit
            Cells['StimType'][UInd] = Stim
            Cells['RespMax'][UInd] = RespMax
            Cells['FreqMax'][UInd] = FreqMax
            Cells['FreqBest'][:,UInd] = FreqBest
            Cells['FreqSharpness'][:,UInd] = FreqSharpness
            Cells['dBMax'][UInd] = dBMax
            Cells['dBBest'][:,UInd] = dBBest
            Cells['dBSharpness'][:,UInd] = dBSharpness
            Cells['FR_HzdBStim'][:,:,UInd] = FreqdB
            # Cells['dBLowest'][UInd] = dBMin

    ## Cleaning
    if Invalid:
        Invalid = [Cells['UnitId'] == I for I in Invalid]
        Invalid = np.sum(Invalid, axis=0, dtype=bool)
        ValidIds = (Cells['UnitId'] != 0) * ~Invalid
    else:
        ValidIds = (Cells['UnitId'] != 0)

    for Key in ['UnitId', 'StimType', 'RespMax', 'FreqMax', 'dBMax']:#, 'dBLowest']:
        Cells[Key] = Cells[Key][ValidIds]

    for Key in ['FreqBest', 'FreqSharpness', 'dBBest', 'dBSharpness']:
        Cells[Key] = Cells[Key][:,ValidIds]

    Cells['FR_HzdBStim'] = Cells['FR_HzdBStim'][:,:,ValidIds]

    if Save: IO.Bin.Write(Cells, AnalysisFile)

    if Return:
        return(Cells)
    else:
        del(Cells)
        return(None)


def FRFreqSharp(CellsParameters, dB):
    Intensity = CellsParameters['Intensities'] == dB
    UnitsId = np.unique(CellsParameters['UnitId'])

    FR_Stim, FreqSh_Stim, FreqBest_Stim = {}, {}, {}
    for Unit in UnitsId:
        ThisUnit = CellsParameters['UnitId'] == Unit
        Stims = CellsParameters['StimType'][ThisUnit]
        if 'Sound_NaCl' in Stims:
            FreqStim = 'Sound_NaCl'
        elif 'Sound' in Stims:
            FreqStim = 'Sound'
        else:
            FreqStim = Stims[0] if len(Stims[0]) else Stims[1]

        Freq = CellsParameters['FreqBest'][Intensity,ThisUnit*(CellsParameters['StimType']==FreqStim)]

        Sharpness = [
            np.nanmean(CellsParameters['dBSharpness'][
                :,
                ThisUnit*(CellsParameters['StimType']==Stim)
            ])
            for S,Stim in enumerate(Stims)
        ]

        FreqBest = [
            CellsParameters['FreqBest'][
                Intensity,
                ThisUnit*(CellsParameters['StimType']==Stim)
            ][0]
            for S,Stim in enumerate(Stims)
        ]

        FreqBest = [sum([int(_) for _ in F.split('-')])//2000 for F in FreqBest]

        FR = [
            CellsParameters['FR_HzdBStim'][
                Intensity,
                (CellsParameters['Freqs']==Freq),
                ThisUnit*(CellsParameters['StimType']==Stim)
            ][0]
            for S,Stim in enumerate(Stims)
        ]

        for S,Stim in enumerate(Stims):
            if Stim not in FR_Stim.keys():
                FR_Stim[Stim], FreqSh_Stim[Stim], FreqBest_Stim[Stim] = [], [], []

            FR_Stim[Stim].append(FR[S])
            FreqSh_Stim[Stim].append(Sharpness[S])
            FreqBest_Stim[Stim].append(FreqBest[S])


    FR = np.array([FR_Stim[FreqStim], FR_Stim['Sound_CNO']]).T
    Sharpness = np.array([FreqSh_Stim[FreqStim], FreqSh_Stim['Sound_CNO']]).T
    FreqBest = np.array([FreqBest_Stim[FreqStim], FreqBest_Stim['Sound_CNO']]).T

    return(FR, Sharpness, FreqBest)


## Level 3
def GetCellsChanges(Cells, Stims, StimRef, AnalysisFile, Save=True, Return=True):
    CellsChanges = {}

    for Stim in Stims:
        Ind = (Cells['StimType'] == Stim)
        CellsChanges[Stim] = Cells['MaxResp'][Ind]
        CellsChanges[Stim+'-Freqs'] = Cells['BestFreq'][Ind]
        CellsChanges[Stim+'-dBs'] = Cells['BestdB'][Ind]

    StimPairs = list(combinations(Stims,2))

    for Pair in StimPairs:
        if StimRef not in Pair: continue
        if Pair[-1] != StimRef: Pair = (Pair[1], Pair[0])

        Key = 'Vs'.join(Pair)
        ChangedFreq = CellsChanges[Pair[0]+'-Freqs'] != CellsChanges[Pair[1]+'-Freqs']
        ChangeddB = CellsChanges[Pair[0]+'-dBs'] != CellsChanges[Pair[1]+'-dBs']

        CellsChanges[Key] = ((CellsChanges[Pair[0]]/CellsChanges[Pair[1]])-1)*100
        CellsChanges[Key+'-FreqChangePerc'] = len(CellsChanges[Key][ChangedFreq])*100/len(CellsChanges[Key])
        CellsChanges[Key+'-dBChangePerc'] = len(CellsChanges[Key][ChangeddB])*100/len(CellsChanges[Key])

    if Save: IO.Bin.Write(CellsChanges, AnalysisFile)

    if Return:
        return(CellsChanges)
    else:
        del(CellsChanges)
        return(None)


