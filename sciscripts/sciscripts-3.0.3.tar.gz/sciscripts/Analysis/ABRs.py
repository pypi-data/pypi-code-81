#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2017
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.ABRs] Importing dependencies...')
import numpy as np
import os

from copy import deepcopy
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Plot import Plot
from sciscripts.IO import IO
print('[Analysis.ABRs] Done.')

## Level 0
def ABRPerCh(Data, Rate, TTLs, ABRCh, TimeWindow, FilterFreq, FilterOrder=4, FilterCoeff='butter', Filter='bandpass'):
    Len = abs(int((Rate*TimeWindow[0])-(Rate*TimeWindow[1])))
    ABRs = np.zeros((Len, len(ABRCh)), dtype=Data.dtype)
    for C,Ch in enumerate(ABRCh):
        ABR = Analysis.FilterSignal(Data[:,Ch-1], Rate, FilterFreq, FilterOrder, FilterCoeff, Filter)
        ABR = Analysis.SliceData(ABR, TTLs,
                                     -int(TimeWindow[0]*Rate),
                                     int(TimeWindow[1]*Rate),
                                     )
        ABR *= 1000 # to µV
        ABRs[:,C] = ABR.mean(axis=1)
        del(ABR)

    return(ABRs)


def LatencyToPeaks(ABRs, X=[], RefKey=None, Std=1):
    Rev = False if '0' in ABRs else True
    Recs = sorted(ABRs.keys(), reverse=Rev)

    if len(Recs) == 1:
        print('You need at least 2 recordings in ABRs dict to compare latencies.')
        return(None)

    if not RefKey: RefKey = Recs[0]
    BestCh = Analysis.GetStrongestCh(ABRs[RefKey])

    if len(X):
        FixedThreshold = ABRs[RefKey][:,BestCh].std()*Std
        Peaks = [Analysis.GetPeaks(ABRs[Rec][:,BestCh], FixedThreshold=FixedThreshold) for Rec in Recs]
    else:
        FixedThreshold = ABRs[RefKey][:,BestCh].std()*Std
        # Peaks = [Analysis.GetPeaks(ABRs[Rec][:,BestCh], FixedThreshold=FixedThreshold) for Rec in Recs]
        # Peaks = [Analysis.GetPeaks(ABRs[Rec][:,BestCh], Std=Std) for Rec in Recs]

    Peaks = [_['Pos'] for _ in Peaks]
    if len(X): Peaks = [P[X[P] > 0] for P in Peaks]

    if not len(Peaks[0]):
        AllPeaks = np.ones((len(Recs),1), dtype=int)*-1
        return(AllPeaks)

    AllPeaks = []; ToRemove = []
    for R, Rec in enumerate(Recs):
        if R == 0: AllPeaks.append(Peaks[R].tolist()); continue
        if not len(Peaks[R]):
            ToRemove.append((R,0))
            AllPeaks.append([AllPeaks[0][-1]])
            continue

        PeakNo = min([len(Peaks[R]), len(Peaks[0])])
        RecPeaks = []
        for P in range(1,PeakNo):
            if np.where((Peaks[0][P] >= Peaks[R][P-1]) *
                        (Peaks[R][P-1] >= Peaks[0][P-1]-3))[0].size:
                RecPeaks.append(Peaks[R][P-1])
            else:
                ToRemove.append((R,P-1))
                try: RecPeaks.append(AllPeaks[0][P-1])
                except IndexError: RecPeaks.append(AllPeaks[0][-1])

        # If no peaks in previous intensity, try the one before
        LocalRef = 0
        LocalLen = 0
        while not LocalLen:
            LocalRef -= 1
            LocalLen = len(AllPeaks[LocalRef])

        if np.where((AllPeaks[LocalRef][-1] < Peaks[R]))[0].size:
            Last = Peaks[R][AllPeaks[LocalRef][-1] < Peaks[R]][0]

            if Last not in RecPeaks:
                # print('Before:', RecPeaks)
                Ind = np.where((AllPeaks[0] <= Last))[0][0]

                IntermedNo = (Ind)-len(RecPeaks)
                if IntermedNo > 0:
                    for _ in range(IntermedNo): ToRemove.append((R,len(RecPeaks)+_))

                    Intermed = [AllPeaks[0][len(RecPeaks)+_] for _ in range(IntermedNo)]
                    RecPeaks += Intermed + [Last]

                else: RecPeaks += [Last]

        AllPeaks.append(RecPeaks)

    for R in ToRemove: AllPeaks[R[0]][R[1]] = -1

    MaxLen = max([len(_) for _ in AllPeaks])
    AllPeaks = [_ + [-1]*(MaxLen-len(_)) for _ in AllPeaks]

    AllPeaks = np.array(AllPeaks)
    for P in range(AllPeaks.shape[1]):
        Ind = np.where((AllPeaks[:,P]==max(AllPeaks[:,P])))[0][-1]+1
        AllPeaks[Ind:,P] = -1

    return(AllPeaks)


## Level 1
def GetThreshold(ABRs, X, Std=1):
    Peaks = LatencyToPeaks(ABRs, X, Std=Std)
    if Peaks is None or Peaks.mean() == -1:
        return(0)

    Threshold = max([np.where((Peaks[:,_] == max(Peaks[:,_])))[0][-1]
                     for _ in range(Peaks.shape[1])])
    return(Threshold)


def LatencyPerFreq(Files, Freqs, Std=1):
    Latencies = {}
    for F,File in enumerate(Files):
        ABRs = IO.Bin.Read(File)[0]
        X = '/'.join(File.split('/')[:-1])+'/X.dat'
        X = IO.Bin.Read(X)[0]

        Latencies[Freqs[F]] = LatencyToPeaks(ABRs, X, Std=Std)

        Thrs = [np.where((Latencies[Freqs[F]][:,_] == max(Latencies[Freqs[F]][:,_])))[0][-1] for _ in range(Latencies[Freqs[F]].shape[1])]
        Ind = np.where((Thrs == max(Thrs)))[0][0]
        Latencies[Freqs[F]] = Latencies[Freqs[F]][:,Ind].astype('float32')

        Latencies[Freqs[F]][Latencies[Freqs[F]] == -1] = float('NaN')

        Latencies[Freqs[F]] /= int(round(1/(X[1] - X[0])))

    return(Latencies)


def Single(Data, Rate, ABRCh, TTLCh, TimeWindow, FilterFreq, FilterOrder=4, Filter='bandpass', Save='', ReturnX=True, Return=True):
    if ReturnX:
        X = np.arange(int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate))*1000/Rate

    if type(TTLCh) == int:
        TTLs = Analysis.QuantifyTTLsPerRec(True, Data[:,TTLCh-1])
    else:
        TTLs = TTLCh

    if len(TTLs) and TTLs[0] != 'Broken':
        ABRs = ABRPerCh(Data, Rate, TTLs, ABRCh, TimeWindow, FilterFreq, FilterOrder, FilterCoeff='butter', Filter=Filter)
    else:
        print('No TTLs in this recording.')
        return(None)

    if Save:
        if ReturnX:
            IO.Bin.Write(X, '/'.join(Save.split('/')[:-2])+'/X.dat')

        IO.Bin.Write(ABRs, Save)

    if Return:
        if ReturnX: return(ABRs, X)
        else: return(ABRs)
    else:
        if ReturnX: del(ABRs, X)
        else: del(ABRs)
        return(None)


## Level 2
def Multiple(Data, Rate, ABRCh, TTLCh, TimeWindow, FilterFreq, Recs='all', Intensities=[], Save='', Return=True):
    if Recs.lower() == 'all': Recs = sorted(Data.keys(), key=lambda x: int(x))

    ABRs = {}
    for R,Rec in enumerate(Recs):
        Rec_R = Rec if not len(Intensities) else Intensities[R]
        ABRCh_R = ABRCh if type(ABRCh[0]) != list else ABRCh[R]

        if Save:
            Save_R = Save+'/'+Rec if not len(Intensities) else Save+'/'+Intensities[R]
        else:
            Save_R = ''

        if type(TTLCh) == list:
            TTLCh_R = IO.Bin.Read(TTLCh[R])[0] if type(TTLCh[R]) == str else TTLCh[R]
        else:
            TTLCh_R = TTLCh

        ABRs[Rec_R] = Single(
            Data[Rec], Rate, ABRCh_R, TTLCh_R, TimeWindow, FilterFreq,
            Save=Save_R, ReturnX=False, Return=Return
        )

    X = np.arange(int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate))*1000/Rate

    if Save:
        IO.Bin.Write(X, '/'.join(Save.split('/')[:-1])+'/X.dat')

    if Return:
        return(ABRs, X)
    else:
        del(ABRs, X)
        return(None)


## Level 3
def GetThresholdsPerFreq(Folders, Std=1):
    Thresholds = {'Thresholds': [], 'Freqs':[]}

    for Folder in Folders:
        ABR = IO.Bin.Read(Folder+'/ABRs', Verbose=False)[0]
        Freqs = sorted(ABR.keys(), key=lambda i: int(i.split('-')[1]))

        for Freq in Freqs:
            Trial = 'Trial'+str(len(ABR[Freq])-2)
            Intensities = sorted(ABR[Freq][Trial], reverse=True, key=lambda x: int(x))
            Threshold = GetThreshold(ABR[Freq][Trial], ABR[Freq]['X'], Std=Std)
            Thresholds['Thresholds'].append(int(Intensities[Threshold]))
            Thresholds['Freqs'].append(Freq)

    Thresholds = {K: np.array(V) for K,V in Thresholds.items()}

    return(Thresholds)

def GetWaveAmpPerFreq(Folders, Std=1):
    WaveAmps = {'Amps': [], 'Freqs':[]}

    for Folder in Folders:
        ABR = IO.Bin.Read(Folder+'/ABRs', Verbose=False)[0]
        Freqs = sorted(ABR.keys(), key=lambda i: int(i.split('-')[1]))

        for Freq in Freqs:
            Trial = 'Trial'+str(len(ABR[Freq])-2)
            Intensities = sorted(ABR[Freq][Trial], reverse=True, key=lambda x: int(x))
            X = IO.Bin.Read(Folder+'/ABRs/'+Freq+'/X.dat', Verbose=False)[0]
            Peaks = LatencyToPeaks(ABR[Freq][Trial], X, Std=Std)
            if Peaks is None or Peaks.mean() == -1:
                WaveAmps['Amps'].append(np.zeros(5))
                WaveAmps['Freqs'].append(Freq)
                continue

            WaveAmp = ABR[Freq][Trial][Intensities[0]][Peaks[0,:],0]
            WaveAmps['Amps'].append(WaveAmp)
            WaveAmps['Freqs'].append(Freq)

    MaxLen = max([_.shape[0] for _ in WaveAmps['Amps']])
    for WA,WaveAmp in enumerate(WaveAmps['Amps']):
        if WaveAmp.shape[0] < MaxLen:
            WaveAmps['Amps'][WA] = np.hstack((WaveAmp, -np.ones(MaxLen-WaveAmp.shape[0])))

    WaveAmps = {K: np.array(V) for K,V in WaveAmps.items()}

    return(WaveAmps)


def Session(Folders, Freqs, Intensities, ABRCh, TTLCh, TimeWindow, FilterFreq, Proc='100', ChannelMap=None, AnalysisFolder=''):
    for F, Folder in enumerate(Folders):
        print(Folder.replace(os.environ['DATAPATH']+'/', '').replace(os.environ['HOME']+'/', ''))
        Data, Rate = IO.DataLoader(Folder, Unit='uV', ChannelMap=ChannelMap)
        if len(Data.keys()) == 1: Proc = list(Data.keys())[0]
        else: ChNo, Proc = IO.OpenEphys.GetChNoAndProcs(Folder+'/settings.xml')

        Data, Rate = Data[Proc]['0'], Rate[Proc]['0']
        print('')
        print([_.shape for _ in Data.values()])

        if not AnalysisFolder:
            AnalysisFolder = os.environ['ANALYSISPATH'] + '/' + Folder.split('/')[-3]

        XSavePath = '/'.join([AnalysisFolder, Folder.split('/')[-2], 'ABRs', Freqs[F]])
        if os.path.isdir(XSavePath): Trial = 'Trial'+str(len(glob(XSavePath)))
        else: Trial = 'Trial0'
        SavePath = '/'.join([XSavePath, Trial])

        TTLCh_F = TTLCh[F] if type(TTLCh) == list else TTLCh
        ABRCh_F = ABRCh[F] if type(ABRCh[0]) == list else ABRCh

        Multiple(Data, Rate, ABRCh_F, TTLCh_F, TimeWindow, FilterFreq, Recs='all', Intensities=Intensities, Save=SavePath, Return=False)

        del(Data)


## Helper functions
def WriteRecAndTTLCh(Folders):
    for Folder in Folders:
        print(Folder)
        Data, Rate = IO.DataLoader(Folder, Unit='uV', ChannelMap=[])
        if len(Data.keys()) == 1: Proc = list(Data.keys())[0]
        Data, Rate = Data[Proc]['0'], Rate[Proc]['0']

        InfoFile = glob(Folder+'/../*.dict')[0]

        for R, Rec in Data.items():
            print(R)
            Info = IO.Txt.Read(InfoFile)
            TTLs = []
            if Info['DAqs']['TTLCh'] <= Rec.shape[1]:
                TTLs = Analysis.QuantifyTTLsPerRec(True, Rec[:,Info['DAqs']['TTLCh']-1])

            if len(TTLs) < 100 or len(TTLs) > Info['Audio']['SoundPulseNo']+100:
                print('TTLs:', len(TTLs))
                while len(TTLs) < 100 or len(TTLs) > Info['Audio']['SoundPulseNo']+100:
                    Break = ''
                    Chs = [Rec[:int(Rate/2),Ch] for Ch in range(Rec.shape[1])]
                    Plot.RawCh(Chs, Lines=len(Chs), Cols=1, Save=False)

                    TTLCh = input('TTLCh: ')
                    RecCh = input('RecCh (space separated): ')
                    TTLCh = int(TTLCh)
                    RecCh = [int(_) for _ in RecCh.split(' ')]
                    Break = input('Break [y/N]? ')

                    if Break.lower() in ['y', 'yes']: break
                    TTLs = Analysis.QuantifyTTLsPerRec(True, Rec[:,TTLCh-1])
                print('TTLs:', len(TTLs))

                if Break.lower() not in ['y', 'yes']:
                    if RecCh != Info['DAqs']['RecCh']:
                        Info['DAqs']['RecCh'] = RecCh
                        IO.Txt.Write(Info, InfoFile)
                        IO.Bin.Write(Rec[:,RecCh], Folder+'/RecCh_'+R+'.dat')


                    Info['DAqs']['TTLCh'] = TTLCh
                    IO.Txt.Write(Info, InfoFile)
                    IO.Bin.Write(TTLs, Folder+'/TTLs_'+R+'.dat')

    return(None)


NoTTLsFile = os.environ['AnalysisPath']+'/Experiments/NoTTLRecs.dict'

def _PrintOptions():
    print('')
    print('This plot shows the first 0.5s of this recording.')
    print('What to do?')
    print('1) Decrease TTL Threshold')
    print('2) Change TTL channel')
    print('3) Decrease TTL Threshold and change TTL channel')
    print('4) Choose a startpoint for TTLs')
    print('5) Plot TTLCh and TTL threshold')
    print('6) Change ABR and TTL channels')
    print('7) Ignore PulseNo restritions')
    print('8) Report broken rec')
    print('9) Abort')
    print('')

    return(None)


def FixTTLs(Data, Rate, DataInfo, Freq, Rec, AnalogTTLs):
    NoTTLRecs = IO.Txt.Read(NoTTLsFile)
    F = DataInfo['InfoFile'].split('/')[-1].split('.')[0]
    TTLCh = DataInfo['DAqs']['TTLCh']
    DataCh = DataInfo['DAqs']['RecCh']


    WhatToDo = None; IgnoreRestritions = False
    if F in NoTTLRecs:
        if Freq in NoTTLRecs[F]:
            if Rec in NoTTLRecs[F][Freq]:
                WhatToDo = NoTTLRecs[F][Freq][Rec]['WhatToDo']
                Std = NoTTLRecs[F][Freq][Rec]['Std']
                SampleStart = NoTTLRecs[F][Freq][Rec]['SampleStart']

                if NoTTLRecs[F][Freq][Rec]['TTLCh']:
                    TTLCh = NoTTLRecs[F][Freq][Rec]['TTLCh']

                if NoTTLRecs[F][Freq][Rec]['DataCh']:
                    DataCh = NoTTLRecs[F][Freq][Rec]['DataCh']

                if WhatToDo == '6': ChangedDataCh = True


    NoChoice = False
    if not WhatToDo:
        NoChoice = True
        if 'Plot' not in locals():
            from Analysis.Plot import Plot
            plt = Plot.Return('plt')

        print('DataCh:', DataCh)
        print('TTLCh:', TTLCh)
        print('')
        _PrintOptions()

        Chs = Data[:int(Rate/2),:]

        if DataInfo['InfoFile'].split('/')[-1].split('-')[0] in ['20170623145925', '20170623162416']:
            Chs[:,-1] = Analysis.FilterSignal(Chs[:,-1], Rate, [8000, 14900])

        Fig, Axes = plt.subplots(1,2,figsize=(10,5), sharex=True)
        Axes[0] = Plot.AllCh(Chs, lw=0.6, Ax=Axes[0])
        Axes[1].plot(Analysis.GetInstFreq(Data[:int(Rate/2),TTLCh-1], Rate))
        plt.show()

        WhatToDo = input(': ')

        if F not in NoTTLRecs: NoTTLRecs[F] = {}
        if Freq not in NoTTLRecs[F]: NoTTLRecs[F][Freq] = {}
        if Rec not in NoTTLRecs[F][Freq]: NoTTLRecs[F][Freq][Rec] = {}

        NoTTLRecs[F][Freq][Rec]['WhatToDo'] = WhatToDo
        for K in ['SampleStart', 'Std', 'TTLCh', 'DataCh']:
            if K not in NoTTLRecs[F][Freq][Rec].keys():
                NoTTLRecs[F][Freq][Rec][K] = None

        Std = NoTTLRecs[F][Freq][Rec]['Std']
        SampleStart = NoTTLRecs[F][Freq][Rec]['SampleStart']
        ChangedDataCh = False


    if WhatToDo == '1':
        if not Std or NoChoice:
            Std = input('How many std above the mean should the threshold be? ')
            Std = float(Std)

        TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1], Std)

        NoTTLRecs[F][Freq][Rec]['Std'] = Std
        IO.Txt.Write(NoTTLRecs, NoTTLsFile)

    elif WhatToDo == '2':
        if not TTLCh or NoChoice:
            TTLCh = input('TTL channel: '); TTLCh = int(TTLCh)

        TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1])

        NoTTLRecs[F][Freq][Rec]['TTLCh'] = TTLCh

    elif WhatToDo == '3':
        if not Std or NoChoice:
            Std = input('How many std above the mean should the threshold be? ')
            Std = float(Std)

        if not TTLCh:
            TTLCh = input('TTL channel: '); TTLCh = int(TTLCh)
            TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1], Std)

        NoTTLRecs[F][Freq][Rec]['Std'] = Std
        NoTTLRecs[F][Freq][Rec]['TTLCh'] = TTLCh
        IO.Txt.Write(NoTTLRecs, NoTTLsFile)

    elif WhatToDo == '4':
        if not SampleStart:
            SampleStart = input('Sample of the rising edge of the 1st pulse: ')
            SampleStart = int(SampleStart)

        TTLs = Analysis.GenFakeTTLsRising(Rate, DataInfo['Audio']['SoundPulseDur'],
                                  DataInfo['Audio']['SoundPauseBeforePulseDur'],
                                  DataInfo['Audio']['SoundPauseAfterPulseDur'], SampleStart,
                                  DataInfo['Audio']['SoundPulseNo'])

        NoTTLRecs[F][Freq][Rec]['SampleStart'] = SampleStart

    elif WhatToDo == '5':
        Std = NoTTLRecs[F][Freq][Rec]['Std']

        Threshold = Analysis.GetTTLThreshold(Data[:,TTLCh-1], Std)
        Plot.TTLCh(Data[:,TTLCh-1], Std, Threshold)
        TTLs = []

    elif WhatToDo == '6':
        if not ChangedDataCh:
            NewABRCh = input('ABR channels (comma separated): ')
            NewABRCh = [int(_) for _ in NewABRCh.split(',')]
            TTLCh = input('TTL channel: '); TTLCh = int(TTLCh)

            TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1])

            NoTTLRecs[F][Freq][Rec]['DataCh'] = NewABRCh
            NoTTLRecs[F][Freq][Rec]['TTLCh'] = TTLCh

            Info = {'ABRCh': NewABRCh, 'TTLCh': TTLCh}
            print(len(TTLs), 'TTLs')
            print('ABR Channels changed. Restarting calculations...')
            print('')
        else:
            TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1])

    elif WhatToDo == '7':
        Std = NoTTLRecs[F][Freq][Rec]['Std']

        TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1], Std)
        IgnoreRestritions = True

    elif WhatToDo == '8':
        TTLs = []
        NoTTLRecs[F][Freq][Rec]['BrokenRec'] = True
        IO.Txt.Write(NoTTLRecs, NoTTLsFile)
        return('Broken')

    else:
        print('Aborted.')
        raise(SystemExit)


    if not IgnoreRestritions:
        if len(TTLs) > DataInfo['Audio']['SoundPulseNo']+4 or len(TTLs) < 100:
            TTLs = []

    if len(TTLs) == 0:
        NoTTLRecs[F][Freq][Rec]['WhatToDo'] = None
        IO.Txt.Write(NoTTLRecs, NoTTLsFile)
    else:
        IO.Txt.Write(NoTTLRecs, NoTTLsFile)
        if WhatToDo == '6'and not ChangedDataCh: return(Info)

    print(len(TTLs), 'TTLs after fix.')
    return(TTLs)


def GetTTLs(Data, Rate, DataInfo, DataFolder, AnalogTTLs=True, R=None, Freq=None):
    TTLCh = DataInfo['DAqs']['TTLCh']
    ABRCh = DataInfo['DAqs']['RecCh']

    if TTLCh > Data.shape[1]:
        print('TTLCh > ChNo; replaced by -1.')
        TTLCh = 0

    print('TTL mean and max:', np.mean(Data[:,TTLCh-1]), np.max(Data[:,TTLCh-1]))
    TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, Data[:,TTLCh-1])
    if len(TTLs) > DataInfo['Audio']['SoundPulseNo']+10 or len(TTLs) < 100:
        TTLs = []

    if max(ABRCh) > Data.shape[1]:
        print(''); print('Wrong ABR Channels!'); print('')

    TTLFile = glob(DataFolder+'/Rec_'+R+'_TTLs.TTLs')
    if len(TTLFile):
        TTLs = IO.Bin.Read(TTLFile[0])[0]

        if TTLs[0] == 'Broken':
            print('Exp', DataFolder.split('/')[-1], 'Rec', R, 'is broken.')
            return('Broken')

    if not len(TTLs):
        print('Fixing TTLs...')
        while len(TTLs) == 0:
            TTLs = FixTTLs(Data, Rate, DataInfo, Freq, R, AnalogTTLs)

        if type(TTLs) == dict:
            DI = deepcopy(DataInfo)
            DI['DAqs']['RecCh'] = TTLs['ABRCh']
            DI['DAqs']['TTLCh'] = TTLs['TTLCh']

            TTLs = []
            while len(TTLs) == 0:
                TTLs = FixTTLs(Data, Rate, DI, Freq, R, AnalogTTLs)

            Chs = [_-1 for _ in DI['DAqs']['RecCh']]

            IO.Bin.Write(Data[:,Chs], DataFolder+'/Rec_'+R+'_ABRs.ABRs')

        if type(TTLs) == str:
            if TTLs == 'Broken':
                print('Exp', DataFolder.split('/')[-1], 'Rec', R, 'is broken.')
                IO.Bin.Write(np.array(['Broken']), DataFolder+'/Rec_'+R+'_TTLs.TTLs')
                return(TTLs)

        if type(TTLs) == list: TTLs = np.array(TTLs)
        IO.Bin.Write(TTLs, DataFolder+'/Rec_'+R+'_TTLs.TTLs')
        print('Done')

    print(len(TTLs), 'TTLs')
    return(TTLs)


