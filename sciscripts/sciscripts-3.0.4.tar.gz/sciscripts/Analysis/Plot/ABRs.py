#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170707
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Plot import Plot


## Level 0
def Single(ABR, X, AllCh=False,
           Ax=None, AxArgs={}, File='ABRs-SingleIntensity', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots()

    BestCh = Analysis.GetStrongestCh(ABR)

    if AllCh:
        for Ch in range(ABR.shape[1]): Ax.plot(X, ABR[:,Ch], lw=2, label=str(Ch))
    else:
        Ax.plot(X, ABR[:,BestCh], 'k', lw=2, label=str(BestCh))

    Ax.plot([X[X==0], X[X==3]], [max(ABR[:,BestCh])*1.2]*2, 'r', lw=2, label='Sound')

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Peaks = Analysis.GetPeaks(ABR[:,BestCh])
        Ax.plot(X[Peaks['Pos']], ABR[Peaks['Pos'],BestCh], 'r*', label='Peaks')
        Ax.plot(X[Peaks['Neg']], ABR[Peaks['Neg'],BestCh], 'r*')

        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        Ax.legend(loc='best')

        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def Multiple(ABRs, X, SpaceAmpF=1, StimDur=None, Peaks=[], PeaksColors=[], Colormap=[],
             Ax=None, AxArgs={}, File='ABRs-SingleFrequency', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots(figsize=(4,4))

    Rev = False if '0' in ABRs else True
    Recs = sorted(list(ABRs.keys()), reverse=Rev)

    AxArgs['xtickspacing'] = round((X[-1]-X[0])/5)

    if ABRs[Recs[0]].shape[1] > 1:
        Chs = ABRs[Recs[0]].copy()
        for M, Max in enumerate(abs(Chs).max(axis=0)): Chs[:,M] /= Max
        for Ch in range(Chs.shape[1]):
            Chs[:,Ch] = abs(np.mean(
                Chs[np.where((X>=0)*(X<1))[0],Ch]/
                Chs[np.where((X>=-1)*(X<0))[0],Ch]
            ))
        Chs = [Chs[0,:].argmax()]
        # Chs = Analysis.GetStrongestCh(ABRs[Recs[0]][np.where((X>=0)*(X<3)),:])
        # Chs = [Chs]

        ABRs = {K: V[:,Chs].reshape((V[:,Chs].shape[0], len(Chs)))
                for K,V in ABRs.items()}
    else:
        Chs = [0]

    # ABRs = {K: V/ABRs[Recs[0]][:,0].max() for K,V in ABRs.items()}
    Spaces = Plot.GetSpaces(ABRs, Recs)
    if not PeaksColors: PeaksColors = Plot.GetColors('colors')
    if not Colormap:
        Colormap = Plot.GetColors('colormaps')
        Colormap = Colormap[0]

    YTicks = np.zeros(len(Recs))
    for Ch in range(len(Chs)):
        for R,Rec in enumerate(Recs):
            Color = Colormap(255-(R*20))
            Y = ABRs[Rec][:,Ch] + Spaces[R]*SpaceAmpF
            Ax.plot(X, Y, color=Color)#, label=Rec)

            if not Ch: YTicks[-(R+1)] = Y.mean()

            if len(Peaks):
                if R >=len(Peaks): continue
                # Ax.plot(X[Peaks[R]], Y[Peaks[R]], 'k*')
                for p,P in enumerate(Peaks[R]):
                    # print(P)
                    if P == -1: continue
                    if p >= len(PeaksColors): continue
                    Ax.plot(X[P], Y[P], PeaksColors[p]+'*', lw=0.75)

            del(Y)

    Y = Ax.get_ylim()
    if StimDur:
        Ax.plot([X[X>=0][0], X[X<=StimDur*1000][-1]], [max(Y)*1.2]*2, 'k', lw=3)
        # FontDict = {'size':8, 'ha':'center', 'va':'bottom'}
        # Ax.text(np.mean([X[X>=0][0], X[X<=StimDur*1000][-1]]), max(Y)*1.2, 'Sound pulse', fontdict=FontDict)

    Ax.tick_params(left=False)
    Ax.spines['left'].set_visible(False)

    YLabels = np.flipud([_[:-2] if _[:-2].lower() == 'db' else _ for _ in Recs])
    AxArgs['yticks'] = YTicks
    AxArgs['yticklabels'] = YLabels
    # if 'ylim' not in AxArgs: AxArgs['ylim'] = Y
    if 'xlim' not in AxArgs: AxArgs['xlim'] = [round(X[0],2), round(X[-1])]
    if 'xlabel' not in AxArgs: AxArgs['xlabel'] = 'Time [ms]'
    if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Intensity [dB]'
    Ax.legend(loc='upper right', frameon=False)
    # print(Y)
    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def LatencyPerFreq(Latencies, Intensities,
                   Ax=None, AxArgs={}, File='ABRs-LatencyPerFreq', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots(figsize=(4,2))

    Colors = Plot.GetColors('colors')

    Freqs = sorted(list(Latencies.keys()), key=lambda x: [int(y) for y in x.split('-')])
    SmallFreqs = [_.split('-')[0][:-3]+'-'+_.split('-')[1][:-3] for _ in Freqs]
    Min = min([min(_) for _ in Latencies.values()])
    Min = round((Min-0.25) * 2) / 2
    Max = max([max(_) for _ in Latencies.values()])
    Max = round((Max+0.25) * 2) / 2
    if 'ylim' not in AxArgs: AxArgs['ylim'] = [Min, Max]

    for F, Freq in enumerate(Freqs):
        Ax.plot(Intensities, Latencies[Freq], Colors[F]+'.-', label=SmallFreqs[F])

    Ax.set_xlim([Intensities[0], Intensities[-1]])
    # Ax = Plot.FitLegendOutside(Ax)
    Ax.legend(loc='upper left', ncol=2, bbox_to_anchor=(0, 1.3))

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Ax.get_legend(),), bbox_inches='tight')

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def ThresholdsPerFreq(Thresholds, Freqs,
                      Ax=None, AxArgs={}, File='ABRs-TresholdsPerFreq', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots(figsize=(4,2))

    Pos = list(range(1,len(Freqs)+1))
    BoxPlot = Ax.boxplot(Thresholds, positions=Pos, showmeans=True)
    for K in ['boxes', 'whiskers', 'caps', 'medians', 'fliers']:
        for I in range(len(Thresholds)):
            BoxPlot[K][I].set(color='k')

    AxArgs['xticks'] = Pos
    AxArgs['xlim'] = [Pos[0]-0.5, Pos[-1]+0.5]
    AxArgs['xticklabels'] = Freqs
    AxArgs['yticks'] = [30, 40, 50, 60, 70, 80]
    AxArgs['ylim'] = [AxArgs['yticks'][0], AxArgs['yticks'][-1]]

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Ax.get_legend(),), bbox_inches='tight')

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def Triang3D(ABRs, X, Azimuth=-110, Elevation=50, Step=1, Show=True):
    Plt = Plot.Return('Plt')
    Axes3D = Plot.Return('Axes3D')
    Triangulation = Plot.Return('Triangulation')

    print('Plotting...')
    Colormaps = [Plt.get_cmap('Reds'), Plt.get_cmap('Blues')]
    YLabel = 'Intensity [dBSPL]'; XLabel = 'Time [ms]'
    ZLabel = 'Voltage [mV]'

    Fig = Plt.figure()
    Axes = Axes3D(Fig)

    Intensities = sorted(list(ABRs.keys()), reverse=True)
    X = np.concatenate([X[np.arange(0,X.shape[0],Step)],
                        X[np.arange(0,X.shape[0],Step)]])

    for LineIndex in range(len(Intensities)-1):
        dB0 = Intensities[LineIndex]
        dB1 = Intensities[LineIndex+1]

        ABR0 = ABRs[dB0][np.arange(0,ABRs[dB0].shape[0],Step),0]
        ABR1 = ABRs[dB1][np.arange(0,ABRs[dB0].shape[0],Step),0]

        Y = [int(dB0)]*len(ABR0) + [int(dB1)]*len(ABR1)
        Z = np.concatenate([ABR0, ABR1])
        T = Triangulation(X, Y)

        Axes.plot_trisurf(X, Y, Z, triangles=T.triangles,
                          cmap=Colormaps[0], edgecolor='none',
                          antialiased=False, shade=False)

#    Axes.locator_params(tight=True)
    Axes.set_xlabel(XLabel); Axes.set_ylabel(YLabel)
    Axes.set_zlabel(ZLabel)
    Axes.grid(False)
    Axes.view_init(Elevation, Azimuth)

    if Show: Plt.show()

    return(None)


## Level 1
def Traces_LatencyPerFreq_AllFreqs(
        ABRs, X, Latencies, Intensities, Thresholds, Freqs, SpaceAmpF=1.5, StimDur=None, Peaks=None,
        File='ABRs-Traces_LatencyPerFreq_AllFreqs', Ext=['svg'], Save=False, Show=True
    ):
    Plt = Plot.Return('Plt')

    Fig = Plt.figure(figsize=(7.086614, 3.5), dpi=200)
    Axes = [Plt.subplot2grid((2, 2), (0, 0), rowspan=2),
            Plt.subplot2grid((2, 2), (0, 1)),
            Plt.subplot2grid((2, 2), (1, 1))]

    YLabel = ['Intensity [dB]', 'Latency [ms]', 'Threshold [dB]']
    XLabel = ['Time [ms]', 'Intensity [dB]', 'Frequency [kHz]']
    AxArgs = [{'xlabel': XLabel[A], 'ylabel': YLabel[A]} for A in range(len(Axes))]

    Axes[0] = Multiple(ABRs, X, SpaceAmpF, StimDur, Peaks, Axes[0], AxArgs[0], Save=False, Show=False)
    Axes[1] = LatencyPerFreq(Latencies, Intensities, Axes[1], AxArgs[1], Save=False, Show=False)
    Axes[2] = ThresholdsPerFreq(Thresholds, Freqs, Axes[2], AxArgs[2], Save=False, Show=False)

    Plt.figtext(0.0, 0.95, 'A', fontsize=14)
    Plt.figtext(0.5, 0.95, 'B', fontsize=14)
    Plt.figtext(0.5, 0.5, 'C', fontsize=14)

    Plot.Set(Fig=Fig)
    Fig.subplots_adjust(wspace=0.3, hspace=0.7)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Axes[1].get_legend(),), bbox_inches='tight')

    if Show: Plt.show()
    else: Plt.close()
    return(None)

