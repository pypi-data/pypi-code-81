#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180907
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np
# from glob import glob

from sciscripts.Analysis.Units import Units
from sciscripts.Analysis.Plot import Plot
from sciscripts.IO import IO


## Level 0
def FiringRate(FR, X=[], TTLs=[], Offsets=[],
               Ax=None, AxArgs={}, File='FiringRate', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    if not len(X): X = np.arange(len(FR))

    Ax.plot(X, FR)
    Ax.plot(X, [FR.mean()]*len(FR), 'k--')
    if len(TTLs):
        # Getting TTLs for a specific rec: TTLs = [_/Rate for _ in TTLs if Offsets[rec] < _ < Offsets[rec+1]]
        Ax.plot(TTLs, [FR.max()+1]*len(TTLs), 'ro')

    if 'xlabel' not in AArg: AArg['xlabel'] = 'Time [s]'
    if 'ylabel' not in AArg: AArg['ylabel'] = 'Firing rate [Hz]'
    # if 'xlim' not in AArg: AArg['xlim'] = [round(HistX[0]), round(HistX[-1])+2]
    # if 'ylim' not in AArg: AArg['ylim'] = [0, max(Ax.get_yticks())]

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)
    return(Result)


def ISIH(ISI, ISISize=0.1, SpkNo=None,
         Ax=None, AxArgs={}, File='FiringRate', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    if not SpkNo: SpkNo = 100
    Ax.plot(np.linspace(0, ISISize, len(ISI)), (ISI/SpkNo)*100)

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def LinePSTH(Hist, HistX, StimWindow, StimType=[], Ax=None, AxArgs={}, lw=2, File='WF-LinePSTH', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    HistX = HistX[:-1]
    Mean = Hist.mean(axis=1)
    SEM = Hist.std(axis=1) / (Hist.shape[0]**0.5)
    Mins = Mean-SEM; Mins[Mins<0] = 0

    # BLStD = Hist[HistX<0,:].std()
    # BLSEM = BLStD / (Hist[HistX<0,:].shape[0]**0.5)
    # BLMins = BLMean-BLSEM
    # if BLMins < 0: BLMins = 0
    # if StD: Ax.plot([HistX[0], HistX[-1]], [BLStD]*2)

    if StimType:
        StimColors = Plot.GetColors('StimColors')
        if 'Opsin' in AArg: StimColors['Light'] = StimColors[AArg['Opsin']]

        for S in range(len(StimType)):
            Color = StimColors[StimType[S]]
            Ax.axvspan(StimWindow[S][0], StimWindow[S][1], color=Color, alpha=0.4/len(StimType), lw=0, label='Stim')
            Ax.fill_between(HistX, Mean+SEM, Mins, color=Color, lw=0, alpha=0.3/len(StimType), label='SEM')
    else:
        Color = 'k'
        Ax.axvspan(StimWindow[0][0], StimWindow[0][1], color=Color, alpha=0.4, lw=0, label='Stim')
        Ax.fill_between(HistX, Mean+SEM, Mins, color=Color, lw=0, alpha=0.3, label='SEM')

    if len(Hist[HistX<0,:]):
        BLMean = Hist[HistX<0,:].mean()
        Ax.plot([HistX[0], HistX[-1]], [BLMean]*2, 'k--')

    Ax.plot(HistX, Mean, 'k', lw=lw)
    Ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # Ax.set_yticklabels([str(round(float(l.get_text()),1)) for l in Ax.get_yticklabels()])

    if 'xlabel' not in AArg: AArg['xlabel'] = 'Time [ms]'
    if 'ylabel' not in AArg: AArg['ylabel'] = 'Mean # spikes'
    # if 'xlim' not in AArg: AArg['xlim'] = [round(HistX[0]), round(HistX[-1])+2]
    # if 'ylim' not in AArg: AArg['ylim'] = [0, max(Ax.get_yticks())]

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)
    return(Result)


def RasterPlot(Raster, RasterX, StimWindow, StimType=[], Marker='|', MarkerSize=2, Ax=None, AxArgs={}, File='WF-RasterPlot', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    if StimType:
        StimColors = Plot.GetColors('StimColors')
        if 'Opsin' in AArg: StimColors['Light'] = StimColors[AArg['Opsin']]

        for S in range(len(StimType)):
            Color = StimColors[StimType[S]]
            Ax.axvspan(StimWindow[S][0], StimWindow[S][1], color=Color, alpha=0.4/len(StimType), lw=0, label='Stim')

    else:
        Color = 'k'
        Ax.axvspan(StimWindow[0][0], StimWindow[0][1], color=Color, alpha=0.4, lw=0, label='Stim')

    for R in range(Raster.shape[1]):
        Ax.scatter(RasterX[:-1], Raster[:,R]*(R+1), c='k', marker=Marker, s=MarkerSize)

    if 'xlabel' not in AArg: AArg['xlabel'] = 'Time [ms]'
    if 'ylabel' not in AArg: AArg['ylabel'] = 'Trials'
#     if not 'xlim' in AArg: AArg['xlim'] = [RasterX[0], RasterX[-1]]
#     if not 'ylim' in AArg: AArg['ylim'] = [0, Raster.shape[1]]

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)
    return(Result)


def RI_StimType(RIArray, StimTypeArray,
                Ax=None, AxArgs={}, File='RI_StimType', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    Colors = ['r', 'k']
    Stims = np.unique(StimTypeArray)

    for S, Stim in enumerate(Stims):
        Ax.scatter(RIArray[StimTypeArray == Stim],
                   range(len(RIArray[StimTypeArray == Stim])),
                   c=Colors[S])

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def RI_StimType_Freq(RIArray, StimTypeArray, FreqArray,
                     Ax=None, AxArgs={}, File='RI_StimType_Freq', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt, Axes3D = Plot.Return('Plt'), Plot.Return('Axes3D')
        Fig = Plt.figure(figsize=(4, 4))
        Ax = Axes3D(Fig)

    Colors = ['r', 'k']
    Stims = np.unique(StimTypeArray)

    for S, Stim in enumerate(Stims):
        Ind = StimTypeArray == Stim
        Ax.scatter(range(len(RIArray[Ind])),
                   RIArray[Ind],
                   FreqArray[Ind], c=Colors[S])

    if 'xlabel' not in AArg: AArg['xlabel'] = 'Units'
    if 'ylabel' not in AArg: AArg['ylabel'] = 'FR Change'
    if 'zlabel' not in AArg: AArg['xlabel'] = 'MaxFreq'

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AArg)
        Ax.autoscale(enable=True, axis='both', tight=True)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AArg)
        Fig.patch.set_visible(False)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, dpi=300)

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def WF_MeanAllChs(Waveforms, SpkX, SpaceAmpF=1, StimType=[], Ax=None, AxArgs={}, File='WF-MeanAllChs', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = Plot.FigAx(Ax, {'figsize': (2,4)})

    if StimType:
        StimColors = Plot.GetColors('StimColors')
        if 'Opsin' in AArg: StimColors['Light'] = StimColors[AArg['Opsin']]

        Colors = [StimColors[S]  for S in StimType]
    else:
        Colors = ['k']

    AlphaInit = 0.4
    AlphaFactor = len(StimType) if len(StimType) else 0.4
    Alpha = AlphaInit/AlphaFactor

    # RMSs = [(Waveforms[:, :, Ch].mean(axis=0)**2).mean()**0.5 for Ch in range(Waveforms.shape[2])]
    # BestCh = RMSs.index(max(RMSs))
    BestCh = Units.GetBestCh(Waveforms)

    WF = Waveforms.mean(axis=0)
    Spaces = Plot.GetSpaces(WF)

    YTicks = []
    for S in range(WF.shape[1]):
        if S == BestCh:
            for Color in Colors: Ax.plot(SpkX, WF[:,S]+Spaces[S]*SpaceAmpF, Color, alpha=Alpha)
        else:
            Ax.plot(SpkX, WF[:,S]+Spaces[S]*SpaceAmpF, 'k')

        YTicks.append(np.mean(WF[:,S]+Spaces[S]*SpaceAmpF))

    if 'ylabel' not in AArg: AArg['ylabel'] = 'Channels'
    if 'xlabel' not in AArg: AArg['xlabel'] = 'Time [ms]'
    if 'xticks' not in AArg: AArg['xticks'] = np.linspace(round(SpkX[0],1), round(SpkX[-1],1), 3)
    if 'yticks' not in AArg: AArg['yticks'] = YTicks

    if 'yticklabels' not in AArg:
        AArg['yticklabels'] = np.arange(WF.shape[1])+1
        Mask = np.ones(AArg['yticklabels'].shape[0], bool)
        Mask[[0,-1]] = False
        Mask[[BestCh-1, BestCh, BestCh+1]] = False
        AArg['yticklabels'] = [Y if not Mask[y] else ''
                                 for y,Y in enumerate(AArg['yticklabels'])]

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)

    return(Result)


def WF_BestCh(Waveforms, SpkX, StimType=[], Ax=None, AxArgs={}, File='WF-BestCh', Ext=['svg'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    # RMSs = [(Waveforms[:, :, Ch].mean(axis=0)**2).mean()**0.5 for Ch in range(Waveforms.shape[2])]
    # BestCh = RMSs.index(max(RMSs))
    BestCh = Units.GetBestCh(Waveforms)

    # SpksToplot = 100
    # Spks = np.arange(Waveforms.shape[0]); np.random.shuffle(Spks)
    # Spks = Spks[:SpksToPlot]
    # for Spk in Spks:  Ax.plot(SpkX, Waveforms[Spk, :, BestCh], 'r', alpha=0.1)

    Mean = Waveforms[:, :, BestCh].mean(axis=0)
    StdUp = Mean + Waveforms[:, :, BestCh].std(axis=0)
    StdDown = Mean - Waveforms[:, :, BestCh].std(axis=0)

    if StimType:
        StimColors = Plot.GetColors('StimColors')
        if 'Opsin' in AArg: StimColors['Light'] = StimColors[AArg['Opsin']]

        for S in range(len(StimType)):
            Color = StimColors[StimType[S]]
            Ax.fill_between(SpkX, StdDown, StdUp, color=Color, lw=0, alpha=0.3, label='SEM')
    else:
        Ax.fill_between(SpkX, StdDown, StdUp, color='k', lw=0, alpha=0.3, label='SEM')

    Ax.plot(SpkX, Mean, 'k')
    # Ax.plot(SpkX, StdUp, 'b'); Ax.plot(SpkX, StdDown, 'b')

    if 'xlabel' not in AArg: AArg['xlabel'] = 'Time [ms]'
    if 'ylabel' not in AArg: AArg['ylabel'] = 'Voltage [µV]'
#     if 'xlim' not in AArg: AArg['xlim'] = [round(SpkX[0],2), max(Ax.get_xticks())]
#     if 'ylim' not in AArg: AArg['ylim'] = [min(Ax.get_yticks()), max(Ax.get_yticks())]

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)
    return(Result)


def WF_Raster_PSTH(Waveforms, Raster, RasterX, Hist, HistX, StimWindow=[], StimType=[], MarkerSize=2, Axes=None, AxArgs=None, ExtraInfo={}, File='WF_Raster_PSTH', Ext=['svg'], Save=False, Show=True):
    AArg = None if AxArgs is None else AxArgs.copy()
    ReturnAxes = True
    if not Axes:
        ReturnAxes = False
        Plt = Plot.Return('Plt')
        Fig = Plt.figure(figsize=(8, 3))
        Axes = [Plt.subplot2grid((2, 5), (0, 0), rowspan=2),
                Plt.subplot2grid((2, 5), (0, 1), rowspan=2, colspan=2),
                Plt.subplot2grid((2, 5), (0, 3), colspan=2),
                Plt.subplot2grid((2, 5), (1, 3), colspan=2)]

    Rate = int((1/np.diff(RasterX)[0])*1000)
    SpkX = np.arange(Waveforms.shape[1])*1000/Rate

    if not AArg: AArg = [{} for _ in range(len(Axes))]
    if 'Opsin' in ExtraInfo:
        for A in range(len(AArg)):
            AArg[A]['Opsin'] = ExtraInfo['Opsin']

    YLabel = ['Channels', 'Voltage [µV]', 'Trials', 'Mean # spikes']
    AArg = [{**{'xlabel': 'Time [ms]', 'ylabel': YLabel[A]}, **AArg[A]} for A in range(len(Axes))]
    AArg[1]['title'] = '-'.join(np.unique(StimType))

    if 'FiringRateUnitStr' in ExtraInfo: AArg[2]['title'] = ExtraInfo['FiringRateUnitStr']
    if 'SpkRespUnitStr' in ExtraInfo: AArg[3]['title'] = ExtraInfo['SpkRespUnitStr']

    Axes[0] = WF_MeanAllChs(Waveforms, SpkX, 1, StimType, Axes[0], AArg[0], Save=False, Show=False)
    Axes[1] = WF_BestCh(Waveforms, SpkX, StimType, Axes[1], AArg[1], Save=False, Show=False)

    if len(StimWindow):
        Axes[2] = RasterPlot(Raster, RasterX, StimWindow, StimType, '|', MarkerSize, Axes[2], AArg[2], Save=False, Show=False)
        Axes[3] = LinePSTH(Hist, HistX, StimWindow, StimType, Axes[3], AArg[3], Save=False, Show=False)

#     Axes[0].autoscale(enable=True, axis='y', tight=True)
#     Axes[0].spines['left'].set_bounds(Axes[0].get_yticks()[0], Axes[0].get_yticks()[-1])

    Axes[1].locator_params(axis='x', nbins=4)

    Axes[2].spines['bottom'].set_visible(False)
    Axes[2].get_xaxis().set_visible(False)
#     Axes[2].locator_params(axis='y', nbins=4)

    # if 'Opsin' in ExtraInfo and '-'.join(StimType) == 'Sound-Light':
    #     if ExtraInfo['Opsin'] == 'Arch':
    #         Axes[2].text(-50, 3000, 'LightLightLightLightLight',
    #                      fontsize = 8,zorder = 6, color = 'g', bbox={'edgecolor':'g','facecolor':'g', 'alpha':1})

    # Axes[3].set_yticks(np.linspace(Axes[3].get_yticks()[0], Axes[3].get_yticks()[-1], 4))

    if ReturnAxes: return(Axes)
    else:
        FigTitle = File.split('/')[-1] if '/' in File else File
        Plot.Set(Fig=Fig, FigTitle=FigTitle)
        Fig.subplots_adjust(wspace=1.5)

        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            if ' ' in File: File = File.split(' ')[0]
            for E in Ext: Fig.savefig(File+'.'+E, dpi=300)

        if Show: Plt.show()
        else: Plt.close()

        return(None)


def WF_Raster_PSTH_AllRecs(Waveforms, Raster, RasterX, Hist, HistX, StimWindow=[], StimType=[], AxArgs=None, ExtraInfo={}, File='WF_Raster_PSTH', Ext=['svg'], Save=False, Show=True):
    AArg = None if AxArgs is None else AxArgs.copy()
    # HistMin = round(min([min((R.mean(axis=1)) + (R.std(axis=1) / (R.shape[0]**0.5))) for R in Hist]), 2)
    # if HistMin < 0: HistMin = 0
    HistMin = 0
    HistMax = round(max([max((R.mean(axis=1)) + (R.std(axis=1) / (R.shape[0]**0.5))) for R in Hist]), 2)

    ## Oh crap look at this
    SpkMin = round(
        min(
            [min(
                (R[:, :, [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                          for Ch in range(R.shape[2])
                          ].index(max(
                              [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                               for Ch in range(R.shape[2])
                               ]
                              )
                          )
                    ].mean(axis=0)
                )
                -
                (R[:, :, [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                          for Ch in range(R.shape[2])
                          ].index(max(
                              [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                               for Ch in range(R.shape[2])
                               ]
                              )
                          )
                   ].std(axis=0)
                )
            ) for R in Waveforms if R.shape[0]]
        )
    )

    SpkMax = round(
        max(
            [max(
                (R[:, :, [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                          for Ch in range(R.shape[2])
                          ].index(max(
                              [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                               for Ch in range(R.shape[2])
                               ]
                              )
                          )
                   ].mean(axis=0)
                )
                +
                (R[:, :, [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                          for Ch in range(R.shape[2])
                          ].index(max(
                              [(R[:, :, Ch].mean(axis=0)**2).mean()**0.5
                               for Ch in range(R.shape[2])
                               ]
                              )
                          )
                   ].std(axis=0)
                )
            ) for R in Waveforms if R.shape[0]]
        )
    )
    ## All this is actually 2 lines!!
    ## o.O

    plt = Plot.Return('plt')
    FigSize = Plot.FigSize.copy()
    FigSize[1] *= 0.7*len(Hist)
    Fig = plt.figure(figsize=FigSize)
    Axes = [
        [plt.subplot2grid((2*len(Hist), 5), (0+(R*2), 0), rowspan=2),
         plt.subplot2grid((2*len(Hist), 5), (0+(R*2), 1), rowspan=2, colspan=2),
         plt.subplot2grid((2*len(Hist), 5), (0+(R*2), 3), colspan=2),
         plt.subplot2grid((2*len(Hist), 5), (1+(R*2), 3), colspan=2)]
        for R in range(len(Hist))
    ]

    if not AArg: AArg = [[{},{'ylim':[SpkMin,SpkMax]},
                              {},{'ylim':[HistMin,HistMax]}]
                             for _ in range(len(Hist))]

    for R in range(len(Hist)):
        # if not len(StimWindow[R]):
        #     # Baseline recording has no TTLs, so no PSTH or Raster
        #     continue

        if 'SpkRespUnit' in ExtraInfo:
            ExtraInfo['SpkRespUnitStr'] = 'p = ' + str(round(ExtraInfo['SpkRespUnit'][R], 4))

        if 'FiringRateUnit' in ExtraInfo:
            ExtraInfo['FiringRateUnitStr'] = str(round(ExtraInfo['FiringRateUnit'][R].mean(), 2)) + 'Hz'

        Axes[R] = WF_Raster_PSTH(Waveforms[R], Raster[R], RasterX[:,R], Hist[R],
                       HistX[:,R], StimWindow[R], StimType[R], Axes=Axes[R],
                       AxArgs=AArg[R], ExtraInfo=ExtraInfo, Save=False, Show=False)

    FigTitle = File.split('/')[-1] if '/' in File else File
    Plot.Set(Fig=Fig, FigTitle=FigTitle)
    Fig.subplots_adjust(hspace=0.5)
    for A in range(len(Axes)-1):
        for a in [0,1,3]:
            Axes[A][a].set_xticklabels([])
            Axes[A][a].set_xlabel('')

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        if ' ' in File: File = File.split(' ')[0]
        for E in Ext: Fig.savefig(File+'.'+E, dpi=300)

    if Show: plt.show()
    else: plt.close('all')

    return(None)


## Level 1
def Features(UnitRec, BinSize=None, ExtraInfo={}, Exp='00', FigPath='.', Ext=['svg'], Save=False, Show=True):
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
            ExtraInfo['SpkRespUnit'] = [ExtraInfo['SpkResp'][_] for _ in Ind]
            FR = [UnitRec['FiringRate'][_] for _ in Ind]
            if 'str' in str(type(FR[0])): FR = [IO.Bin.Read(_)[0] for _ in FR]
            ExtraInfo['FiringRateUnit'] = FR

        if 'str' in str(type(Spks[0])):
            Spks = [IO.Bin.Read(_)[0] for _ in Spks]

        if 'str' in str(type(Raster[0])):
            Raster = [IO.Bin.Read(_)[0] for _ in Raster]

        if 'str' in str(type(PSTH[0])):
            PSTH = [IO.Bin.Read(_)[0] for _ in PSTH]

        # if True in [np.isnan(_).any() for _ in Spks]:
        #     print('Spike waveforms contains nan, skipping...')
        #     continue

        # if True in [np.isnan(_).all() for _ in Raster]:
        #     print('Raster contains nan, skipping...')
        #     continue

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
            WF_Raster_PSTH_AllRecs(
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
                ExtraInfo_i = {K: [V[i]] if K in ['SpkRespUnit', 'FiringRateUnit'] else V for K,V in ExtraInfo.items()}

                WF_Raster_PSTH_AllRecs(
                    [Spks[i]], [Raster[i]], UnitRec['RasterX'][:,[ind]],
                    [PSTH[i]], UnitRec['PSTHX'][:,[ind]],
                    Rate, [StimTimes[i]], [StimTypes[i]],
                    None, ExtraInfo_i, FigFileI, Ext=Ext, Save=Save, Show=Show
                )

    return(None)

