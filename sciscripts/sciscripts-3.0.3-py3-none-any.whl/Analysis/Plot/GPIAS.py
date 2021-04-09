#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2017-06-12
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis.Plot import Plot


## Level 0
def Trace(Data, X, PulseDur, SpanLabel='', LineNoGapLabel='', LineGapLabel='',
          Ax=None, AxArgs={}, File='GPIASTrace', Ext=['svg'], Save=False, Show=True):

    Fig, Ax, ReturnAx = Plot.FigAx(Ax, SubPlotsArgs={})
    Ax.axvspan(X[X>= 0][0], X[X >= PulseDur][0], color='k', alpha=0.5, lw=0, label=SpanLabel)
    Ax.plot(X, Data['NoGap'], color='r', label=LineNoGapLabel, lw=2)
    Ax.plot(X, Data['Gap'], color='b', label=LineGapLabel, lw=2)
    Plot.Set(Ax=Ax, AxArgs=AxArgs)

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Traces(GPIASData, X, SoundPulseDur, File, Normalize=True, Type='Index',
           Ext=['svg'], AxArgs={}, Save=True, Show=True):
    plt = Plot.Return('plt')
    if Type == 'Index': Type = 'IndexTrace'

    print('Plotting...')
    YLim = []
    for F, Freq in GPIASData[Type].items():
        for G in Freq.values():
            if 'float' in str(type(G)): continue
            YLim.append(max(G)); YLim.append(min(G))

    YLim = [(min(YLim) - 0.5).round(), (max(YLim) + 0.5).round()]
    XLim = [round(min(X)-0.5), round(max(X)+0.5)]
    if not Normalize: XLim, YLim = None, None

    PlotNo = len(GPIASData[Type].keys())
    Fig = plt.figure(figsize=(6, 1.5*PlotNo))
    Axes = [plt.subplot(PlotNo,1,_+1) for _ in range(PlotNo)]

    for F, Freq in enumerate(GPIASData[Type].keys()):
        AxArgs['title'] = Freq + ' Hz' + ' Index = ' + str(round(GPIASData['Index'][Freq]['GPIASIndex'], 4))
        LineNoGapLabel = 'No Gap'; LineGapLabel = 'Gap'
        SpanLabel = 'Sound Pulse'
        XLabel = 'time [ms]'; YLabel = 'voltage [mV]'

        PulseDur = SoundPulseDur*1000
        FData = GPIASData[Type][Freq]
        AxArgs = {**{'ylabel': YLabel, 'xlabel': XLabel,
                     'ylim': YLim, 'xlim': XLim}, **AxArgs}
        Axes[F] = Trace(FData, X, PulseDur, SpanLabel, LineNoGapLabel, LineGapLabel, Axes[F], AxArgs)

        # if F != len(GPIASData[Type].keys())-1:
        #     Axes[F].tick_params(bottom=False)
        #     Axes[F].spines['bottom'].set_visible(False)
        #     Axes[F].set_xticklabels([])
        #     Axes[F].set_xlabel('')

        # if F != len(GPIASData[Type].keys())//2:
        #     Axes[F].tick_params(left=False)
        #     Axes[F].spines['left'].set_visible(False)
        #     Axes[F].set_yticklabels([])
        #     Axes[F].set_ylabel('')
        # else:
        #     Axes[F].legend(loc='upper left', prop={'size':6})

    Axes[0].legend(loc='upper left')

    FigTitle = File.split('/')[-1]
    Plot.Set(Fig=Fig, FigTitle=FigTitle)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)
    if Show: plt.show()
    else: plt.close()

    print('Done.')
    return(None)


def IndexPerExp(Indexes, Exps,
                Ax=None, AxArgs={}, File='GPIAS-IndexPerExp', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax, SubPlotsArgs={})

    Pos = list(range(1,len(Exps)+1))
    BoxPlot = Ax.boxplot(Indexes, positions=Pos, showmeans=True)
    for K in ['boxes', 'whiskers', 'caps', 'medians', 'fliers']:
        for I in range(len(Indexes)): BoxPlot[K][I].set(color='k')

    # Ax.text((Pos[0] + Pos[1])/2, sum(Ax.get_ylim())/2, 'n='+str(len(Indexes[0])), ha='center', va='center')

    AxArgs['xlim'] = [0,len(Exps)+1]
    AxArgs['xticks'] = Pos
    AxArgs['xticklabels'] = Exps
    if not 'ylabel' in AxArgs: AxArgs['ylabel'] = 'GPIAS dec. [perc.]'

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def AllAnimalsAllExpAllFreq(Traces_IFAE, Indexes_IFAE, ExpOrder=[], X=[],
                            File='GPIAS-IndexPerExp', Ext=['svg'], Save=False, Show=True):
    Plt = Plot.Return('Plt')
    Exps = ExpOrder if len(ExpOrder) else sorted(np.unique(Indexes_IFAE['Exps']), reverse=True)

    Animals = sorted(np.unique(Indexes_IFAE['Animals']))
    Freqs = sorted(np.unique(Indexes_IFAE['Freqs']), key=lambda x: int(x.split('-')[1]))
    FreqsNo = len(Freqs)
    EmptyX = True if not len(X) else False

    for Animal in Animals:
        Fig, Axes = Plt.subplots(FreqsNo, len(Exps), sharex=True, dpi=96, figsize=(14,10))

        for E,Exp in enumerate(Exps):
            ExpMask = (Indexes_IFAE['Animals'] == Animal) * (Indexes_IFAE['Exps'] == Exp)

            for F,Freq in enumerate(Freqs):
                if not True in (ExpMask * (Indexes_IFAE['Freqs'] == Freq)):
                    continue
                Ind = np.where((ExpMask * (Indexes_IFAE['Freqs'] == Freq)))[0][0]
                if EmptyX:
                    X = np.linspace(-200, 200, Traces_IFAE['Traces'][Ind].shape[0])

                Axes[F][E].axvspan(X[X >= 0][0], X[X >= 0.05*1000][0],
                                color='k', alpha=0.4, lw=0, label='Sound pulse')
                Axes[F][E].plot(X, Traces_IFAE['Traces'][Ind][:,0], 'r', label='NoGap')
                Axes[F][E].plot(X, Traces_IFAE['Traces'][Ind][:,1], 'b', label='Gap')
                Axes[F][E].set_title(Freq+' '+str(Indexes_IFAE['Index'][Ind]))

            if F == E == 0: Axes[F][E].legend()


        for A in Axes:
            for Ax in A: Plot.Set(Ax=Ax)

        Plot.Set(Fig=Fig)
        Fig.suptitle(Animal)
        Fig.tight_layout()

        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Ax.get_legend(),), bbox_inches='tight')

        if Show: Plt.show()
        else: Plt.close()

    return(None)


def Group_AllFreq(Data,
                  Ax=None, AxArgs={}, File='GPIAS-IndexAllFreq', Ext=['pdf'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax, SubPlotsArgs={})

    Pos = [b for a in [[_*2+_+1, _*2+_+2] for _ in range(Data.shape[0]//2)] for b in a]
    Ticks = [np.mean([_*2+_+1, _*2+_+2]) for _ in range(Data.shape[0]//2)]

    Boxes = Ax.boxplot(Data.T, sym='+', widths=0.5, positions=Pos)

    for K in ['whiskers', 'caps', 'fliers']:
        for I in range(len(Boxes[K])):
            Color = 'k' if I%4 in [0,1] else 'maroon'
            Boxes[K][I].set(color=Color)

    for K in ['boxes', 'medians', 'means']:
        for I in range(len(Boxes[K])):
            Color = 'k' if not I%2 else 'maroon'
            Boxes[K][I].set(color=Color)

    Ax.set_xticks(Ticks)
    Ax.set_xticklabels(['8-10', '9-11', '10-12', '12-14', '14-16', '8-16'])
    Ax.set_ylabel('Frequency (KHz)')
    Ax.set_ylabel('GPIAS index')

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)

