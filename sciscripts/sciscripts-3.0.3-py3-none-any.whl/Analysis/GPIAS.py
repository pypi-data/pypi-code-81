#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from scipy import signal

from sciscripts.Analysis import Analysis as sAnalysis
from sciscripts.IO import IO#, Asdf#, Hdf5


## Level 0
def CheckGPIASRecs(Data, SizeLimits, Plot=False):
    ToCheck = [Rec for Rec in Data.keys()
                   if len(Data[Rec])<min(SizeLimits)
                   or len(Data[Rec])>max(SizeLimits)]

    if ToCheck:
        if Plot:
            Params = {'backend': 'TkAgg'}
            from matplotlib import rcParams; rcParams.update(Params)
            import matplotlib.pyplot as plt

            for Rec in ToCheck:
                print('Showing Rec', Rec+', size', Data[Rec].shape[0])
                plt.plot(Data[Rec])
                plt.show()

        return(ToCheck)
    else:
        print('All recs within expected size.')
        return(None)


def ConvertIndexesToArray(Indexes):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Index':[]}
    for E, Exp in Indexes.items():
        for A, Animal in Exp.items():
            for Freq, Index in Animal.items():
                Array['Exps'].append(E)
                Array['Animals'].append(A)
                Array['Freqs'].append(Freq)
                Array['Index'].append(Index)

    for K in Array.keys(): Array[K] = np.array(Array[K])
    return(Array)


def ConvertTracesToArray(Traces):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Traces':[], 'ColOrder':[]}
    ColOrder = ['NoGap', 'Gap']
    for E, Exp in Traces.items():
        for A, Animal in Exp.items():
            for Freq, Trace in Animal.items():
                Array['Exps'].append(E)
                Array['Animals'].append(A)
                Array['Freqs'].append(Freq)
                Array['ColOrder'].append(ColOrder)

                ATrace = np.zeros((Trace['Gap'].shape[0],2), Trace['Gap'].dtype)
                for i in range(2):
                    Trace[ColOrder[i]] = Trace[ColOrder[i]].reshape(Trace[ColOrder[i]].shape[0])
                    ATrace[:,i] = Trace[ColOrder[i]]

                Array['Traces'].append(ATrace)

    for K in [_ for _ in Array.keys() if _ != 'Traces']: Array[K] = np.array(Array[K])
    return(Array)


def GetExpsIndexesDict(Exps, ExpNames=None):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the last tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE = {}, {}
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(File)[0]
            # if 'XValues' in GPIASRec:
            #     GPIASRec['X'] = GPIASRec.pop('XValues')
            #     Asdf.Write(GPIASRec, File)

            GPIASRec, X = GPIASRec['GPIAS'], GPIASRec['X']
            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            # Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal],
            #                                  **{K: np.abs(V['GPIASIndex'])
            #                                     for K, V in GPIASRec['Index'].items()}}

            Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal],
                                             **{K: sAnalysis.GetNegEquiv(V['GPIASIndex'])
                                                for K, V in GPIASRec['Index'].items()}}
            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetExpsIndexesDictBest(Exps, ExpNames=None):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the best tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE = {}, {}
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(File)[0]
            # if 'XValues' in GPIASRec:
            #     GPIASRec['X'] = GPIASRec.pop('XValues')
            #     Asdf.Write(GPIASRec, File)

            GPIASRec, X = GPIASRec['GPIAS'], GPIASRec['X']
            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            # Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal],
            #                                  **{K: np.abs(V['GPIASIndex'])
            #                                     for K, V in GPIASRec['Index'].items()}}

            Dict = {K: sAnalysis.GetNegEquiv(V['GPIASIndex']) for K, V in GPIASRec['Index'].items()}
            for K in Dict:
                if K in Indexes_IFAE[E][Animal]:
                    if Dict[K] < Indexes_IFAE[E][Animal][K]:
                        print(Indexes_IFAE[E][Animal][K], Dict[K])
                        Indexes_IFAE[E][Animal][K] = Dict[K]
                else:
                    Indexes_IFAE[E][Animal][K] = Dict[K]

            # Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal], **Dict}

            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetMAF(Indexes_IFAE, Animals, ExpOrder):
    MAF = []
    for Animal in Animals:
        ## Indexes_IFAE as array
        ThisAnimal = Indexes_IFAE['Animals'] == Animal

        Freqs = [
            Indexes_IFAE['Freqs'][ThisAnimal*(Indexes_IFAE['Exps'] == Exp)]
            for Exp in ExpOrder[:2]
        ]

        FreqsI = np.array([
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs[0]
        ]).ravel()

        Freqs[0] = np.array(Freqs[0])[FreqsI > 30].tolist()
        Freqs = sorted(
            np.intersect1d(Freqs[0], Freqs[1]),
            key=lambda x: int(x.split('-')[-1])
        )

        ExpFIDiff = [
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[1])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            - abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs
        ]



        ## Indexes_IFAE as dict
        # FreqsB = sorted(Indexes_IFAE[ExpOrder[0]][Animal].keys(),
        #                 key=lambda x: [int(y) for y in x.split('-')])
        # FreqsA = sorted(Indexes_IFAE[ExpOrder[1]][Animal].keys(),
        #                 key=lambda x: [int(y) for y in x.split('-')])

        # Freqs = [F for F in set(FreqsB).intersection(FreqsA)]
        #           # if abs(Indexes_IFAE[ExpOrder[1]][Animal][F]) - abs(Indexes_IFAE[ExpOrder[0]][Animal][F]) < -10]

        # ExpFIDiff = [abs(Indexes_IFAE[ExpOrder[1]][Animal][Freq]) -
        #           abs(Indexes_IFAE[ExpOrder[0]][Animal][Freq]) for Freq in set(FreqsB).intersection(FreqsA)]

        ## Debug
        # print(Animal)
        # print('Before', Indexes_IFAE[ExpOrder[0]][Animal])
        # print('After', Indexes_IFAE[ExpOrder[1]][Animal])
        # print(ExpFIDiff)
        # print('')

        if not ExpFIDiff: MAF.append(None)
        else: MAF.append(Freqs[ExpFIDiff.index(min(ExpFIDiff))])

    return(MAF)


def GetMAFIndexes(Indexes_IFAE, MAF, Animals, ExpOrder):
    Indexes = [
        np.array(
            [Indexes_IFAE['Index'][
                (Indexes_IFAE['Exps'] == Exp) *
                (Indexes_IFAE['Animals'] == Animal) *
                (Indexes_IFAE['Freqs'] == MAF[A])
             ] for A, Animal in enumerate(Animals) if MAF[A]
            ]
        ).ravel() for E, Exp in enumerate(ExpOrder)
    ]


    # Indexes = [[Indexes_IFAE[Exp][Animal][MAF[A]]
    #             for A, Animal in enumerate(Animals) if MAF[A]]
    #            for E, Exp in enumerate(ExpOrder)]

    # Override to account for inverted responses
    # Indexes = [[sAnalysis.GetNegEquiv(_) for _ in Exp] for Exp in Indexes]
    # Indexes = [[_ if _ > 0 else -_ for _ in Exp] for Exp in Indexes]
    # Indexes = [[_ if _ < 100 else _-100 for _ in Exp] for Exp in Indexes]
    # Indexes = [[_ if _ < 100 else 100 for _ in Exp] for Exp in Indexes]

    return(Indexes)


def IndexCalcOld(Data, Keys, PulseSampleStart, SliceSize):
    Index = {}
    for Key in Keys:
        BGStart = 0; BGEnd = SliceSize
        PulseStart = PulseSampleStart; PulseEnd = PulseSampleStart + SliceSize

        if type(Data[Key[0]]) == list:
            if not Data[Key[0]]:
                print('Key', Key[0], 'is empty. Skipping...')
                continue

        ResRMSBG = (np.mean(Data[Key[0]][BGStart:BGEnd]**2))**0.5
        ResRMSPulse = (np.mean(Data[Key[0]][PulseStart:PulseEnd]**2))**0.5
#            ResRMS = ResRMSPulse
        if ResRMSPulse < ResRMSBG: ResRMS = ResRMSPulse
        else: ResRMS = ResRMSPulse - ResRMSBG

        RefRMSBG = (np.mean(Data[Key[1]][BGStart:BGEnd]**2))**0.5
        RefRMSPulse = (np.mean(Data[Key[1]][PulseStart:PulseEnd]**2))**0.5
#            RefRMS = RefRMSPulse
        if RefRMSPulse < RefRMSBG: RefRMS = RefRMSPulse
        else: RefRMS = RefRMSPulse - RefRMSBG

        # GPIAS index (How much Res is different from Ref)
        Index[Key[2]] = (RefRMS-ResRMS)/RefRMS

    return(Index)


def IndexCalc(Data, Keys, PulseSampleStart, SliceSize, BGNormalize=True):
    Index = {}
    for Key in Keys:
        PulseStart = PulseSampleStart; PulseEnd = PulseSampleStart + SliceSize

        if type(Data[Key[0]]) == list:
            if not Data[Key[0]]:
                print('Key', Key[0], 'is empty. Skipping...')
                continue

        ResRMSPulse = (np.mean(Data[Key[0]][PulseStart:PulseEnd]**2))**0.5
        RefRMSPulse = (np.mean(Data[Key[1]][PulseStart:PulseEnd]**2))**0.5

        if BGNormalize:
            BGStart = PulseSampleStart-SliceSize; BGEnd = PulseSampleStart
            ResRMSBG = (np.mean(Data[Key[0]][BGStart:BGEnd]**2))**0.5
            RefRMSBG = (np.mean(Data[Key[1]][BGStart:BGEnd]**2))**0.5

            ResRMS = abs(ResRMSPulse-ResRMSBG)
            RefRMS = abs(RefRMSPulse-RefRMSBG)

        else:
            RefRMS = RefRMSPulse
            ResRMS = ResRMSPulse

        Index[Key[2]] = ((ResRMS/RefRMS)-1)*100

    return(Index)


def PreallocateDict(Freqs):#, PrePostFreq=None):
    Dict = {
        Key: {'-'.join([str(Freq[0]), str(Freq[1])]): {} for Freq in Freqs}
        for Key in ['Trace', 'Index', 'IndexTrace']
    }

    # if PrePostFreq:
    #     for Key in ['Trace', 'Index', 'IndexTrace']:
    #         Dict[Key][PrePostFreq]['Pre'] = []
    #         Dict[Key][PrePostFreq]['Post'] = []

    for Freq in Dict['Trace'].keys():
        Dict['Trace'][Freq]['NoGap'] = []; Dict['Trace'][Freq]['Gap'] = []
        Dict['IndexTrace'][Freq]['NoGap'] = []; Dict['IndexTrace'][Freq]['Gap'] = []

    return(Dict)


def OrganizeRecs(Dict, Data, Rate, DataInfo, AnalogTTLs, TimeWindow, Proc=None, Events=None,
                 FilterFreq=[70, 400], FilterOrder=4, FilterType='', Filter='butter'):

    Recs = sorted(Data.keys(), key=lambda i: int(i))

    for R, Rec in Data.items():
        print('Slicing and filtering Rec ', R, '...')
        Freq = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][0];
        Trial = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][1];

        SFreq = ''.join([str(DataInfo['Audio']['NoiseFrequency'][Freq][0]), '-',
                         str(DataInfo['Audio']['NoiseFrequency'][Freq][1])])

        if Trial == -1: STrial = 'Pre'
        elif Trial == -2: STrial = 'Post'
        elif Trial % 2 == 0: STrial = 'NoGap'
        else: STrial = 'Gap'

        if AnalogTTLs:
            TTLs = sAnalysis.QuantifyTTLsPerRec(AnalogTTLs, Rec[:,DataInfo['DAqs']['TTLCh']-1])
            if len(TTLs) > 1:
                print('More than one TTL detected!!')
                # TTLs = [Rec[:,DataInfo['DAqs']['TTLCh']-1].argmax()]
                TTLs = [TTLs[0]]
            print(TTLs)

            if not TTLs: print('No TTL detected. Skipping trial...'); continue

        else:
            TTLs = sAnalysis.QuantifyTTLsPerRec(AnalogTTLs, EventsDict=Events,
                                      TTLCh=DataInfo['DAqs']['TTLCh'], Proc=Proc, Rec=R)

        if not FilterType:
            if len(FilterFreq) == 1: FilterType = 'lowpass'
            else: FilterType = 'bandpass'

        if len(DataInfo['DAqs']['RecCh']) == 1:
            GD = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][0]-1],
                                           Rate, FilterFreq, FilterOrder, Filter, FilterType)
            # GD = Rec[:,DataInfo['DAqs']['RecCh'][0]-1]

            GD -= GD.mean()
            GD = sAnalysis.SliceData(GD, TTLs, -int(TimeWindow[0]*Rate),
                                     int(TimeWindow[1]*Rate), AnalogTTLs)

        elif len(DataInfo['DAqs']['RecCh']) == 3:
            ## Testing
            # X = Rec[:,DataInfo['DAqs']['RecCh'][0]-1]
            # Y = Rec[:,DataInfo['DAqs']['RecCh'][1]-1]
            # Z = Rec[:,DataInfo['DAqs']['RecCh'][2]-1]

            # GD = [
            #     np.abs(X-X.mean()),
            #     np.abs(Y-Y.mean()),
            #     np.abs(Z-Z.mean())]
            # GD = [sAnalysis.SliceData(
            #     _, TTLs, -int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate),
            #     AnalogTTLs) for _ in GD]

            X = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][0]-1],
                                          Rate, FilterFreq, FilterOrder, Filter, FilterType)
            Y = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][1]-1],
                                          Rate, FilterFreq, FilterOrder, Filter, FilterType)
            Z = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][2]-1],
                                          Rate, FilterFreq, FilterOrder, Filter, FilterType)

            GD = np.mean([
                np.abs(X-X.mean()),
                np.abs(Y-Y.mean()),
                np.abs(Z-Z.mean())], axis=0)

            # GD = np.mean([
            #     -(X-X.mean()),
            #     Y-Y.mean(),
            #     Z-Z.mean()], axis=0)

            GD -= GD.mean()

            GD = sAnalysis.SliceData(
                GD, TTLs, -int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate),
            )


        Dict['IndexTrace'][SFreq][STrial].append(GD)
        Dict['Trace'][SFreq][STrial].append(GD)

    return(Dict)


## Level 1
def GetAllTrials(
        Data, DataInfo, Rate, TimeWindow=[-0.1, 0.15], FilterFreq=[70, 400],
        FilterOrder=3, FilterType='', Filter='butter', AnalogTTLs=True
    ):

    if not DataInfo:
        # Override for old .mat recordings
        if not FilterType:
            if len(FilterFreq) == 1: FilterType = 'lowpass'
            else: FilterType = 'bandpass'

        # PrePostFreq = None

        GPIASData = Data.copy()
        for Key in ['IndexTrace', 'Trace']:
            for F,Freq in GPIASData[Key].items():
                for G,Gap in Freq.items():
                    for T,Trial in enumerate(Gap):
                        if Filter:
                            GD = sAnalysis.FilterSignal(Trial, Rate, FilterFreq, FilterOrder, Filter, FilterType)
                        else:
                            GD = Trial.copy()

                        GD -= GD.mean()
                        GD = sAnalysis.SliceData(GD, GPIASData['TTLs'], -int(TimeWindow[0]*Rate),
                                                 int(TimeWindow[1]*Rate), AnalogTTLs)

                        print(Key, F, G, T)
                        GPIASData[Key][F][G][T] = GD.copy()

        del(GD)

    else:
        # PrePostFreq = DataInfo['ExpInfo']['FreqOrder'][0][0]
        # PrePostFreq = '-'.join([str(DataInfo['Audio']['NoiseFrequency'][PrePostFreq][0]),
        #                         str(DataInfo['Audio']['NoiseFrequency'][PrePostFreq][1])])

        # if '0' not in Data:
        #     Data = {str(int(K)-1): V for K,V in Data.items()}

        GPIASData = PreallocateDict(DataInfo['Audio']['NoiseFrequency'])#, PrePostFreq)
        GPIASData = OrganizeRecs(GPIASData, Data, Rate, DataInfo, AnalogTTLs,
                                       TimeWindow, None, None,
                                       FilterFreq, FilterOrder, FilterType, Filter)

    return(GPIASData)#, PrePostFreq)


## Level 2
def Analysis(Data, DataInfo, Rate, AnalysisFolder, AnalysisKey,
             TimeWindow=[-0.1, 0.15],
             FilterFreq=[70, 400], FilterOrder=3, FilterType='', Filter='butter',
             SliceSize=100, AnalogTTLs=True, Return=False, Save=True):

    GPIASData = GetAllTrials(
        Data, DataInfo, Rate, TimeWindow, FilterFreq,
        FilterOrder, FilterType, Filter, AnalogTTLs
    )

    SliceSize = int(SliceSize * (Rate/1000))

    for Freq in GPIASData['IndexTrace'].keys():
        for Key in GPIASData['IndexTrace'][Freq].keys():
            # Average trials for traces
            GPIASData['Trace'][Freq][Key] = np.mean(GPIASData['Trace'][Freq][Key], axis=0)
            if GPIASData['Trace'][Freq][Key].shape == ():
                print('Freq', Freq, 'trial', Key, 'is empty. Skipping...')
                continue

            for Tr in range(len(GPIASData['IndexTrace'][Freq][Key])):
                GPIASData['IndexTrace'][Freq][Key][Tr] = abs(
                        signal.hilbert(GPIASData['IndexTrace'][Freq][Key][Tr])
                )

            GPIASData['IndexTrace'][Freq][Key] = np.nanmean(GPIASData['IndexTrace'][Freq][Key], axis=0)

        # RMS
        Keys = [['Gap', 'NoGap', 'GPIASIndex']]

        GPIASData['Index'][Freq] = IndexCalc(
                                       GPIASData['IndexTrace'][Freq], Keys,
                                       -int(TimeWindow[0]*Rate), SliceSize, False)

    X = np.arange(int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate))*1000/Rate

    if Save:
        # Asdf.Write({'GPIAS': GPIASData, 'X': X}, AnalysisFolder+'/'+AnalysisKey+'.asdf')
        IO.Bin.Write({'GPIAS': GPIASData, 'X': X}, AnalysisFolder+'/'+AnalysisKey)

    if Return: return(GPIASData, X)
    else: return(None)

