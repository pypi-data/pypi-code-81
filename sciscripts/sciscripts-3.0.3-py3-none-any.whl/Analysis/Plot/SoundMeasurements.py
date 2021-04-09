#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2018-09-04
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os

from sciscripts.Analysis.Analysis import FilterSignal
from sciscripts.Analysis.Plot import Plot
from sciscripts.IO import DAqs

## Plots
def Intensity_AmpF(SoundIntensity, Ax=None, AxArgs={}, File='IntensityCurve-Freq_AmpF', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots()

    Colors = Plot.GetColors('Colors')

    for F,Freq in enumerate(SoundIntensity['Freqs']):
        Ax.semilogx(SoundIntensity['AmpFs'], SoundIntensity['dB'][:,F],
                    label=Freq + ' Hz', color=Colors[F])

    Default = {
        'xlabel': 'Sound amplification factor',
        'ylabel': 'Intensity [dBSPL]',
        'xlim': Ax.get_xlim(),
        'ylim': Ax.get_ylim(),
    }

    AxArgs = {**Default, **AxArgs}
    Ax.legend(loc='upper left')

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


def PxxSp(PSD, SoundIntensity, SoundAmpF, Freq, Colormap, Ax=None, AxArgs={}, File='PowerSpectrumDensity', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots()

    F = SoundIntensity['Freqs'].tolist().index(Freq)
    for A,AmpF in enumerate(SoundAmpF[Freq]):
        # if AmpF == '0.0': AmpF = '0'
        A_SI = SoundIntensity['AmpFs'].tolist().index(AmpF)

        Colors = [Colormap(255-(A*255//len(SoundAmpF[Freq])))]
        LineLabel = str(SoundIntensity['dB'][A_SI,F].round()) + ' dB'

        Ax.semilogy(PSD['F'][:,A_SI,F], PSD['PxxSp'][:,A_SI,F],
                    label=LineLabel, color=Colors[0])

        # for IAmpF in SoundIntensity:
        #     IdB = SoundIntensity[IAmpF]['dB']

        #     if SoundIntensity[AKey]['dB'] == IdB:
        #         Ax.semilogy(PSD[IAmpF][0], PSD[IAmpF][1],
        #                     label=LineLabel, color=Colors[0])
        #     else: continue

    Default = {
        'xlabel': 'Frequency [Hz]',
        'ylabel': 'PSD [V²/Hz]',
        'xlim': [5000, 20000]
    }

    AxArgs = {**Default, **AxArgs}

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


def Table(SoundIntensity, Ax=None, File='IntensityTable', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Plt = Plot.Return('Plt')
        Fig, Ax = Plt.subplots(subplot_kw={'frame_on':False})

    Ax.xaxis.set_visible(False)
    Ax.yaxis.set_visible(False)
    Ax.table(cellText=SoundIntensity['dB'], rowLabels=SoundIntensity['AmpFs'], colLabels=SoundIntensity['Freqs'], loc='center')

    if ReturnAx:
        return(Ax)
    else:
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)

        if Show: Plt.show()
        else: Plt.close()
        return(None)


def PxxSp_Freq(SoundIntensity, PSD, System, Setup, Intensities=[80, 70, 60, 50, 40, 30, 0], Ax=None, AxArgs={}, File='PowerSpectrumDensity_AllFreqs', Ext=['svg'], Save=False, Show=True):
    Colormaps = Plot.GetColors('Colormaps')

    SoundAmpF = DAqs.dBToAmpF(Intensities, System, Setup)
    SoundAmpF = {A: [str(_) for _ in AmpF] for A,AmpF in SoundAmpF.items()}

    Plt = Plot.Return('Plt')
    Fig, Axes = Plt.subplots(len(SoundIntensity['Freqs']), sharex=True)
    for F,Freq in enumerate(SoundIntensity['Freqs']):
        if F >= len(Colormaps): f = len(Colormaps)-F-1
        else: f = F

        Axes[F] = PxxSp(PSD, SoundIntensity, SoundAmpF, Freq, Colormaps[f],
                       Ax=Axes[F], AxArgs={'title': Freq, 'xlabel': ''},
                       Save=False, Show=False)

    Axes[-1].set_xlabel('Frequency [Hz]')

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)

    if Show: Plt.show()
    else: Plt.close()
    return(None)


def All(System, Setup, FigPath=None, Ext=['svg'], Save=False, Show=True):
    SoundIntensity = DAqs.GetSoundIntensity(System, Setup)
    PSD = DAqs.GetPSD(System, Setup)
    if not FigPath: FigPath = DAqs.CalibrationPath+'/'+System+'/'+Setup

    Intensity_AmpF(SoundIntensity, File=FigPath+'/IntensityCurve-Freq_AmpF', Ext=Ext, Save=Save, Show=Show)
    PxxSp_Freq(SoundIntensity, PSD, System, Setup, File=FigPath+'/PowerSpectrumDensity_AllFreqs', Ext=Ext, Save=Save, Show=Show)
    # Table(SoundIntensity, File=FigPath+'IntensityTable', Ext=['pdf'], Save=Save, Show=Show)
    return(None)
