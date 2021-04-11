#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Plot.Plot] Importing dependencies...')
import os
import numpy as np
from itertools import accumulate#, combinations
from matplotlib.colors import to_rgba
from subprocess import check_output

from sciscripts.Analysis.Analysis import Pairwise
print('[Analysis.Plot.Plot] Done.')

## Level 0
def BarAutolabel(Bars, Ax, Color='k', Position='bottom'):
    """
    Modified from http://matplotlib.org/examples/api/barchart_demo.html
    Attach a text label above each bar displaying its height.
    """

    for Bar in Bars:
        Height = Bar.get_height()
        Ax.text(Bar.get_x() + Bar.get_width()/2.,
                Height,# * Space,
                str(Height),
                color=Color,
                ha='center',
                va=Position)

    return(Ax)


def ClickCallback(Event):
    """ Taken and modified from Joe Kington's code.
        Source at https://stackoverflow.com/a/27566966 """

    global X, Y
    # X, Y = None, None
    while X == Y == None:
        print('Click on the speaker position.')
        if Event.inaxes is not None:
            print(Event.xdata, Event.ydata)
            X, Y = Event.inaxes.transData.inverted().transform((Event.x, Event.y))
        else:
            print('Clicked coordinate is ouside axes limits')

    plt.close()
    return(None)


def FitLegendOutside(Ax, Width=0.8, Loc='center left', Frame=False):
    # Shrink axis and fit legend outside plot
    # Taken from IanS at https://stackoverflow.com/a/4701285
    Box = Ax.get_position()
    Ax.set_position([Box.x0, Box.y0, Box.width * Width, Box.height])
    Ax.legend(loc=Loc, bbox_to_anchor=(1, 0.5), frameon=Frame)

    return(Ax)


def GetScreenInfo():
    Screen = {}
    try:
        Screen['DPI'] = check_output(['xdpyinfo'])
        Screen['DPI'] = str(Screen['DPI']).split('screen #')[1:]
        Screen['DPI'] = [_.split('resolution')[1].split('\\n')[0].split('x')[0].split(' ')[-1] for _ in Screen['DPI']]
        Screen['DPI'] = [int(_) for _ in Screen['DPI']]
    except:
        print('xdpyinfo not installed. Assuming a 96 dpi screen.')
        Screen['DPI'] = [96]

    try:
        Size = check_output(['xrandr'])
        Size = [l for l in str(Size).split('\\n') if ' connected' in l]
        Screen['Size_mm'] = [[int(_[:-2]) for _ in f.split(' ') if 'mm' in _] for f in Size ]
        Screen['Size_px'] = [_.split('+')[0].split('x') for f in Size for _ in f.split(' ') if 'x' in _ and '+' in _]
        Screen['Size_px'] = [[int(_) for _ in s] for s in Screen['Size_px']]
    except:
        print('xrandr not installed. Assuming a 15.6" full HD screen.')
        Screen['Size_mm'] = [[344, 193]]
        Screen['Size_px'] = [[1920, 1080]]

    if len(np.unique([
        len(Screen['DPI']),
        len(Screen['Size_mm']),
        len(Screen['Size_px'])
    ])) > 1:
        # In case only one of xdpyinfo or xrandr are available, and the system
        # has more than one screen, use only info about the first screen.
        Screen['DPI'] = [Screen['DPI'][0]]
        Screen['Size_mm'] = [Screen['Size_mm'][0]]
        Screen['Size_px'] = [Screen['Size_px'][0]]

    ScreenNo = len(Screen['DPI'])
    Screen['Size_in'] = [[_*0.03937008 for _ in s] for s in Screen['Size_mm']]
    Screen['RealDPI'] = [round(Screen['Size_px'][_][0]/Screen['Size_in'][_][0]) for _ in range(ScreenNo)]

    return(Screen)


def GetSpaces(Data, KeyList=None):
    """
        Calculate offsets for plotting all channels in the same plot without overlap.

        Parameters:
            Data: array_like or dict
                If array_like, Data must be a 2D array, with dimensions (samples, channels).
                If dict, Data must be shaped as {Channel: Samples}.

            KeyList: list or None, optional
                List of keys if Data is a dict. If None, Data keys should be int or int() convertable, and KeyList will be  a list of the sorted keys.
                Ignored if Data is array_like.

        Returns:
            Spaces: list
                The offset for each channel to be plot without overlap.
    """
    if type(Data) in [list, np.ndarray, np.memmap]:
        Spaces = [min(Data[:,P[0]])-max(Data[:,P[1]]) for P in Pairwise(range(Data.shape[1]))]

    elif type(Data) == dict:
        if not KeyList: KeyList = sorted(Data.keys(), key=lambda x: int(x))
        Spaces = [min(Data[P[0]])-max(Data[P[1]]) for P in Pairwise(KeyList)]

    Spaces = [0]+list(accumulate(Spaces))

    return(Spaces)


def GetTicks(Ax, Lim):
    # Override automatic tick formatter
    Step = round((Ax.get_yticks()[1]-Ax.get_yticks()[0])-0.5)
    print(Lim); print(Step)
    Ticks = np.arange(min(Lim), max(Lim)+Step, Step)

    return(Ticks)


def InchToRealSize(Size_in, ScreenDPI=96, RealDPI=142):
    Size = Size_in*RealDPI/ScreenDPI
    return(Size)


def SameScale(Axes, Axis):
    if Axis.lower() == 'x':
        Lim = [f(Ax.get_xlim()) for f in (min,max) for Ax in Axes]
        Lim = [f(Lim) for f in (min,max)]
        for Ax in Axes:
            Ax.set_xlim(Lim)
            Ax.spines['bottom'].set_bounds(Lim[0], Lim[1])

    elif Axis.lower() == 'y':
        Lim = [f(Ax.get_ylim()) for f in (min,max) for Ax in Axes]
        Lim = [f(Lim) for f in (min,max)]
        for Ax in Axes:
            Ax.set_ylim(Lim)
            Ax.spines['left'].set_bounds(Lim[0], Lim[1])

    return(None)


def Set(Backend='TkCairo', Ax=None, Fig=None, AxArgs={}, FigTitle=None, Params=False,
        HideControls=False, Tight=True):


    if Params:
        Params = {
            'backend'             : Backend,
            'image.cmap'          : 'inferno',
            # 'savefig.dpi'         : 300,
            'savefig.format'      : 'svg',
            'savefig.transparent' : True,

            'axes.titlesize'      : 10,
            'xtick.labelsize'     : 'small',
            'ytick.labelsize'     : 'small',
            'axes.spines.top'     : False,
            'axes.spines.right'   : False,
            'xtick.direction'     : 'out',
            'ytick.direction'     : 'out',
            'lines.linewidth'     : 1,

            'figure.figsize'       : FigSize,
            # 'figure.dpi'           : Screen['DPI'][0],
            'figure.subplot.wspace': 0.2,
            'figure.subplot.hspace': 0.2,

            'svg.fonttype'        : 'none',
            'pdf.fonttype'        : 42,
            'pgf.rcfonts'         : False,
            'pgf.preamble'        : '',
            'font.family'         : 'sans-serif',
            'font.serif'          : ['DejaVu Serif'],
            'font.sans-serif'     : ['DejaVu Sans'],
            'font.cursive'        : ['Zapf Chancery'],
            'font.monospace'      : ['DejaVu Sans Mono'],
            'font.size'           : 10,
            'legend.fontsize'     : 8,
        }

        return(Params)

    if Ax:
        ## General
        Ax.spines['bottom'].set_position(('outward', 2))
        Ax.spines['left'].set_position(('outward', 2))
        Ax.spines['right'].set_visible(False)
        Ax.spines['top'].set_visible(False)
        Ax.tick_params(top=False, right=False)
        Ax.patch.set_visible(False)

        if 'title' in AxArgs: Ax.set_title(AxArgs['title'])


        ## X
        if 'xlabel' in AxArgs: Ax.set_xlabel(AxArgs['xlabel'])
        if 'xlim' in AxArgs: Ax.set_xlim(AxArgs['xlim'])
        if 'xticks' in AxArgs: Ax.set_xticks(AxArgs['xticks'])
        if 'xticklabels' in AxArgs: Ax.set_xticklabels(AxArgs['xticklabels'])

        if 'xtickspacing' in AxArgs:
            import matplotlib.ticker as ticker
            Ax.xaxis.set_major_locator(ticker.MultipleLocator(AxArgs['xtickspacing']))

        if 'xbounds' in AxArgs:
            Ax.spines['bottom'].set_bounds(AxArgs['xbounds'])
        else:
            if len(Ax.get_xticks()) and len(Ax.get_xlim()):
                Lim, Ticks = Ax.get_xlim(), Ax.get_xticks()
                Bounds = [Ticks[Ticks >= Lim[0]][0],
                          Ticks[Ticks <= Lim[1]][-1]]
                Ax.spines['bottom'].set_bounds(Bounds)


        ## Y
        if 'ylabel' in AxArgs: Ax.set_ylabel(AxArgs['ylabel'])
        if 'ylim' in AxArgs: Ax.set_ylim(AxArgs['ylim'])
        if 'yticks' in AxArgs: Ax.set_yticks(AxArgs['yticks'])
        if 'yticklabels' in AxArgs: Ax.set_yticklabels(AxArgs['yticklabels'])

        if 'ytickspacing' in AxArgs:
            import matplotlib.ticker as ticker
            Ax.yaxis.set_major_locator(ticker.MultipleLocator(AxArgs['ytickspacing']))

        if 'ybounds' in AxArgs:
            Ax.spines['left'].set_bounds(AxArgs['ybounds'])
        else:
            if len(Ax.get_yticks()) and len(Ax.get_ylim()):
                Lim, Ticks = Ax.get_ylim(), Ax.get_yticks()
                Bounds = [Ticks[Ticks >= Lim[0]][0],
                          Ticks[Ticks <= Lim[1]][-1]]
                Ax.spines['left'].set_bounds(Bounds)


        ## Z
        if 'zlim' in AxArgs:
            if 'zlabel' in AxArgs: Ax.set_zlabel(AxArgs['zlabel'])
            if 'zticks' in AxArgs: Ax.set_zticks(AxArgs['zticks'])
            if 'zticklabels' in AxArgs: Ax.set_zticklabels(AxArgs['zticklabels'])
            Ax.set_zlim(min(ZLim), max(ZLim))


    if Fig:
        if FigTitle: Fig.suptitle(FigTitle)

        if HideControls:
            if Backend[:2].lower() == 'tk': Fig.canvas.toolbar.pack_forget()
            if Backend[:2].lower() == 'qt': Fig.canvas.toolbar.setVisible(False)

        if Tight:
            Fig.tight_layout()
            if FigTitle: Fig.subplots_adjust(top=0.85)

        # for Obj in Fig.findobj(): Obj.set_clip_on(False)
        Fig.patch.set_visible(False)

    return(None)


def SignificanceBar(X, Y, Text, Ax, TextArgs={}, LineArgs={}, TicksDir='down', LineTextSpacing=None):
    if TicksDir == 'down':
        from matplotlib.markers import TICKDOWN as Tick
        AmpF = LineTextSpacing if LineTextSpacing is not None else 1.02
    elif TicksDir == 'up':
        from matplotlib.markers import TICKUP as Tick
        AmpF = LineTextSpacing if LineTextSpacing is not None else 0.98
    elif TicksDir == None:
        Tick = None
        AmpF = LineTextSpacing if LineTextSpacing is not None else 1.02
    else:
        print('TicksDir should be "up", "down" or None.')
        return(None)

    TextArgsLoc = {'size': 8, 'ha': 'center', 'va': 'center'}
    LineArgsLoc = {'color': 'k'}
    TextArgsLoc = {**TextArgsLoc, **TextArgs}
    LineArgsLoc = {**LineArgsLoc, **LineArgs}

    Yy = max(Y)*AmpF
    Ax.plot(X, Y, marker=Tick, **LineArgsLoc)
    Ax.text(sum(X)/2, Yy, Text, **TextArgsLoc)
    return(None)


def SubLabels(Fig, Positions, Letters, FontArgs={'size':12, 'va': 'top'}, Color=''):
    for P,Pos in enumerate(Positions):
        if Color:
            Fig.text(Pos[0], Pos[1], Letters[P], fontdict=FontArgs, color=Color)
        else:
            Fig.text(Pos[0], Pos[1], Letters[P], fontdict=FontArgs)
    return(None)


## Level 1
Screen = GetScreenInfo()
FigSizeA4 = [8.27, 11.69]
FigSize = [InchToRealSize(FigSizeA4[0]-1.97), InchToRealSize((FigSizeA4[1]-1.97)*0.3)]


def ClickXY(Frame):
    X, Y = None, None
    Fig, Ax = plt.subplots()
    Ax.imshow(Frame, vmin=0, vmax=(2**24)-1)
    Ax.tick_params(bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    Fig.tight_layout(pad=0)
    Fig.canvas.callbacks.connect('button_press_event', ClickCallback)
    plt.show()


def Return(Function):
    if Function.lower() == 'plt':
        if 'plt' not in globals():
            Params = Set(Params=True)
            from matplotlib import rcParams; rcParams.update(Params)
            from matplotlib import pyplot as plt

            return(plt)
        else:
            return(globals()['plt'])

    elif Function.lower() == 'gridspecfromsubplotspec':
        if 'GridSpecFromSubplotSpec' not in globals():
            from matplotlib.gridspec import GridSpecFromSubplotSpec
            return(GridSpecFromSubplotSpec)
        else:
            return(globals()['GridSpec'])

    elif Function.lower() == 'gridspec':
        if 'GridSpec' not in globals():
            from matplotlib.gridspec import GridSpec
            return(GridSpec)
        else:
            return(globals()['GridSpec'])

    elif Function.lower() == 'inset_axes':
        if 'inset_axes' not in globals():
            from mpl_toolkits.axes_grid1.inset_locator import inset_axes
            return(inset_axes)
        else:
            return(globals()['inset_axes'])

    elif Function.lower() == 'triangulation':
        if 'Triangulation' not in globals():
            from matplotlib.tri import Triangulation
            return(Triangulation)
        else:
            return(globals()['Triangulation'])

    elif Function.lower() == 'axes3d':
        if 'Axes3D' not in globals():
            from mpl_toolkits.mplot3d.axes3d import Axes3D
            return(Axes3D)
        else:
            return(globals()['Axes3D'])

    elif Function.lower() == 'mpatches':
        if 'mpatches' not in globals():
            import matplotlib.patches as mpatches
            return(mpatches)
        else:
            return(globals()['mpatches'])

    elif Function.lower() == 'line2d':
        if 'Line2D' not in globals():
            from matplotlib.lines import Line2D
            return(Line2D)
        else:
            return(globals()['Line2D'])

    elif Function.lower() == 'listedcolormap':
        if 'ListedColormap' not in globals():
            from matplotlib.colors import ListedColormap
            return(ListedColormap)
        else:
            return(globals()['ListedColormap'])

    elif Function.lower() == 'animation':
        if 'Animation' not in globals():
            from matplotlib.animation import FuncAnimation as Animation
            return(Animation)
        else:
            return(globals()['Animation'])


## Level 2
def ApplyColorMapToCycle(Ax, CMap=None, Interval=None, Reverse=False):
    plt = Return('plt')
    if not CMap: CMap = plt.get_cmap()
    else: CMap = plt.get_cmap(CMap)

    if not Interval: Interval = [0,0.8]

    Lines = Ax.get_lines()
    if Reverse: Lines.reverse()
    for L,Line in enumerate(Lines):
        Line.set_color(CMap(np.linspace(Interval[0],Interval[1],len(Lines)))[L])

    return(None)


def CheckData(Data, Rate, SpaceAmpF=0.3, TimeWindow=0.2, SkipTime=10, ChLabels=[]):
    """
        Plot an animated visualization of Data.

        Parameters:
            Data: array_like
                Input 2D array, with dimensions (samples, channels).
            Rate: int
                Data's sampling rate.
            SpaceAmpF: float, optional
                Amplification factor for spacing between channels. Defaults to 0.3.
            TimeWindow: float, optional
                Amount of Data to show  at once, in seconds. Defaults to 0.2.
            SkipTime: int, optional
                Amount of samples to advance per step. Defaults to 10.
            ChLabels: list, optional
                Label of channels. If empty, channel number will be used. Defaults to [].
    """
    for C in range(Data.shape[1]): Data[:,C] /= Data[:,C].max()
    Data[:,-1] *= 0.6

    Spaces = GetSpaces(Data, SpaceAmpF)
    if not ChLabels:
        ChLabels = list(range(1, Data.shape[1]+1))

    SkipTime = int(Rate*SkipTime/1000)

    try:
        Fig, Ax = plt.subplots(figsize=(7,6))
        for S in range(0,Data.shape[0]-int(TimeWindow*Rate),SkipTime):
            t = np.arange(S, (TimeWindow*Rate)+S, 1)/Rate

            YTicks = []
            for Ch in range(Data.shape[1]):
                Y = Data[S:int(TimeWindow*Rate)+S,Ch] - Spaces[Ch]
                YTicks.append(Y.mean())
                Ax.plot(t, Y, 'k')

            XBar = [t[t.shape[0]//2], t[t.shape[0]//2+int(TimeWindow*0.2*Rate)]]
            Ax.plot(XBar, [-Spaces[-1]*1.05]*2, 'k', lw=2)

            Ax.set_yticks(YTicks)
            Ax.set_yticklabels(ChLabels)
            Ax.set_xlabel('Time [s]')
            Ax.set_ylabel('Depth [µm]')

            plt.pause(0.001)
            Ax.clear()
        plt.show()

    except KeyboardInterrupt:
        print('Stopping animation...')
        plt.close('all')
        return(None)


def FigAx(Ax, SubPlotsArgs={}):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        plt = Return('Plt')

        Fig, Ax = plt.subplots(**SubPlotsArgs)
    else:
        Fig = None

    return(Fig, Ax, ReturnAx)


def GenColorMap(RGB):
    """
    Generate colormap based on the provided RGB color.

    Parameters
    ----------
    RGB: list
        List of three values (red, green, blue) representing the desired RGB
        color. The values should be in the range 0-1 or 0-255.

    Returns
    -------
    CMap: colormap
        A colormap based on the provided RGB color.
    """
    ListedColormap = Return('ListedColormap')

    CMap = np.ones((256, 4))
    for RGBInd,RGBVal in enumerate(RGB):
        CMap[:, RGBInd] = np.linspace(1, RGBVal, 256)
    CMap = ListedColormap(CMap)

    return(CMap)


def GenLegendHandle(color='r', alpha=1, label='', hatch='', ltype='line', lw=2, marker=None):
    if ltype == 'line':
        Line2D = Return('Line2D')
        Handler = Line2D([0], [0], color=color, alpha=alpha, lw=lw, label=label, marker=marker)
    elif ltype == 'square':
        mpatches = Return('mpatches')
        Handler = mpatches.Patch(color=color, alpha=alpha, label=label, hatch=hatch)

    return(Handler)


def GetColors(Key):
    Plt = Return('Plt')
    C = {'colors': ['r', 'g', 'b', 'c', 'm', 'y', 'k']}
    C['colormaps'] = [Plt.get_cmap('Reds'), Plt.get_cmap('Greens'), Plt.get_cmap('Blues'), Plt.get_cmap('Purples'), Plt.get_cmap('Oranges'), Plt.get_cmap('Greys'), Plt.get_cmap('Blues'), Plt.get_cmap('Greens')]

    C['stimcolors'] = {
        'Sound': 'r', 'CNO': 'k',
        'Light': 'b', 'SoundLight': 'm', 'Both': 'g', 'LightMask': 'c', 'ChR2':'b', 'Arch':'g'
    }

    C['stimhatches'] = {'Light': '\\', 'Sound': '/', 'SoundLight': '-', 'Both': 'x', 'LightMask': '.', 'Light': '\\', 'Light': '\\'}

    Key = Key.lower()
    if Key not in C: print("Key must be in ['colors', 'colormaps', 'stimcolors', 'stimhatches'].")
    else: return(C[Key])


def SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show):
    if ReturnAx:
        # Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        plt = Return('plt')
        Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E)

        if Show: plt.show()
        else: plt.close()
        return(None)


def ScaleBar(
        Fig, Ax,
        ScalarMappableArgs={'cmap': 'inferno', 'vmin':0, 'vmax':1},
        ColorbarArgs={}
    ):
    plt = Return('plt')

    SM = plt.cm.ScalarMappable(
        cmap=ScalarMappableArgs['cmap'],
        norm=plt.Normalize(
            vmin=ScalarMappableArgs['vmin'],
            vmax=ScalarMappableArgs['vmax']
        )
    )
    SM._A = []

    Fig.colorbar(SM, ax=Ax, **ColorbarArgs)

    return(None)



## Level 3
def AllCh(Data, X=[], Colors=[], Labels=[], Leg=[], SpaceAmpF=1, ScaleBar=0, lw=2,
          Ax=None, AxArgs={}, File='AllCh', Ext=['svg'], Save=False, Show=True, SubPlotsArgs={}):
    if type(Data) == list: Data = np.array(Data).T
    if len(Data.shape) == 1: Data = Data.reshape((Data.shape[0],1))

    DataLen, ChNo = Data.shape
    if not len(X): X = np.arange(DataLen)
    if not len(Colors): Colors = ['k'] * ChNo
    Spaces = GetSpaces(Data) if ChNo > 1 else [0]

    Fig, Ax, ReturnAx = FigAx(Ax, SubPlotsArgs)

    YTicks = np.zeros(ChNo)
    Lines = [0] * ChNo
    for Ch in range(ChNo):
        Y = Data[:,Ch] + Spaces[Ch]*SpaceAmpF
        if ScaleBar:
            if Ch == 0: Ax.plot([X[0]]*2, [0, ScaleBar], 'k', lw=lw)
        Lines[Ch] = Ax.plot(X, Y, lw=lw)
        YTicks[Ch] = Y.mean()

        Lines[Ch][0].set_color(Colors[Ch])
        if Leg: Lines[Ch][0].set_label(Leg[Ch]); Ax.legend(loc='best')

    # AxArgs['yticks'] = YTicks
    # AxArgs['yticklabels'] = Labels if len(Labels) else 1+np.arange(ChNo)
    Ax.set_yticks(YTicks)
    Ax.set_yticklabels(Labels if len(Labels) else 1+np.arange(ChNo))
    Ax.tick_params(left=False)
    Ax.spines['left'].set_visible(False)
    Ax.spines['left'].set_position(('axes', 0))

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def BoxPlots(Data, X=[], Colors=[], LinesAmpF=1, Width=None, Means=True,
             Ax=None, AxArgs={}, File='Boxplots', Ext=['svg'], Save=False, Show=True):

    if not len(X): X = list(range(1,len(Data)+1))
    if not len(Colors): Colors = ['k']*len(Data)

    Fig, Ax, ReturnAx = FigAx(Ax)
    BoxPlot = Ax.boxplot(Data, positions=X, widths=Width, showmeans=False,
                         patch_artist=True)

    for I in range(len(BoxPlot['fliers'])):
        BoxPlot['fliers'][I].set_markeredgecolor(Colors[I])

    for I in range(len(BoxPlot['boxes'])):
        BoxPlot['boxes'][I].set(edgecolor=Colors[I], facecolor=to_rgba(Colors[I], 0.2))

    for I in range(len(BoxPlot['medians'])):
        BoxPlot['medians'][I].set(color=Colors[I])

    for K in ['whiskers', 'caps']:
        for I in range(len(BoxPlot[K])):
            BoxPlot[K][I].set(color=Colors[I//2])

    if Means:
        # in matplotlib 2.2.4 the 'showmeans' feature somehow prevents
        # inkscape from opening the resulting figure if exported to svg
        # so means have to be manually plotted
        Means = [np.mean(_) for _ in Data]
        for B,Box in enumerate(Means):
            Ax.plot(X[B], Box, color=Colors[B], marker='^')

    AxArgs = {**{'xticks': X}, **AxArgs}

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Comodulogram(Cmdlgrm, AmpFreq, PhaseFreq, CMap='inferno',
                 Ax=None, AxArgs={}, File='Comodulogram', Ext=['pdf'], Save=False, Show=True):

    if len(Cmdlgrm.shape) == 3:
        for C in range(Cmdlgrm.shape[2]):
            Comodulogram(Cmdlgrm[:,:,C], AmpFreq, PhaseFreq, CMap, Ax, AxArgs,
                         File=File+'_'+str(C), Ext=Ext, Save=Save, Show=Show)

        return(None)

    Fig, Ax, ReturnAx = FigAx(Ax)
    plt = Return('plt')

    Ax.pcolormesh(PhaseFreq, AmpFreq, Cmdlgrm)
    SM = plt.cm.ScalarMappable(cmap=CMap, norm=plt.Normalize(vmin=0, vmax=1))
    SM._A = []
    Fig.colorbar(SM, ax=Ax, label='Modulation Index')
    Ax.set_xlabel('Phase Frequency [Hz]')
    Ax.set_ylabel('Amplitude Frequency [Hz]')

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Scatter3D(
        Data, ScatterArgs={}, Elevation=30, Azimuth=-130,
        ScaleBarArgs={},
        Ax=None, AxArgs={}, File='Scatter3D', Ext=['pdf'], Save=False, Show=True
    ):
    Fig, Ax, ReturnAx = FigAx(Ax, {'subplot_kw': {'projection': '3d'}})

    ScatterDefaults = dict(c=Data[:,0], cmap='inferno', edgecolors='face', alpha=1, marker='.')
    ScatterArgs = {**ScatterDefaults, **ScatterArgs}

    Ax.scatter(Data[:,0], Data[:,1], Data[:,2], **ScatterArgs)
    Ax.view_init(Elevation, Azimuth)

    if ScaleBarArgs:
        if 'label' in ScaleBarArgs: ColorbarArgs={'label': ScaleBarArgs['label']}

        ScalarMappableArgs = {'cmap': ScatterArgs['cmap'], 'vmin':0, 'vmax':1}
        for K in ['vmin', 'vmax']:
            if K in ScaleBarArgs: ScalarMappableArgs[K] = ScaleBarArgs[K]

        ScaleBar(ScaleBarArgs['Fig'], Ax, ScalarMappableArgs, ColorbarArgs)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def ScatterMean(Data, X=[], ColorsMarkers=[], ColorsLines=[], Alpha=0.4, XSpread=0.1, YSpread=0, LogY=False,
                Marker='o', Line='--', CMap=None, Paired=False, PlotArgs={}, ErrorArgs={},
                Ax=None, AxArgs={}, File='ScatterMean', Ext=['svg'], Save=False, Show=True):

    if not len(X): X = list(range(len(Data)))

    NaN = [np.isnan(_) for _ in Data]
    if True in [True in _ for _ in NaN]:
        if Paired:
            NaNs = []
            for _ in NaN:
                NaNs = _ if len(NaNs) == 0 else NaNs + _

            Data = [_[~NaNs] for _ in Data]
        else:
            Data = [Line[~NaN[L]] for L,Line in enumerate(Data)]

    Boxes = [[np.random.uniform(V-YSpread, V+YSpread, 1)[0] for V in L] for L in Data]
    XPoss = [np.random.uniform(Pos-XSpread, Pos+XSpread, len(Boxes[P])) for P,Pos in enumerate(X)]
    Errors = [[0, np.std(Box)/len(Box)**0.5, 0] for Box in Boxes]
    Colors = [ColorsMarkers, ColorsLines]

    for C,ColorItem in enumerate(Colors):
        if not len(ColorItem):
            if not CMap: Colors[C] = ['k']*max(len(Data), len(X))
            else: Colors[C] = ['']*max(len(Data), len(X))
        elif ColorItem == 'default':
            Colors[C] = ['']*max(len(Data), len(X))

    Fig, Ax, ReturnAx = FigAx(Ax)
    for P,Pos in enumerate(X):
        Box, XPos, Error = Boxes[P], XPoss[P], Errors[P]

        if LogY:
            Ax.semilogy(
                XPos, Box, color=Colors[P], markeredgecolor=Colors[0][P],
                markerfacecolor=Colors[0][P], marker=Marker, linestyle='', alpha=Alpha
            )
        else:
            Ax.plot(
                XPos, Box, color=Colors[1][P], markeredgecolor=Colors[0][P],
                markerfacecolor=Colors[0][P], marker=Marker, linestyle='', alpha=Alpha, **PlotArgs
            )
        Ax.errorbar([Pos-XSpread, Pos, Pos+XSpread], [np.mean(Box)]*3, Error, lw=3, elinewidth=1, capsize=5, color=Colors[1][P], **ErrorArgs)

    if Paired:
        if len(np.unique([len(_) for _ in Data])) != 1:
            print('All boxes must have the same length.')
            return(None)

        for L in range(len(Boxes[0])):
            if LogY: Ax.semilogy(
                [_[L] for _ in XPoss],
                [_[L] for _ in Boxes],
                color=Colors[1][P], linestyle=Line, alpha=Alpha
            )
            else: Ax.plot(
                [_[L] for _ in XPoss],
                [_[L] for _ in Boxes],
                color=Colors[1][P], linestyle=Line, alpha=Alpha
            )

        if CMap: ApplyColorMapToCycle(Ax, CMap=CMap)

    Ax.set_xlim([X[0]-(XSpread*2), X[-1]+(XSpread*2)])
    Ax.set_xticks(X)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Spectrogram(T, F, Sxx, Colormap='inferno', Line={},
                Ax=None, AxArgs={}, File='Spectrogram', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = FigAx(Ax)

    Ax.pcolormesh(T, F, Sxx, cmap=Colormap)
    if 'xlim' not in AxArgs: AxArgs['xlim'] = [round(T[0]), round(T[-1])]
    if 'ylim' not in AxArgs: AxArgs['ylim'] = [0, max(F)]
    if 'xlabel' not in AxArgs: AxArgs['xlabel'] = 'Time [s]'
    if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Frequency [Hz]'

    Set(Ax=Ax, AxArgs=AxArgs)

    if Line:
        if 'Y' not in Line:
            print("Line['Y'] should contain plottable 1D data.")
            return(None)
        if 'X' not in Line: Line['X'] = np.arange(len(Line['Y']))
        if 'ylim' not in Line: Line['ylim'] = [min(Line['Y']), max(Line['Y'])]

        LineAx = Ax.twinx()
        LineAx.plot(Line['X'], Line['Y'], Line['Color'])
        Set(Ax=LineAx, AxArgs={k:v for k,v in Line if k not in ['X', 'Y']})

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)

