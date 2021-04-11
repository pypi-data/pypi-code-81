#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2017
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Analysis] Importing dependencies...')
import numpy as np
import os
import scipy.signal as ssig
import scipy.special as ssp
from itertools import tee
from scipy.stats.stats import pearsonr
from scipy import fftpack

from sciscripts.IO import IO
print('[Analysis.Analysis] Done.')


## Level 0
def BinSizeInc(Bins, BinSize, BinSizeNew):
    if BinSizeNew%BinSize:
        print('BinSizeNew must be multiple of BinSize.')
        return(None)

    if Bins.shape[0]%2:
        BinsNew = np.vstack((
            Bins,
            np.zeros((1,Bins.shape[1]))
        ))
    else:
        BinsNew = Bins.copy()

    BinsNew = BinsNew.reshape((
        int(BinsNew.shape[0]/int(BinSizeNew/BinSize)),
        int(BinSizeNew/BinSize),
        BinsNew.shape[1]
    )).sum(axis=1)

    if Bins.shape[0]%2: BinsNew = BinsNew[:-1,:]

    return(BinsNew)


def ChDiff(Data):
    Diff = np.zeros((Data.shape[0], Data.shape[1]-1), Data.dtype)
    for Ch in range(Diff.shape[1]):
        Diff[:,Ch] = Data[:,Ch] - Data[:,Ch-1]

    return(Diff)


def Convolve(Signal1, Signal2):
    EdgeSize = Signal2.shape[0]//2
    Edge = np.zeros(EdgeSize)
    Signal1 = np.hstack((Edge, Signal1, Edge))

    if 'complex' in str(type(Signal1[0])) or 'complex' in str(type(Signal2[0])):
        DType = 'complex'
    else:
        DType = Signal1.dtype

    Signal = np.zeros(Signal1.shape[0]-1, dtype=DType)
    for S in range(Signal1.shape[0]-Signal2.shape[0]):
        Signal1Index = np.arange(Signal2.shape[0])+S
        Signal[EdgeSize+S] = (Signal2[::-1] * Signal1[Signal1Index]).sum()

    Signal /= (Signal2**2).sum()
    return(Signal)


def Coupling(H, HMax):
    Mi = (HMax - H)/HMax
    return(Mi)


def CumulativeMA(Base, Add, ElNo):
    if len(Base) == 0:
        Base = Add
    else:
        Base = ((Base * ElNo) + Add)/(ElNo+1)

    return(Base)


def Entropy(Hist):
    Probs = Hist/np.sum(Hist)
    H = -np.sum(Probs[Probs > 0] * np.log(Probs[Probs > 0]))
    HMax = np.log(Hist.shape[0])
    return(H, HMax)


def EucDist(A, B):
    """
    Function to calculate the distance between two spatial points

    Parameters
    ----------
    A and B: list or tuple or array_like
        Iterable containing 2 elements each such as A[0] and B[0] are the
        x coord and A[1] and B[1] are the y coord.

    Returns
    -------
    Dist: float or ndarray
        Euclidean distance between points A and B.
    """
    Dist = ((A[1:] - A[:-1])**2 + (B[1:] - B[:-1])**2)**0.5
    return(Dist)


def FilterSignal(Signal, Rate, Frequency, FilterOrder=4, Coeff='butter', Type='bandpass'):
    Data = np.zeros(Signal.shape, dtype='float32')
    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            print('Filtering channel', C+1, '...')
            Data[:,C] = FilterSignal(Signal[:,C], Rate, Frequency, FilterOrder, Coeff, Type)

    else:
        if Coeff == 'butter':
            if Type not in ['bandpass', 'bandstop', 'lowpass', 'highpass']:
                print("Choose 'bandpass', 'bandstop', 'lowpass' or 'highpass'.")

            elif len(Frequency) not in [1, 2]:
                print('Frequency must have 2 elements for bandpass; or 1 element for \
                lowpass or highpass.')

            else:
                passband = [_/(Rate/2) for _ in Frequency]
                f2, f1 = ssig.butter(FilterOrder, passband, Type)
                Data = ssig.filtfilt(f2, f1, Signal, padtype='odd', padlen=0)

        elif Coeff == 'fir':
            Freqs = np.arange(1,(Rate/2)+1)
            DesiredFreqs = np.zeros(int(Rate/2))
            DesiredFreqs[min(Frequency):max(Frequency)] = 1

            o = FilterOrder + ((FilterOrder%2)*-1) +1
            a = ssig.firls(o, Freqs, DesiredFreqs, nyq=Rate/2)
            Data = ssig.filtfilt(a, 1.0, Signal, padtype='odd', padlen=0)

    return(Data)


def FixTTLs(Array, TTLsToFix):
    for TTL in TTLsToFix:
        nInd = np.random.randint(1, 100)
        while nInd == TTL: nInd = np.random.randint(0, 100)
        while nInd >= len(Array): nInd = np.random.randint(0, 100)

        print('TTL', str(TTL), 'was replaced by', str(nInd))
        Array[TTL] = Array[nInd]

    return(Array)


def GenTTLVector(TTLs, TTLLen, FullLen):
    TTLVec = np.zeros([FullLen, 1])

    for TTL in TTLs:
        TTLVec[TTL:TTL+TTLLen] = np.ones([TTLLen, 1])

    return(TTLVec)


def GenFakeTTLsRising(Rate, PulseDur, PauseBefore, PauseAfter, SampleStart, PulseNo):
    BlockDur = PauseBefore+PulseDur+PauseAfter
    # FakeTTLs = [int(((PauseBefore)+(_*BlockDur))*Rate)+SampleStart for _ in range(PulseNo)]
    FakeTTLs = np.arange(SampleStart, SampleStart+(BlockDur*Rate*PulseNo), BlockDur*Rate, dtype='int')
    return(FakeTTLs)


def GetFxx(Rate, NFFT, FreqWindow):
    """
    Based on Chronux's getfgrid @ http://chronux.org/
    Returns the frequencies associated with a given FFT-based computation

    Parameters
    ----------
    Rate: int
        Sampling rate.
    NFFT: int
        Nuber of FFT points.
    FreqWindow: list or array
        List with the lowest and highest frequency to be calculated in Hz.

    Returns
    -------
    Fxx: array
        Frequencies to be returned in an FFT-based computation.

    """
    Fxx = np.arange(0, Rate/NFFT, Rate)
    Fxx = Fxx[:NFFT]
    Freqs = np.where((Fxx >= FreqWindow[0]) * (Fxx <= FreqWindow[-1]))[0]
    Fxx = Fxx[Freqs]

    return(Fxx)


def GetAmpEnv(Signal):
    if len(Signal.shape) > 1:
        Data = np.zeros(Signal.shape, 'float32')
        for C in range(Data.shape[1]):
            print(f'Processing ch {C+1}...')
            Data[:,C] = GetAmpEnv(Signal[:,C])

    else:
        Mean = Signal.mean(axis=0)
        # Orders faster when signal size is a power of two, so padding and truncating
        Data = ssig.hilbert(Signal-Mean, fftpack.next_fast_len(len(Signal)))[:len(Signal)]
        Data = abs(Data)
        Data += Mean

    return(Data)


def GetEventEdges(EventsDict, Ch, Proc, Rec, Edge='rise'):
    if Edge.lower() == 'rise': Id = 1
    elif Edge.lower() == 'fall': Id = 0
    else: print('Edge should be "rise" or "fall"')

    Events = EventsDict['sampleNum'][(EventsDict['channel'] == Ch) *
                                     (EventsDict['recordingNumber'] == Rec) *
                                     (EventsDict['nodeId'] == Proc) *
                                     (EventsDict['eventId'] == Id) *
                                     (EventsDict['eventType'] == 3)]

    return(Events)


def GetNegEquiv(Number):
    """
    Return the negative equivalent of a percentage, for calculating differences.
    The equivalent decrease of an increase of:
        - 100% is -50%;
        - 300% is -75%;
        - 400% is -80%;

    and so on. The increase can go up to infinity, but the decrease
    can only go down to -100%. In other words, this function maps values that
    range from 0 to inf into 0 to -100.

    Parameters
    ----------
    Number: int or float
        Number in the range 0-inf. If Number is < 0, it will be returned
        unmodified.

    Returns
    -------
    NumberNeg: int or float
        The representation of Number into the range 0 to -100.

    """
    NumberNeg = Number if Number < 0 else -(100-(100/((Number+100)/100)))
    return(NumberNeg)


def GetPeaks(Signal, Std=1, FixedThreshold=None):
    if len(Signal.shape) == 2:
        Peaks = {'Pos':[], 'Neg':[]}
        for Ch in range(Signal.shape[1]):
            PeaksCh = GetPeaks(Signal[:,Ch], Std, FixedThreshold)
            for K in Peaks.keys(): Peaks[K].append(PeaksCh[K])

    else:
        if FixedThreshold: Threshold = FixedThreshold
        else: Threshold = Std*Signal.std()

        if Threshold:
            ThresholdPos = Signal.mean()+Threshold
            ThresholdNeg = Signal.mean()-Threshold
            Peaks = {
                'Pos': np.where((Signal[1:-1] > ThresholdPos) *
                                (Signal[:-2] < Signal[1:-1]) *
                                (Signal[1:-1] >= Signal[2:]))[0]+1,
                'Neg': np.where((Signal[1:-1] < ThresholdNeg) *
                                (Signal[:-2] > Signal[1:-1]) *
                                (Signal[1:-1] <= Signal[2:]))[0]+1
            }
        else:
            Peaks = {
                'Pos': np.where((Signal[:-2] < Signal[1:-1]) *
                                (Signal[1:-1] >= Signal[2:]))[0]+1,
                'Neg': np.where((Signal[:-2] > Signal[1:-1]) *
                                (Signal[1:-1] <= Signal[2:]))[0]+1
            }

    return(Peaks)


def GetPhase(Signal):
    if len(Signal.shape) > 1:
        Data = np.zeros(Signal.shape)
        for C in range(Data.shape[1]):
            print(f'Processing ch {C+1}...')
            Data[:,C] = GetPhase(Signal[:,C])

    else:
        # Orders faster when signal size is a power of two, so padding and truncating
        Data = ssig.hilbert(Signal, fftpack.next_fast_len(len(Signal)))[:len(Signal)]
        Data = np.angle(Data)

    return(Data)


def GetPowerOf2(N):
    Next = int(np.ceil(np.log2(N)))
    return(Next)


def GetRecXValues(TTLs, Rate, TimeBeforeTTL, TimeAfterTTL):
    NoOfSamplesBefore = int((TimeBeforeTTL*Rate) * 10**-3)
    NoOfSamplesAfter = int((TimeAfterTTL*Rate) * 10**-3)
    NoOfSamples = NoOfSamplesBefore + NoOfSamplesAfter
    XValues = (range(-NoOfSamplesBefore,
                     NoOfSamples-NoOfSamplesBefore)/Rate) * 10**3

    return(XValues)


def GetTTLInfo(Events, EventRec, TTLCh):
    print('Get TTL data...')
    EventID = Events['TTLs']['user_data']['eventID']
    EventCh = Events['TTLs']['user_data']['event_channels']
    EventSample = Events['TTLs']['time_samples']

    TTLRecs = np.nonzero(np.bincount(EventRec))[0]
    TTLRecs = ["{0:02d}".format(_) for _ in TTLRecs]
    TTLsPerRec = {Rec: [EventSample[_] for _ in range(len(EventRec))
                         if EventRec[_] == int(Rec)
                         and EventCh[_] == TTLCh-1
                         and EventID[_] == 1]
                  for Rec in TTLRecs}

    return(TTLsPerRec)


def GetTTLThreshold(TTLCh, StdNo=3):
    if not StdNo: StdNo = 3
    Threshold = np.mean(TTLCh) + StdNo*(np.std(TTLCh))
    return(Threshold)


def IsInt(Obj):
    try: int(Obj); return(True)
    except: return(False)


def IsFloat(Obj):
    try: float(Obj); return(True)
    except: return(False)


def Morlet(Freq, t, CyclesNo=5, FreqScalingFactor=1, Offset=0):
    SigmaT = CyclesNo/(2*np.pi*Freq)

    Gaussian = np.exp((-((t-Offset)/FreqScalingFactor)**2)/(2*SigmaT**2))
    CosSen = np.exp(1j * 2 * np.pi * Freq/FreqScalingFactor * (t-Offset))
    Psi = FreqScalingFactor * Gaussian * CosSen

    return(Psi)


def NestedClean(Nest):
    if 'numpy' in str(type(Nest)):
        if not Nest.size: return(None)
        else: return(Nest)
    else:
        if len(Nest) == 0: return(None)

    ToDel = []
    if type(Nest) == dict:
        for K, Key in Nest.items():
            Nest[K] = NestedClean(Key)

            if type(Nest[K]) == np.ndarray:
                if not Nest[K].size: ToDel.append(K)
            else:
                if not Nest[K]: ToDel.append(K)

        for K in ToDel: del(Nest[K])
        return(Nest)

    elif type(Nest) in [list, tuple]:
        for E, El in enumerate(Nest):
            Nest[E] = NestedClean(El)

            if type(Nest[E]) == np.ndarray:
                if not Nest[E].size: ToDel.append(E)
            else:
                if not Nest[E]: ToDel.append(E)

        for E in ToDel: del(Nest[E])
        return(Nest)

    else:
        return(Nest)


def Normalize(Data):
    Norm = Data.astype('float32')

    if len(Norm.shape) == 2:
        for Ch in range(Norm.shape[1]):
            Norm[:,Ch] = Normalize(Norm[:,Ch])

    elif len(Norm.shape) == 1:
        Norm /= abs(Norm).max()

    else:
        print('Only 1 or 2 dimensions allowed.')
        return(None)

    return(Norm)


def Pairwise(iterable):
    """
    Taken from https://docs.python.org/3.6/library/itertools.html#itertools-recipes
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def PolygonArea(X,Y):
    """
    Calculate the area of a polygon based on lists of x and y coordinates.

    Parameters:
        X and Y: lists or tuples or array_like
            Iterable containing x and y coordinates, respectively, of the
            vertices of the polygon.
    Returns:
        Area: float
            Area of the polygon defined by the vertices at the provided
            coordinates.

    Author: Madhi
    Source: https://stackoverflow.com/a/30408825
    """
    Area = 0.5 * np.abs(np.dot(X, np.roll(Y,1)) - np.dot(Y, np.roll(X,1)))
    return(Area)


def RemapChannels(Tip, Head, Connector):
    """
    Get probe channels order. It doesn't matter what logic you follow to order
    your connector channels, but you MUST follow the same logic for your probe
    head.

    If the probe tip channels are put top-down or bottom-up, the resulting
    channel map will be ordered accordingly.

    Example:
        # A16 probe connected to A16OM16 adaptor
        A16OM16 = [13, 12, 14, 11, 15, 10, 16, 9, 5, 4, 6, 3, 7, 2, 8, 1]
        A16 = {'Tip': [9, 8, 10, 7, 13, 4, 12, 5, 15, 2, 16, 1, 14, 3, 11, 6],
               'Head': [8, 7, 6, 5, 4, 3, 2, 1, 9, 10, 11, 12, 13, 14, 15, 16]}

        ChannelMap = RemapChannels(A16['Tip'], A16['Head'], A16OM16)
    """
    print('Get channel order... ', end='')
    ChNo = len(Tip)
    ChMap = [0]*ChNo

    for Ch in range(ChNo):
        TipCh = Tip[Ch] # What channel should be the Ch
        HeadCh = Head.index(TipCh) # Where Ch is in Head
        ChMap[Ch] = Connector[HeadCh] # Channels in depth order

    print('Done.')
    return(ChMap)


def RMS(Data):
    if len(Data.shape) == 2:
        DataRMS = np.empty(Data.shape[1])
        for C in range(Data.shape[1]): DataRMS[C] = RMS(Data[:,C])
    else:
        DataRMS = np.mean(Data**2)**0.5

    return(DataRMS)


def StrRange(Start='a', End='z', Step=1):
    if max(len(Start), len(End)) > 1:
        print('Only 1-char length strings are accepted.')
        return(None)
    else:
        Range = map(chr, range(ord(Start), ord(End), Step))
        return(Range)


def SubSample(Data, Rate, NewRate, t=[]):
    SubSampleF = int(Rate/NewRate)
    if len(Data.shape) > 1:
        Data = Data[np.arange(0,Data.shape[0],SubSampleF), :]
    else:
        Data = Data[np.arange(0,Data.shape[0],SubSampleF)]

    if len(t): t = t[np.arange(0,t.shape[0],SubSampleF)]

    if len(t): return(Data, t)
    else: return(Data)


def Upsample2d(Data, Dim1, Dim2, Up):
    """
    Upsample a 2-dimensional array.

    Parameters
    ----------
    Data: 2d array
        Array of shape (Dim1.shape[0], Dim2.shape[0]) containing the values.

    Dim1: 1d array
        Array of shape (Data.shape[0],) representing the 1st dimension.

    Dim2: 1d array
        Array of shape (Data.shape[1],) representing the 2nd dimension.

    Up: int, list
        How many times should the dimensions be upsampled. If int, the value is
        applied for both dimensions. If list, the values are applied to the
        dimensions, respectively.

    Returns
    -------
    DataUp: 2d array
        The upsampled array.

    Dim1Up: 1d array
        The upsampled array for the 1st dimension.

    Dim2Up: 1d array
        The upsampled array for the 2nd dimension.

    Example
    -------
    To upsample a spectrogram 5x in both dimension:
        SxxUp, FUp, TUp = SxxUpsample(Sxx, F, T, 5)
    """
    DimsUp = [
        np.interp(
            np.linspace(0,1,len(Dim)*Up),
            np.linspace(0,1,len(Dim)),
            Dim
        )
        for Dim in [Dim1, Dim2]
    ]

    Data1Up = np.zeros((len(Dim1),len(DimsUp[1])), dtype='float32')
    for I in range(Data.shape[0]):
        Data1Up[I,:] = np.interp(
            np.linspace(0,1,Data1Up.shape[1]),
            np.linspace(0,1,Data.shape[1]),
            Data[I,:]
        )

    DataUp = np.zeros((len(DimsUp[0]),len(DimsUp[1])), dtype='float32')
    for F in range(Data1Up.shape[1]):
        DataUp[:,F] = np.interp(
            np.linspace(0,1,len(DimsUp[0])),
            np.linspace(0,1,Data1Up.shape[0]),
            Data1Up[:,F]
        )

    return(DataUp, DimsUp[0], DimsUp[1])


def UniqueStr(List, KeepOrder=False):
    """ Better alternative: numpy.unique(List) """
    if KeepOrder:
        used = set()
        UniqueList = [x for x in List if x not in used and (used.add(x) or True)]
    else:
        UniqueList = set(List); UniqueList = sorted(list(UniqueList))

    return(UniqueList)


def VonMises(Phi, PhiMean, Kappa):
    VM = np.exp(Kappa * (np.cos(Phi - PhiMean)))
    VM /= 2 * np.pi * ssp.iv(0, Kappa)
    return(VM)


def WhereMultiple(Test, Data):
    """ Return indexes of elements in Test at Data.
        Values in Test must be unique.

        Parameters:
            Test: array_like
                Input array with values to be found on Data. Elements must be unique.
            Data: array_like
                The values against which to find each value of Test.

        Returns:
            I: ndarray, int
                Indices of the values from Test in Data.

        Taken from Divakar @ https://stackoverflow.com/a/33678576
    """
    I = np.nonzero(Test[:,None] == Data)[1]
    return(I)


## Level 1
def ComodulationPhaseAmp(Data, Rate, PhaseFreqBand, PhaseFreqBandWidth, PhaseFreqBandStep, AmpFreqBand, AmpFreqBandWidth, AmpFreqBandStep, FilterOrder=2, File='ComodulogramPhaseAmp', Save=False):
    """ Calculate how strongly Phase of one frequency band modulates amplitude of another. """
    PhaseFreq = np.arange(PhaseFreqBand[0], PhaseFreqBand[1], PhaseFreqBandStep)
    AmpFreq = np.arange(AmpFreqBand[0], AmpFreqBand[1], AmpFreqBandStep)

    if len(Data.shape) == 2:
        Comodulogram = np.empty((len(AmpFreq), len(PhaseFreq), Data.shape[1]))
        for C in range(Data.shape[1]):
            print(f'=== [Ch {C+1}] ===')
            Comodulogram[:,:,C] = ComodulationPhaseAmp(Data[:,C], Rate, PhaseFreqBand, PhaseFreqBandWidth, PhaseFreqBandStep, AmpFreqBand, AmpFreqBandWidth, AmpFreqBandStep, FilterOrder, Save=False)[0]

    else:
        Phases = np.arange(-180,161,20)
        MeanAmp = np.empty(len(Phases))
        Comodulogram = np.empty((len(AmpFreq), len(PhaseFreq)))

        Func = [GetPhase, GetAmpEnv]

        print('Getting phase and amp. env. for each frequency band...', end=' ')
        PhaseAmp = [
            [
                Func[A](
                    FilterSignal(Data, Rate, [_, _+Band], FilterOrder)
                )
                for _ in AF
            ]
            for A, (AF,Band) in enumerate([
                [PhaseFreq, PhaseFreqBandWidth],
                [AmpFreq, AmpFreqBandWidth]
            ])
        ]
        print('Done')

        for PhF,PhaseF in enumerate(PhaseFreq):
            for AF,AmpF in enumerate(AmpFreq):
                print(f'    [Phase {PhaseF}-{PhaseF+PhaseFreqBandWidth}] [Amp {AmpF}-{AmpF+AmpFreqBandWidth}]')

                for P,Ph in enumerate(Phases):
                    I = (np.rad2deg(PhaseAmp[0][PhF])>Ph)*(np.rad2deg(PhaseAmp[0][PhF])<(Ph+20))
                    MeanAmp[P] = np.mean(PhaseAmp[1][AF][I])

                p = MeanAmp/sum(MeanAmp)
                MI = (np.log(len(p))+sum(p[p>0]*np.log(p[p>0])))/np.log(len(p))
                Comodulogram[AF,PhF] = MI

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        IO.Bin.Write(Comodulogram, File+'.dat')
        IO.Bin.Write(AmpFreq, File+'_AmpFreq.dat')
        IO.Bin.Write(PhaseFreq, File+'_PhaseFreq.dat')

    return(Comodulogram, AmpFreq, PhaseFreq)


def ComodulationAmpAmp(Data, Rate, AmpFreqBand1, AmpFreqBandWidth1, AmpFreqBandStep1, AmpFreqBand2, AmpFreqBandWidth2, AmpFreqBandStep2, FilterOrder=2, File='ComodulogramAmpAmp', Save=False):
    """ Calculate how strongly amplitude of one frequency band modulates amplitude of another. """
    AmpFreq1 = np.arange(AmpFreqBand1[0], AmpFreqBand1[1], AmpFreqBandStep1)
    AmpFreq2 = np.arange(AmpFreqBand2[0], AmpFreqBand2[1], AmpFreqBandStep2)

    if len(Data.shape) == 2:
        Comodulogram = np.empty((len(AmpFreq1), len(AmpFreq2), Data.shape[1]))
        for C in range(Data.shape[1]):
            print(f'=== [Ch {C+1}] ===')
            Comodulogram[:,:,C] = ComodulationAmpAmp(Data[:,C], Rate, AmpFreqBand1, AmpFreqBandWidth1, AmpFreqBandStep1, AmpFreqBand2, AmpFreqBandWidth2, AmpFreqBandStep2, FilterOrder, Save=False)[0]

    else:
        Comodulogram = np.empty((len(AmpFreq1), len(AmpFreq2)))

        print('Getting amp. env. for each frequency band...', end=' ')
        Amp = [
            [
                GetAmpEnv(
                    FilterSignal(Data, Rate, [_, _+Band], FilterOrder)
                )
                for _ in AF
            ]
            for AF,Band in [
                [AmpFreq1, AmpFreqBandWidth1],
                [AmpFreq2, AmpFreqBandWidth2]
            ]
        ]
        print('Done')

        for AF1,AmpF1 in enumerate(AmpFreq1):
            for AF2,AmpF2 in enumerate(AmpFreq2):
                print(f'    [Amp {AmpF1}-{AmpF1+AmpFreqBandWidth1}] [Amp {AmpF2}-{AmpF2+AmpFreqBandWidth2}]')
                r,p = pearsonr(Amp[0][AF1], Amp[1][AF2])
                Comodulogram[AF1,AF2] = r

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        IO.Bin.Write(Comodulogram, File+'.dat')
        IO.Bin.Write(AmpFreq1, File+'_AmpFreq1.dat')
        IO.Bin.Write(AmpFreq2, File+'_AmpFreq2.dat')

    return(Comodulogram, AmpFreq1, AmpFreq2)



def CWT(Signal, t, Rate, Freqs, tPsi, Wavelet=Morlet, WaveletArgs=dict(CyclesNo=5, FreqScalingFactor=1, Offset=0)):
    Signal_Psi = np.zeros((Freqs.shape[0], t.shape[0]), dtype='complex')
    if 't' not in WaveletArgs: WaveletArgs['t'] = tPsi

    for F,Freq in enumerate(Freqs):
        WaveletArgs['Freq'] = Freq
        Psi = Wavelet(WaveletArgs)
        Signal_Psi[F,:] = np.convolve(Signal, Psi, 'same')

    return(Signal_Psi)


def GetDeltaPhase(SignalRef, SignalResult):
    if len(SignalRef.shape) > 1:
        if SignalRef.shape[1] != SignalResult.shape[1]:
            print('Ref and Result dimensions have to be the same.')
            return(None)

        DeltaPhase = np.zeros(SignalRef.shape)
        for C in range(DeltaPhase.shape[1]):
            DeltaPhase[:,C] = GetDeltaPhase(SignalRef[:,C], SignalResult[:,C])

    else:
        PhaseRef = GetPhase(SignalRef)
        PhaseResult = GetPhase(SignalResult)
        DeltaPhase = np.angle(np.exp(1j * (PhaseRef - PhaseResult)))

    return(DeltaPhase)


def GetEntropyMI(Hist):
    H = Entropy(Hist)[0]
    Probs = Hist/np.sum(Hist)
    MI = (np.log(Probs.shape[0])-H)/np.log(Probs.shape[0])
    return(MI)


def GetInstFreq(Signal, Rate):
    if len(Signal.shape) == 2:

        InstFreq = np.zeros((Signal.shape[0]-1, Signal.shape[1]))
        for C in range(Signal.shape[1]):
            InstFreq[:,C] = GetInstFreq(Signal[:,C], Rate)

    else:
        SignalPhase = GetPhase(Signal)

        # Instantaneous frequency can be achieved by
        # InstFreq = np.angle(np.exp(1j*np.diff(SignalPhase)))/(2*np.pi/Rate)
        # Or by unwrapping the signal
        SignalPhaseUnwrapped = np.unwrap(SignalPhase)
        InstFreq = np.diff(SignalPhaseUnwrapped)/(2*np.pi/Rate)

    return(InstFreq)


def GetNFFT(WindowSize, Pad=0):
    NFFT = int(2**(GetPowerOf2(WindowSize)+Pad))
    return(NFFT)


def GetPLVs(SignalRef, SignalResult, Rate, Freqs, FreqBand):
    if len(SignalRef.shape) > 1:
        if SignalRef.shape[1] != SignalResult.shape[1]:
            print('Ref and Result dimensions have to be the same.')
            return(None)

        PLVs = np.zeros((Freqs.shape[0], SignalRef.shape[1]), dtype='float32')
        for C in range(PLVs.shape[1]):
            PLVs[:,C] = GetPLVs(SignalRef[:,C], SignalResult[:,C], Rate, Freqs, FreqBand)

    else:
        PLVs = np.zeros((Freqs.shape[0]), dtype='float32')
        for F,Freq in enumerate(Freqs):
            SignalFilteredRef = FilterSignal(SignalRef, Rate, [Freq, Freq+FreqBand])
            SignalFilteredResult = FilterSignal(SignalResult, Rate, [Freq, Freq+FreqBand])
            DP = GetDeltaPhase(SignalFilteredRef, SignalFilteredResult)
            PLVs[F] = np.abs(np.mean(np.exp(1j * DP)))

    return(PLVs)


def GetStrongestCh(Data):
    BestCh = RMS(Data).argmax()
    return(BestCh)


def PSD(Signal, Rate, Scaling='density', WindowSize=None, NPerSeg=None, NOverlap=None):
    if not WindowSize: WindowSize = len(Signal)
    if not NPerSeg: NPerSeg = WindowSize//2
    if not NOverlap: NOverlap = WindowSize//4

    F, PxxSp = [], []

    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            print('PSD of channel', C+1, '...')
            f, pxx = PSD(Signal[:,C], Rate, Scaling, WindowSize, NPerSeg, NOverlap)

            if not len(F):
                F = np.zeros((len(pxx), Signal.shape[1]), dtype='float')
                PxxSp = F.copy()

            F[:,C], PxxSp[:,C] = f, pxx

    else:
        NFFT = GetNFFT(WindowSize)
        F, PxxSp = ssig.welch(Signal, Rate, nperseg=WindowSize//2,
                                noverlap=WindowSize//4, nfft=NFFT, detrend=False)

    return(F, PxxSp)


def QuantifyTTLsPerRec(AnalogTTLs, Data=[], StdNo=2.5, EventsDict={}, TTLCh=None,
                       Proc=None, Rec=None, Edge='rise'):
    print('Get TTL timestamps... ', end='')
    if AnalogTTLs:
        Threshold = GetTTLThreshold(Data, StdNo); print('TTL threshold:', Threshold)

        if Edge == 'rise':
            TTLs = np.where((Data[:-1] < Threshold)*(Data[1:] > Threshold))[0]
        elif Edge == 'fall':
            TTLs = np.where((Data[:-1] > Threshold)*(Data[1:] < Threshold))[0]
        else:
            print('"Edge" should be "rise" of "fall".')
            return(None)

    else:
        TTLs = GetEventEdges(EventsDict, TTLCh, Proc, Rec, Edge='rise')

    print('Done.')
    return(TTLs)


def RemapCh(Probe, Adaptor):
    Probes = {
        'A16': {'Tip': [9, 8, 10, 7, 13, 4, 12, 5, 15, 2, 16, 1, 14, 3, 11, 6],
                'Head': [8, 7, 6, 5, 4, 3, 2, 1, 9, 10, 11, 12, 13, 14, 15, 16]},
        'CM16': {'Tip': [9, 8, 10, 7, 11, 6, 12, 5, 13, 4, 14, 3, 15, 2, 16, 1],
                 'Head': [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 13, 14, 15, 16]},
        'Ciralli': {'Tip': [12, 11, 10, 9, 8, 7, 6, 5, 13, 14, 15, 16, 1, 2, 3, 4],
                    'Head': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]}
    }

    Adaptors = {
        'CustomAdaptor': [5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 1, 2, 3, 4],
        'RHAHeadstage': [16, 15, 14, 13, 12, 11, 10, 9, 1, 2, 3, 4, 5, 6, 7, 8],
        'RHAOM': [12, 11, 10, 9, 8, 7, 6, 5, 13, 14, 15, 16, 1, 2, 3, 4],
        'A16OM16': [13, 12, 14, 11, 15, 10, 16, 9, 5, 4, 6, 3, 7, 2, 8, 1],
        'None16': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }

    if Probe not in Probes or Adaptor not in Adaptors:
        print('Unknown probe and/or adaptor.')
        print('Known probes:')
        for P in Probes.keys(): print('    ' + P)
        print('Known adaptors:')
        for A in Adaptors.keys(): print('    ' + A)
        return(None)

    Map = RemapChannels(Probes[Probe]['Tip'], Probes[Probe]['Head'], Adaptors[Adaptor])
    return(Map)


def SignalIntensity(Signal, Rate, FreqBand, Ref, NoiseRMS=None, WindowSize=None):
    Intensity = {}; IntensityPSD = {}

    F, PxxSp = PSD(Signal, Rate, WindowSize=WindowSize)
    Range = (F > FreqBand[0])*(F < FreqBand[1])
    BinSize = F[1] - F[0]

    PxxRMS = (sum(PxxSp[Range]) * BinSize)**0.5
    if NoiseRMS: PxxRMS = PxxRMS - NoiseRMS

    dB = 20*(np.log10((PxxRMS/Ref)/2e-5))

    IntensityPSD['F'] = F
    IntensityPSD['PxxSp'] = PxxSp
    Intensity['RMS'] = PxxRMS
    Intensity['dB'] = dB

    return(Intensity, IntensityPSD)


def SliceData(Signal, TTLs, NoOfSamplesBefore, NoOfSamplesAfter):
    NoOfSamples = NoOfSamplesBefore+NoOfSamplesAfter
    Array = np.zeros((NoOfSamples, len(TTLs)))

    for T, TTL in enumerate(TTLs):
        Start = TTL-NoOfSamplesBefore
        End = TTL+NoOfSamplesAfter

        if Start < 0 or End > len(Signal):
            print('TTL too close to the edge. Skipping...')
            continue

        Array[:,T] = Signal[Start:End]

    return(Array)


def Spectrogram(Signal, Rate, WindowSize=None, Overlap=None, NFFT=None, Window='hann'):
    if not WindowSize: WindowSize = len(Signal)//2
    if not Overlap: Overlap = WindowSize//2
    if not NFFT: NFFT = GetNFFT(WindowSize)

    F, T, Sxx = [], [], []

    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            print('Spectrogram of channel', C+1, '...')
            f, t, sxx = Spectrogram(
                Signal[:,C], Rate, WindowSize, Overlap, NFFT, Window
            )

            if not len(F):
                F = f
                T = t
                Sxx = np.zeros((sxx.shape[0], sxx.shape[1], Signal.shape[1]), dtype='float')

            Sxx[:,:,C] = sxx

    else:
        F, T, Sxx = ssig.spectrogram(
            Signal, Rate, axis=0, nperseg=WindowSize,
            noverlap=Overlap, nfft=NFFT, detrend=False, window=Window
        )

    return(F, T, Sxx)


