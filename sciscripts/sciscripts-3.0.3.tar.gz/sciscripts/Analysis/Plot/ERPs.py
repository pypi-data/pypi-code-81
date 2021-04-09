#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20190428
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis.Plot import Plot

def Paired(Data, X, ScaleBar=0, lw=1, Title='', ShowLines=True,
           Ax=None, AxArgs={}, File='Paired8Ch', Ext=['pdf'], Save=False, Show=True):

    # Plt = Plot.Return('plt')
    ShowTitle = False if Ax else True
    Fig, Ax, ReturnAx = Plot.FigAx(Ax, {'figsize':(4, 8.27)})

    # Fig, Ax = Plt.subplots(figsize=(4, 8.27))
    # Plot channels
    if 'xticks' not in AxArgs.keys():
        AxArgs['xticks'] = np.linspace(X[0], X[-1], 4)

    Ax = Plot.AllCh(Data, X, Ax=Ax, AxArgs=AxArgs, ScaleBar=ScaleBar, lw=lw)

    if ShowLines:
        # plot P20, P40 and P60 lines
        Line20 = X[X >= 0.02][0]
        # Line40 = X[X >= 0.04][0]
        # Line60 = X[X >= 0.06][0]
        Line520 = X[X >= 0.52][0]
        # Line540 = X[X >= 0.54][0]
        # Line560 = X[X >= 0.56][0]

        LineY = Ax.get_ylim()
        Ax.plot([Line20]*2, LineY, 'b--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line40]*2, LineY, 'r--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line60]*2, LineY, 'g--', lw=lw/1.3, zorder=1)
        Ax.plot([Line520]*2, LineY, 'b--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line540]*2, LineY, 'r--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line560]*2, LineY, 'g--', lw=lw/1.3, zorder=1)

    if ShowTitle: Fig.suptitle(Title)
    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Paired8Ch(Data, X, ScaleBar=0, lw=1, Title='',
              File='Paired8Ch', Ext=['pdf'], Save=False, Show=True):

    if Data.shape[1] % 2:
        print('This function only allows arrays with even number of columns.')
        return(None)

    Plt = Plot.Return('plt')

    Fig, Axes = Plt.subplots(1, 2, figsize=(8.27, 8.27))
    # Plot channels
    AxArgs = {'xticks': np.linspace(X[0], X[-1], 4)}
    Axes[0] = Plot.AllCh(Data[:,:Data.shape[1]//2], X, Ax=Axes[0], AxArgs=AxArgs, ScaleBar=ScaleBar, lw=lw)
    Axes[1] = Plot.AllCh(Data[:,Data.shape[1]//2:], X, Ax=Axes[1], AxArgs=AxArgs, ScaleBar=ScaleBar, lw=lw)

    # plot P20, P40 and P60 lines
    Line20 = X[X >= 0.02][0]
    # Line40 = X[X >= 0.04][0]
    # Line60 = X[X >= 0.06][0]
    Line520 = X[X >= 0.52][0]
    # Line540 = X[X >= 0.54][0]
    # Line560 = X[X >= 0.56][0]

    for Ax in Axes:
        LineY = Ax.get_ylim()
        Ax.plot([Line20]*2, LineY, 'b--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line40]*2, LineY, 'r--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line60]*2, LineY, 'g--', lw=lw/1.3, zorder=1)
        Ax.plot([Line520]*2, LineY, 'b--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line540]*2, LineY, 'r--', lw=lw/1.3, zorder=1)
        # Ax.plot([Line560]*2, LineY, 'g--', lw=lw/1.3, zorder=1)

    Fig.suptitle(Title)
    Plot.Set(Fig=Fig)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        if ' ' in File: File = File.split(' ')[0]
        for E in Ext: Fig.savefig(File+'.'+E, dpi=300)

    if Show: Plt.show()
    else: Plt.close(Fig)

    return(None)


def Paired8ChSepClick(Data, X, lw=1, Title='',
                      File='Paired8ChSepClick', Ext=['pdf'], Save=False, Show=True):

    if Data.shape[1] % 2:
        print('This function only allows arrays with even number of columns.')
        return(None)

    Plt = Plot.Return('plt')

    Fig, Axes = Plt.subplots(Data.shape[1]//2, 4, figsize=(8.27,5.51))
    # Plot channels
    Zero = np.where((X >= 0))[0][0]
    Rate = int(round(1/(X[1] - X[0])))
    Start = [Zero-int(Rate*0.05), Zero-int(Rate*0.05)+int(Rate*0.5)]
    End = [Zero+int(Rate*0.15), Zero+int(Rate*0.15)+int(Rate*0.5)]

    # plot P20, P40 and P60 lines
    Line20 = X[X >= 0.02][0]
    Line40 = X[X >= 0.04][0]
    Line60 = X[X >= 0.06][0]
    Line520 = X[X >= 0.52][0]
    Line540 = X[X >= 0.54][0]
    Line560 = X[X >= 0.56][0]

    for Ch in range(Data.shape[1]):
        L = Ch % 8
        C = 0
        if Ch > 7: C = 2

        Axes[L][C].plot(X[Start[0]:End[0]], Data[Start[0]:End[0],Ch], 'k', lw=lw)
        Axes[L][C+1].plot(X[Start[1]:End[1]], Data[Start[1]:End[1],Ch], 'k', lw=lw)

        LineY = [Axes[L][C].get_ylim(), Axes[L][C+1].get_ylim()]

        Axes[L][C].plot([Line20]*2, LineY[0], 'b--', lw=lw/1.3, zorder=1)
        Axes[L][C].plot([Line40]*2, LineY[0], 'r--', lw=lw/1.3, zorder=1)
        Axes[L][C].plot([Line60]*2, LineY[0], 'g--', lw=lw/1.3, zorder=1)

        Axes[L][C+1].plot([Line520]*2, LineY[1], 'b--', lw=lw/1.3, zorder=1)
        Axes[L][C+1].plot([Line540]*2, LineY[1], 'r--', lw=lw/1.3, zorder=1)
        Axes[L][C+1].plot([Line560]*2, LineY[1], 'g--', lw=lw/1.3, zorder=1)


    for L,Line in enumerate(Axes):
        for C,Ax in enumerate(Line):
            if C % 2:
                Ax.tick_params(left=False, labelleft=False)
                Ax.spines['left'].set_visible(False)
                Ax.spines['left'].set_position(('axes', 0))
            else:
                Ax.tick_params(left=False, labelleft=False)

            if L != 7:
                Ax.tick_params(bottom=False, labelbottom=False)
                Ax.spines['bottom'].set_visible(False)
                Ax.spines['bottom'].set_position(('axes', 0))


    Fig.suptitle(Title)
    # Plot.Set(Fig=Fig)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        if ' ' in File: File = File.split(' ')[0]
        for E in Ext: Fig.savefig(File+'.'+E, dpi=300)

    if Show: Plt.show()
    else: Plt.close(Fig)

    return(None)

