#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180907
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from glob import glob

from sciscripts.Analysis.Plot import Units as UnitsPlot
from sciscripts.IO import IO


def Raster_Full(SpkClusters, UnitsId, SpkRecs, SpkSamples, Rate, Rec, Offset=0, PulseDur=None, TTLs=[],
                Ax=None, AxArgs={}, File='RasterFull', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = UnitsPlot.FigAx(Ax)

    if PulseDur and TTLs.size:
        for TTL in TTLs:
            Ax.axvspan(TTL/Rate, (TTL/Rate)+PulseDur,
                       color='k', alpha=0.3, lw=0)

    for I, Id in enumerate(UnitsId):
        Ids = np.where((SpkClusters == Id) & (SpkRecs == Rec))[0]
        Spks = (SpkSamples[Ids]-Offset)/Rate
        Ax.plot(Spks, np.ones(len(Spks))+I, 'ko')

    Result = UnitsPlot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def FreqCurve(AllCells, Stim, Ax=None, AxArgs={}, File='FreqAnddBCurve', Ext=['svg'], Save=False, Show=True):
    for E, Exp in enumerate(AllCells):
        Fig, Ax, ReturnAx = UnitsPlot.FigAx(Ax)

        IntFreq = np.zeros(Exp['Freqs'].shape, dtype=np.int16)
        for F, Freq in enumerate(Exp['Freqs']):
            IntFreq[F] = sum([float(_) for _ in Freq[F].split('-')])/2

        StimIndex = np.where((Exp['StimType'] == Stim))[0]
        for U in StimIndex:
            for f in range(Exp['HzdBCurve'].shape[1]):
                Ax.plot(Exp['HzdBCurve'][:,f,U], label=IntFreq[f], lw=2)

        Ax.legend()
        if 'xlabel' not in AxArgs: AxArgs['xlabel'] = 'Intensities [dB]'
        if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Baseline-corrected\nSpike count'
        if 'ylim' not in AxArgs: AxArgs['ylim'] = [min(Ax.get_yticks()), max(Ax.get_yticks())]
        AxArgs.update({'xticks': range(len(Exp['Intensities'])), 'xticklabels': Exp['Intensities']})

        Result = UnitsPlot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)

    return(Result)


def dBCurve(AllCells, Stim, Ax=None, AxArgs={}, File='FreqAnddBCurve', Ext=['svg'], Save=False, Show=True):
    for E, Exp in enumerate(AllCells):
        Fig, Ax, ReturnAx = UnitsPlot.FigAx(Ax)

        IntFreq = np.zeros(Exp['Freqs'].shape, dtype=np.int16)
        for F, Freq in enumerate(Exp['Freqs']):
            IntFreq[F] = sum([float(_) for _ in Freq[F].split('-')])/2

        StimIndex = np.where((Exp['StimType'] == Stim))[0]
        for U in StimIndex:
            for d in range(Exp['HzdBCurve'].shape[0]):
                Ax.plot(Exp['HzdBCurve'][d,:,U], label=Exp['Intensities'][d], lw=2)

        Ax.legend()
        if 'xlabel' not in AxArgs: AxArgs['xlabel'] = 'Frequencies [Hz]'
        if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Baseline-corrected\nSpike count'
        if 'ylim' not in AxArgs: AxArgs['ylim'] = [min(Ax.get_yticks()), max(Ax.get_yticks())]
        AxArgs.update({'xticks': range(len(Exp['Freqs'])), 'xticklabels': Exp['Freqs']})

        Result = UnitsPlot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)

    return(Result)


def Qnt_Opsin_Stims(Resp, Opsins=None, Keys=None, HSpace=1, Ax=None, AxArgs={}, File='CellsQuant', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = UnitsPlot.FigAx(Ax)
    plt = UnitsPlot.Plot.Return('plt')

    StimColors = UnitsPlot.Plot.GetColors('StimColors')
    StimHatches = UnitsPlot.Plot.GetColors('StimHatches')

    if not Opsins: Opsins = [_ for _ in Resp.keys()]
    if not Keys: Keys = [sorted([_ for _ in Resp[O].keys() if _ != 'Total']) for O in Opsins]
    Bars = [[Resp[O][K]*100/Resp[O]['Total'] for K in Keys[o]] for o,O in enumerate(Opsins)]
    Colors = [[StimColors[_] for _ in Keys[o]] for o,O in enumerate(Opsins)]
    Hatches = [[StimHatches[_] for _ in Keys[o]] for o,O in enumerate(Opsins)]
    Totals = [Resp[O]['Total'] for O in Opsins]

    Offsets = [0]+[len(_)+HSpace for _ in Bars][:-1]
    Offsets = list(UnitsPlot.Plot.accumulate(Offsets))
    Max = [max(_) for _ in Bars]
    XTicks = []

    for B, Bar in enumerate(Bars):
        XTicks.append(Offsets[B]+len(Bar)/2)
        X = [Offsets[B]+0.5+_ for _ in range(len(Bar))]
        plt.rcParams['hatch.linewidth'] = 2
        BarsB = Ax.bar(X, Bar, color=Colors[B], alpha=0.5, edgecolor=Colors[B])

        for BarB, Hatch in zip(BarsB, Hatches[B]): BarB.set_hatch(Hatch)

        if B == 0:
            for BB, BarB in enumerate(BarsB): BarB.set_label(Keys[B][BB])

        Ax.text(Offsets[B]+len(Bar)/2, Max[B]+5, 'n = '+str(Totals[B]), horizontalalignment='center', verticalalignment='center', fontsize=8)

    if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Perc.'
    if 'xticks' not in AxArgs: AxArgs['xticks'] = XTicks
    if 'xticklabels' not in AxArgs: AxArgs['xticklabels'] = Opsins

    Ax.legend()

    Result = UnitsPlot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Features(UnitRec, FigPath, Exp, BinSize=None, ExtraInfo={}, Ext=['svg'], Save=False, Show=True):
    Rate = round(1/(UnitRec['RasterX'][1,0]-UnitRec['RasterX'][0,0]))*1000

    IDs = np.unique(UnitRec['UnitId'])
#    Exp
    if BinSize:
        UnitRec['PSTHX'] = np.tile(np.arange(UnitRec['PSTHX'][:,0][0],
                                             UnitRec['PSTHX'][:,0][-1],
                                             BinSize),
                                   (UnitRec['PSTHX'].shape[1],1)).T

        for i in range(len(UnitRec['PSTH'])):
            UnitRec['PSTH'][i] = np.vstack((UnitRec['PSTH'][i], np.zeros((1,UnitRec['PSTH'][i].shape[1]))))
            UnitRec['PSTH'][i] = UnitRec['PSTH'][i].reshape((int(UnitRec['PSTH'][i].shape[0]/(BinSize*Rate/1000)),
                                                             int(BinSize*Rate/1000),
                                                             UnitRec['PSTH'][i].shape[1])).sum(axis=1)

            UnitRec['PSTH'][i] = UnitRec['PSTH'][i][:-1,:]

    for I, Id in enumerate(IDs):
        print('Unit', Id)
        Ind = np.where((UnitRec['UnitId'] == Id))[0]

        Spks = [UnitRec['Spks'][_] for _ in Ind]
        Raster = [UnitRec['Raster'][_] for _ in Ind]
        PSTH = [UnitRec['PSTH'][_] for _ in Ind]

        if 'SpkResp' in ExtraInfo:
            ExtraInfo['SpkResp'] = [ExtraInfo['SpkResp'][_] for _ in Ind]
            FR = [UnitRec['FiringRate'][_] for _ in Ind]
            if 'str' in str(type(FR[0])): FR = [IO.Bin.Read(_)[0] for _ in FR]
            ExtraInfo['FiringRate'] = FR

        if 'str' in str(type(Spks[0])):
            Spks = [IO.Bin.Read(_)[0] for _ in Spks]

        if 'str' in str(type(Raster[0])):
            Raster = [IO.Bin.Read(_)[0] for _ in Raster]

        if 'str' in str(type(PSTH[0])):
            PSTH = [IO.Bin.Read(_)[0] for _ in PSTH]

        Stims = UnitRec['StimType'][Ind]
        for s in range(len(Stims)):
            if 'Laser' in Stims[s]: Stims[s] = Stims[s].replace('Laser', 'Light')


        FigFile = FigPath+'/'+Exp+'_Unit'+"{0:04d}".format(Id)+'_AllRecs'
        print(Exp+'_Unit'+"{0:04d}".format(Id)+'_AllRecs')
        # print(UnitRec['StimType'][Ind])
        # print(UnitRec['SpkResp'][Ind])
        print('')

        StimTimes = [[] for _ in Stims]
        StimTypes = [[] for _ in Stims]

        ## for 300ms hists
        # for s,S in enumerate(StimTimes):
        #     if S == ['Sound']:
        #         StimTimes[s] = [[0,3], [100,103], [200,203]]
        #         Stims[s] = ['Sound']*3
        #     elif S == ['Light']:
        #         StimTimes[s] = [[0,10], [100,110], [200,210]]
        #         Stims[s] = ['Light']*3
        #     else:
        #         StimTimes[s] = [[4,7], [104,107], [204,207], [0,10], [100,110], [200,210]]
        #         Stims[s] = ['Sound']*3 + ['Light']*3

        ## for 100ms hists
        for s,S in enumerate(Stims):
            if 'Sound' in S:
                StimTimes[s].append([0,3])
                StimTypes[s].append('Sound')

            if 'Light' in S:
                StimTimes[s].append([0,10])
                StimTypes[s].append('Light')

            for T in ['CNO']:
                if T in S:
                    StimTimes[s].append(np.round(UnitRec['PSTHX'][[0,-1],0]))
                    StimTypes[s].append(T)


        if len(Stims) == len(np.unique(Stims)):
            UnitsPlot.WF_Raster_PSTH_AllRecs(
                Spks, Raster, UnitRec['RasterX'][:,Ind],
                PSTH, UnitRec['PSTHX'][:,Ind],
                Rate, StimTimes, StimTypes,
                None, ExtraInfo, FigFile, Ext=Ext, Save=Save, Show=Show
            )
        else:
            for i,ind in enumerate(Ind):
                FigFileI = '-'.join([
                    '_'.join(FigFile.split('_')[:-1]),
                    UnitRec['StimType'][ind],
                    '_'.join([_[:-3] for _ in UnitRec['Freq'][ind].split('-')])+'kHz',
                    str(int(UnitRec['dB'][ind]))+'dB'
                ])

                print(FigFileI.split('/')[-1])

                UnitsPlot.WF_Raster_PSTH_AllRecs(
                    [Spks[i]], [Raster[i]], UnitRec['RasterX'][:,[ind]],
                    [PSTH[i]], UnitRec['PSTHX'][:,[ind]],
                    Rate, [StimTimes[i]], [StimTypes[i]],
                    None, ExtraInfo, FigFileI, Ext=Ext, Save=Save, Show=Show
                )

    return(None)


def AllPlots(AnalysisPath, Stims, FigPath=None, BinSize=None, Ext=['svg'], Save=False, Show=True):
    if not FigPath: FigPath = AnalysisPath + '/Plots'

    AsdfFiles = sorted(glob(AnalysisPath+'/**/*_AllUnits.asdf', recursive=True))
    for F,File in enumerate(AsdfFiles):
        UnitRec = IO.Asdf.Read(File)
        if not UnitRec['Raster']: continue

        Exp = File.split('/')[-1][:-14]
        Features(UnitRec, FigPath, Exp, BinSize, {}, Ext, Save, Show)

    AsdfFiles = sorted(glob(AnalysisPath+'/**/*_CellChanges.asdf'))
    for F,File in enumerate(AsdfFiles):
        # # Convert Freqs to int: '8000-10000' > 9000
        # IntFreq = np.zeros(AllCells[F]['MaxFreq'].shape, dtype=np.int16)
        # for F, Freq in enumerate(AllCells[F]['MaxFreq']):
        #     IntFreq[F] = sum([float(_) for _ in AllCells[F]['MaxFreq'][F].split('-')])/2

        # FreqsNaCl = IntFreq[AllCells[F]['StimType'] == 'NaCl']
        # FreqsCNO = IntFreq[AllCells[F]['StimType'] == 'CNO']
        # ChangeInFreq = ((FreqsCNO/FreqsNaCl)-1)*100

        CellChanges = IO.Asdf.Read(File)

        UnitInfo = 'PercBars-'+'-'.join(Stims)
        FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
        UnitsPlot.Plot.PercBars(CellChanges, FigFile, Ext, Save, Show)

        UnitInfo = 'Boxplot-'+'-'.join(Stims)
        FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
        AxArgs = {'xlabel': '', 'ylabel': 'Evoked firing rate change'}
        UnitsPlot.Plot.BoxPlots(np.vstack((CellChanges[Stims[1]], CellChanges[Stims[0]])).T, ['NaCl', 'CNO'], AxArgs=AxArgs, FigFile=FigFile, Ext=Ext, Save=Save, Show=Show)

        # AllFiringRate(FR, Save=Save, Show=Show)

    # AsdfFiles = sorted(glob(AnalysisPath+'/**/*_Cells.asdf'))
    # AllCells = [IO.Asdf.Read(File) for File in AsdfFiles]
    # Plot.FreqCurve(AllCells, Ext=Ext, Save=Save, Show=Show)
    # Plot.dBCurve(AllCells, Ext=Ext, Save=Save, Show=Show)

    AsdfFiles = glob(AnalysisPath+'/**/*_CellsChangesMerge.asdf')
    if len(AsdfFiles) != 1:
        print('There should be only one **/*_CellsChangesMerge.asdf file,')
        print('but there are', str(len(AsdfFiles))+'.')
        print('Group data cannot be plotted.')
        return(None)

    CellsChangesMerge = IO.Asdf.Read(AsdfFiles[0])
    UnitInfo = 'PercBarsAll-'+'-'.join(Stims)
    FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
    UnitsPlot.Plot.PercBars(CellsChangesMerge, FigFile, Ext, Save, Show)

    UnitInfo = 'BoxplotAll-'+'-'.join(Stims)
    FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
    AxArgs = {'xlabel': '', 'ylabel': 'Evoked firing rate change'}
    UnitsPlot.Plot.BoxPlots(np.vstack((CellsChangesMerge[Stims[1]], CellsChangesMerge[Stims[0]])).T, ['NaCl', 'CNO'], AxArgs=AxArgs, FigFile=FigFile, Ext=Ext, Save=Save, Show=Show)

    return(None)
