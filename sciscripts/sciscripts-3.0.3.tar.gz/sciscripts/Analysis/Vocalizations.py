#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20200919
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Heavily based on code written by D. Laplagne.
"""

import numpy as np
from scipy import io
from copy import deepcopy

from sciscripts.IO import Bin, Mat, Wav
from sciscripts.Analysis import Analysis

from sciscripts.Analysis.Plot import Plot
plt = Plot.Return('plt')

#%%

def USVDetect(File, NoiseSonicMean, NoiseSonicSTD, M, N, Setup='', TimeWindow=2e-3, TimeStep=2.5e-4, BandwidthRes=1000, Overlap=0.2, FFTPad=0, UltrasonicLimit=18000, HRelax=6.75, DurThr=0.003):

    Audio, Rate = Wav.Read(File)
    ChNo = Audio.shape[1]

    WindowSize = round(Rate*TimeWindow)
    WindowStep = round(Rate*TimeStep)
    NFFT = Analysis.GetNFFT(WindowSize, FFTPad)
    Fxx, Txx, Sxx =  Analysis.Spectrogram(Audio, Rate, WindowSize, Overlap, NFFT)

    SxxRate = 1/(Txx[1]-Txx[0])
    SxxHigh = Sxx[Fxx>=UltrasonicLimit,:,:] # ultrasonic spectrogram (entropy detection is based on only this range of frequencies)
    SxxLow = Sxx[Fxx<UltrasonicLimit,:,:] # sonic spectrogram
    PxxSum = SxxHigh.sum(axis=0)
    PxxNorm = SxxHigh/np.tile(PxxSum, (1,Fxx.shape[0]))
    SxxHigh = -(PxxNorm*np.log2(PxxNorm)).sum(axis=0)

    # Threshold the entropy
    HRelaxed = np.ones((1,chNum))*HRelax
    HRelaxed = S.H <= np.tile(HRelaxed, (SxxHigh.shape[0],1))

    # Sonic noise
    NoiseSonic = SxxLow.mean(axis=0)
    NoiseSonic = (NoiseSonic-np.tile(NoiseSonicMean,(NoiseSonic.shape[0],1))/np.tile(NoiseSonicSTD,(NoiseSonic.shape[0],1)))
    HNoiseSonic = NoiseSonic - M*SxxHigh - N
    HNoiseSonicLow = HNoiseSonic < 0

    # Detect USVs combining channels
    idx = np.arange(Txx.shape[0])
    SxxWindowSize = round(WindowSize/2 * S_Fs)
    Window = np.ones((1,2*SxxWindowSize))
    HRelaxedCh = np.zeros((Txx.shape[0],ChNo))
    USVs = {
        'StartsLow': np.zeros((HNoiseSonicLow.shape[0], ChNo), dtype=bool),
        'StartsRel': np.zeros((HRelaxed.shape[0], ChNo), dtype=bool),
        'EndsLow': np.zeros((HNoiseSonicLow.shape[0], ChNo), dtype=bool),
        'EndsRel': np.zeros((HRelaxed.shape[0], ChNo), dtype=bool),
        'Starts': np.zeros(ChNo, dtype=bool),
        'Ends': np.zeros(ChNo, dtype=bool),
    }

    for Ch in range(ChNo):
        USVs['StartsLow'][:,Ch]  = np.where(np.diff(np.array([np.zeros(HNoiseSonicLow.shape[0]), HNoiseSonicLow[:,Ch]]), axis=0) == 1)[0]
        USVs['EndsLow'][:,Ch]  = np.where(np.diff(np.array([np.zeros(HNoiseSonicLow.shape[0]), HNoiseSonicLow[:,Ch]]), axis=0) == -1)[0]

        HRelaxed[-1,Ch]   = 0                                         # force the relaxed entropy region to end when the clip ends
        USVs['StartsRel'][:,Ch]  = np.where(np.diff(np.array([np.zeros(HRelaxed.shape[0]), HRelaxed[:,Ch]]), axis=0) == 1)[0]
        USVs['EndsRel'][:,Ch]  = np.where(np.diff(np.array([np.zeros(HRelaxed.shape[0]), HRelaxed[:,Ch]]), axis=0) == -1)[0]
        USVs['StartsLow'][:,Ch]  = USVs['StartsLow'][:,Ch][:USVs['EndsLow'][:,Ch].shape[0]]                        # if the last USV does not end just skip it
        USVs['StartsRel'][:,Ch]  = USVs['StartsRel'][:,Ch][:USVs['EndsRel'][:,Ch].shape[0]]

        for u in range(USVs['StartsLow'].shape[0]):
            USVs['Starts'][u,Ch]  = USVs['StartsRel'][np.where((USVs['StartsRel'][u,Ch] <= USVs['StartsLow'][u,Ch]))[0][-1],Ch]  # find the corresponding start in the relaxed vector
            USVs['Ends'][u,Ch]    = USVs['EndsRel'][np.where((USVs['EndsRel'][u,Ch] >= USVs['EndsLow'][u,Ch]))[0][0],Ch] # find the corresponding end in the relaxed vector
            if Txx[USVs['Ends'][u,Ch]] - Txx[USVs['Starts'][u,Ch]] > DurThr:                       # only include events longer than the duration of each spectrum in the spectrogram (minimum time slice)
                HRelaxedCh[:,Ch] = HRelaxedCh[:,Ch] | ((idx >= USVs['Starts'][u,Ch]) & (idx <= USVs['Ends'][u,Ch]))   # add this region to the relaxed vector for this channel

    HRelaxedAll = logical(sum(HRelaxedCh,2))  # combine all channels

    # Join times with low entropy within a time window
    HNoiseSonicLowWindow   = np.convolve(HRelaxedAll.astype('float32'), Window, 'same') >= 1
    USVs['Starts']  = np.where(np.diff(np.array([np.zeros(HNoiseSonicLowWindow.shape[0]), HNoiseSonicLowWindow])) == 1)
    USVs['Ends']    = np.where(np.diff(np.concatenate(([0], HNoiseSonicLowWindow))) == -1)[0]
    USVs['Starts']  = USVs['Starts'][Txx(USVs['Starts']) < max(Txx)-up.overlap,:]     # only analyze the USVs that start before the overlap time
    USVs['Ends']    = USVs['Ends'][Txx(USVs['Ends']) < max(Txx)-up.overlap,:]         # only analyze the USVs that start before the overlap time
    USVs['Starts']  = USVs['Starts'][:USVs['Ends'].shape[0],:]                        # if the last USV does not end just skip it

    USV         = []     # a cell here keeps the format compatible with that of Detect_USVs_indep
    USVclip     = []
    USVsgram    = []

#     # Extract the USVs
#     for u = 1:length(USVs['Starts'])
#         # Pick the mic with strongest signal
#         thisValid           = HRelaxedCh(USVs['Starts'](u):USVs['Ends'](u),:)     # logical
#         thisH               = S.H(USVs['Starts'](u):USVs['Ends'](u),:)           # entropy
#         thisH(~thisValid)   = nan
#         Hweighted           = nanmean(thisH,1)./sum(thisValid,1)     # both low H values and number of valid timepoints helps you
#         [~, mic]            = min(Hweighted)
#         USV(u).mic          = mic
#
#         # Extract the USV on that channel
#         newstart            = max(1,USVs['Starts'](u) + find(thisValid(:,mic),1,'first')-1 - wndSize)
#         newend              = min(length(Txx),USVs['Starts'](u) + find(thisValid(:,mic),1,'last')-1 + wndSize)
#         USV(u).time         = Txx(newstart) + time_onset + up.wnd/2           ##ok<*AGROW> % starting time (without the leading silence)
#         USV(u).dur          = Txx(newend) - Txx(newstart) - up.wnd    # USV duration
#         USV(u).H            = S.H(newstart:newend,mic)
#         USV(u).lowH         = HRelaxedCh(newstart:newend,mic)
#         USV(u).sonicNoise   = mean(SxxN(newstart:newend,mic))
#         USV(u).q            = ' '  # since we now check sonic noise and duration here, all are valid by those criteria
#
#         sound_from          = round(Txx(newstart) * Fs)
#         sound_to            = round(Txx(newend) * Fs)
#         USVclip(u).sound    = sound_clip(sound_from:sound_to,mic)   # sound clip
#
#         USVsgram(u).S = Sxx(newstart:newend,:,mic)
#         USVsgram(u).t = Txx(newstart:newend) + time_onset
#     end
#
#     USV         = {USV}
#     USVclip     = {USVclip}
#     USVsgram    = {USVsgram}




def USVSort(File, VocsSplitHz=30000):
#     Vocs = Bin.Read(File)[0]
#     Rate = Vocs['Rate']
    Vocs = Mat.Read(File)
    Rate = Vocs['USVinfo']['soundFs']

    if type(Vocs['USVclip'][0]) == list:
        Vocs['USVclip'] = Vocs['USVclip'][0]
        Vocs['USV'] = Vocs['USV'][0]

    VocsSorted = {'22kHz': [], '50kHz': [], 'Skipped': []}
    for S,Stage in enumerate(Vocs['USVclip']):
        V, Voc = S, Stage

        if Vocs['USV'][V]['q'] == 'd':
            VocsSorted['Skipped'].append(V)
            print('Skipped No', V); continue

        F, Pxx = Analysis.PSD(Voc['sound'], Rate)
        PxxSp = Pxx[:]; Pxx[F<12000] = 0
        Thr = Pxx.mean() + (3*Pxx.std())

        print('Voc No', str(V)+', peak at', str(F[Pxx.argmax()]/1000)+'kHz')
        if Pxx.max() > Thr:
            if F[Pxx.argmax()] > VocsSplitHz: VocsSorted['50kHz'].append(V)
            else: VocsSorted['22kHz'].append(V)
        else:
            ShowVoc = True
            SF, ST, Sxx = Spectrogram(Voc, Rate, 10000)

            while ShowVoc:
                Fig, Axes = plt.subplots(2, 1)
                Axes[0].plot(F, PxxSp, lw=2); Axes[0].plot([F[0], F[-1]], [Thr, Thr], lw=2)
                Plot.Spectrogram(Axes[1], ST, SF, Sxx, HighFreqThr=100000)
                plt.show()

                Ans = None
                while Ans not in range(5):
                    print('0) 22kHz')
                    print('1) 50kHz')
                    print('2) Show voc.', V, 'again')
                    print('3) Skip voc.', V)
                    print('4) Stop sorting')
                    Ans = input(': '); Ans = int(Ans)

                ShowVoc = False
                if Ans == 0: VocsSorted['22kHz'].append(V)
                elif Ans == 1: VocsSorted['50kHz'].append(V)
                elif Ans == 2: ShowVoc = True
                elif Ans == 3: VocsSorted['Skipped'].append(V)
                elif Ans == 4: Break = True

    return(VocsSorted)


# def USVSortedWrite(FileName, Vocs, VocsSorted):
#     with h5py.File(FileName) as F:
#         for S, Setup in Vocs.items():
#             Path = '/Vocs/'+S
#             if Path not in F: F.create_group(Path)
#
#             for C, Class in Setup.items():
#                 F['Vocs'][S][C] = Class
#
#         for S, Setup in VocsSorted.items():
#             for G, Group in Setup.items():
#                 for P, Pair in Group.items():
#                     Path = '/VocsSorted/'+S+'/'+G+'/'+P
#                     if Path not in F: F.create_group(Path)
#
#                     for C, Class in Pair.items():
#                         F['VocsSorted'][S][G][P][C] = Class
#
#     return(None)


# def USVSortedRead(FileName):
#     with h5py.File(FileName, 'r') as F:
#         Vocs = {}
#         for S, Setup in F['Vocs'].items():
#             Vocs[S] = {}
#             for C, Class in Setup.items():
#                 Vocs[S][C] = Class[:]
#
#         VocsSorted = {}
#         for S, Setup in F['VocsSorted'].items():
#             VocsSorted[S] = {}
#             for G, Group in Setup.items():
#                 VocsSorted[S][G] = {}
#                 for P, Pair in Group.items():
#                     VocsSorted[S][G][P] = {}
#
#                     for C, Class in Pair.items():
#                         VocsSorted[S][G][P][C] = Class[:]
#
#     return(Vocs, VocsSorted)


def DictFixKeys(Dict, Copy=True):
    if Copy: DictCopy = deepcopy(Dict)
    else: DictCopy = Dict

    for K,Key in DictCopy.items():
        if type(Key) is dict: DictCopy[K] = DictFixKeys(Key)
        else:
            if K[0].isdigit():
                Kk = 'x'+K
                DictCopy[Kk] = Key
                del(DictCopy[K])

    return(DictCopy)


def DictUndoFixKeys(Dict, Copy=True):
    if Copy: DictCopy = deepcopy(Dict)
    else: DictCopy = Dict

    for K,Key in DictCopy.items():
        if type(Key) is dict: DictCopy[K] = DictUndoFixKeys(Key)
        else:
            if K[0] == 'x':
                Kk = K[1:]
                DictCopy[Kk] = Key
                del(DictCopy[K])

    return(DictCopy)


def RecursiveDict(Dict, Copy=True):
    if Copy: DictCopy = deepcopy(Dict)
    else: DictCopy = Dict

    for K,Key in DictCopy.items():
        if type(Key) is dict: DictCopy[K] = RecursiveDict(Key)
        elif type(Key) is list: pass#DictCopy[K] = np.array(Key, dtype='float32')
        elif type(Key) is np.ndarray: pass#DictCopy[K] = Key.tolist()

    return(DictCopy)


# def BoxPlots(Data, FigTitle, XLabel, YLabel, Names, FigName, LinesAmpF=2, Ext=['pdf', 'eps'], Save=True):
#     if type(Data) is not type(np.array([])): Data = np.array(Data).T

#     Fig, Ax = plt.subplots(1,1)
#     BoxPlot = Ax.boxplot(Data, showmeans=True)

#     for K in ['boxes', 'whiskers', 'caps', 'medians', 'fliers']:
#         for I in range(Data.shape[1]):
#             BoxPlot[K][I].set(color='k')
#             BoxPlot[K][I].set(color='k')

#     LineY = np.amax(Data) + ((np.amax(Data)-np.amin(Data))*0.1)

#     TPairs = list(combinations(range(Data.shape[1]), 2))
#     if FigName.split('-')[1] == 'ST': TPairs = [(0,1), (2,3)]
#     else: TPairs = [(0,3), (1,2)]

#     for TP in TPairs:
#         SS = Data[:, TP[0]]; DD = Data[:, TP[1]]
#         if np.mean(SS) > np.mean(DD): SS, DD = DD, SS

#         p = Stats.RTTest(SS, DD)
#         p = p['p.value']*len(TPairs)

#         if p < 0.05:
#             LineY = LineY+(TP[1]*LinesAmpF)
#             Plot.SignificanceBar([TP[0]+1, TP[1]+1], [LineY, LineY], str(p), Ax)

#     Plot.Set(AxesObj=Ax, Axes=True)
#     Ax.spines['left'].set_position(('outward', 5))
#     Ax.spines['bottom'].set_position(('outward', 5))
#     Ax.set_ylabel(YLabel); Ax.set_xlabel(XLabel)
#     Ax.set_xticks(list(range(1,Data.shape[1]+1))); Ax.set_xticklabels(Names)
#     Fig.suptitle(FigTitle)
#     if Save:
#         for Ex in Ext:
#             Fig.savefig(FigName+'.'+Ex, format=Ex)

#     return(Fig, Ax)


# def ScatterMean(Data, FigTitle, XLabel, YLabel, Names, FigName, LinesAmpF=2, Spread=0.2, Ext=['pdf', 'svg'], Save=True):
#     if type(Data) is not type(np.array([])): Data = np.array(Data).T

#     Fig, Ax = plt.subplots(1,1)

#     for P in range(Data.shape[1]):
#         X = np.random.uniform(P+1-Spread, P+1+Spread, len(Data[:,P]))
#         Error = [0, np.std(Data[:,P])/len(Data[:,P])**0.5, 0]

#         Ax.plot(X, Data[:,P], 'ko')
#         Ax.errorbar([P+1-Spread, P+1, P+1+Spread], [np.mean(Data[:,P])]*3, Error, lw=3, elinewidth=1, capsize=10, color='k')

#     Margin = ((np.amax(Data)-np.amin(Data))*0.1)
#     LineY = np.amax(Data) + Margin

# #    TPairs = list(combinations(range(Data.shape[1]), 2))
# #    if FigName.split('-')[1] == 'ST': TPairs = [(0,1), (2,3)]
# #    else: TPairs = [(0,3), (1,2)]
# #
# #    for TP in TPairs:
# #        SS = Data[:, TP[0]]; DD = Data[:, TP[1]]
# #        if np.mean(SS) > np.mean(DD): SS, DD = DD, SS
# #
# #        p = Stats.RTTest(SS, DD)
# #        p = p['p.value']*len(TPairs)
# #        print(FigTitle, TP, round(p, 3))
# #
# #        if p < 0.05:
# #            if p < 0.001: p = 'p < 0.001'
# #            else: p = 'p = ' + str(round(p, 3))
# #
# #            LineY = LineY+(TP[1]*LinesAmpF)
# #            Plot.SignificanceBar([TP[0]+1, TP[1]+1], [LineY, LineY], p, Ax)

#     Plot.Set(AxesObj=Ax, Axes=True)
#     Ax.set_ylim([-Margin, LineY + LineY*0.05]); Ax.set_xlim([0, Data.shape[1]+1])
#     Ax.spines['left'].set_position(('outward', 5))
#     Ax.spines['bottom'].set_position(('outward', 5))
#     Ax.set_ylabel(YLabel); Ax.set_xlabel(XLabel)
#     Ax.set_xticks(list(range(1,Data.shape[1]+1))); Ax.set_xticklabels(Names)
#     Fig.suptitle(FigTitle)
#     if Save:
#         for Ex in Ext:
#             Fig.savefig(FigName+'.'+Ex, format=Ex)


#     return(Fig, Ax)


# def ScatterMeanSorted(Data, FigTitle, XLabel, YLabel, Names, FigName, LinesAmpF=2, Spread=0.2, Ext=['pdf', 'svg'], Save=True):
#     Fig, Ax = plt.subplots(1,1)
#     Colors = ['m', 'y']; XTicks = []
#     for P in range(len(Data)):
#         I = [P*3+1, P*3+2]; XTicks.append(sum(I)/2)

#         for C in range(len(Data[P])):
#             X = np.random.uniform(I[C]-Spread, I[C]+Spread, len(Data[P][C]))
#             Error = [0, np.std(Data[P][C])/len(Data[P][C])**0.5, 0]

#             Ax.plot(X, Data[P][C], Colors[C]+'o')
#             Ax.errorbar([I[C]-Spread, I[C], I[C]+Spread], [np.mean(Data[P][C])]*3, Error, lw=3, elinewidth=1, capsize=10, color='k')

#     Margin = ((np.amax(Data)-np.amin(Data))*0.1)
#     LineY = np.amax(Data) + Margin

#     Plot.Set(AxesObj=Ax, Axes=True)
#     Ax.set_ylim([-Margin, LineY + LineY*0.05]); Ax.set_xlim([0, XTicks[-1]+1.5])
#     Ax.spines['left'].set_position(('outward', 5))
#     Ax.spines['bottom'].set_position(('outward', 5))
#     Ax.set_ylabel(YLabel); Ax.set_xlabel(XLabel)
#     Ax.set_xticks(XTicks); Ax.set_xticklabels(Names)
#     Ax.legend(['22kHz', '50kHz'], loc='best')

#     Fig.suptitle(FigTitle)
#     if Save:
#         for Ex in Ext:
#             Fig.savefig(FigName+'.'+Ex, format=Ex)


#     return(Fig, Ax)


# def STSameGender(Data, FigTitle, XLabel, YLabel, Names, FigName, LinesAmpF, Ext=['pdf', 'svg'], Save=True):
#     if type(Data) is not type(np.array([])): Data = np.array(Data).T

#     Fig, Ax = plt.subplots(1,1)

#     Margin = ((np.amax(Data)-np.amin(Data))*0.1)
#     LineY = np.amax(Data) + Margin
# #    TPairs = [(0,1), (2,3)]
# #
# #    for TP in TPairs:
# #        for G in range(Data.shape[0]):
# #            Ax.plot([TP[0]+1, TP[1]+1], [Data[G,TP[0]], Data[G,TP[1]]], 'ko-')
# #
# #        SS = Data[:, TP[0]]; DD = Data[:, TP[1]]
# #        if np.mean(SS) > np.mean(DD): SS, DD = DD, SS
# #
# #        p = Stats.RTTest(SS, DD)
# #        p = p['p.value']*len(TPairs)
# #        print(FigTitle, TP, round(p, 3))
# #
# #        if p < 0.05:
# #            if p < 0.001: p = 'p < 0.001'
# #            else: p = 'p = ' + str(round(p, 3))
# #
# #            LineY = LineY+(TP[1]*LinesAmpF)
# #            Plot.SignificanceBar([TP[0]+1, TP[1]+1], [LineY, LineY], p, Ax)

#     Plot.Set(AxesObj=Ax, Axes=True)
#     Ax.set_ylim([-Margin, LineY + LineY*0.05]); Ax.set_xlim([0, Data.shape[1]+1])
#     Ax.spines['left'].set_position(('outward', 5))
#     Ax.spines['bottom'].set_position(('outward', 5))
#     Ax.set_ylabel(YLabel); Ax.set_xlabel(XLabel)
#     Ax.set_xticks(list(range(1,Data.shape[1]+1))); Ax.set_xticklabels(Names)
#     Fig.suptitle(FigTitle)
#     if Save:
#         for Ex in Ext:
#             Fig.savefig(FigName+'.'+Ex, format=Ex)


#     return(Fig, Ax)
