#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[IO.SigGen] Importing dependencies...')
import numpy as np
from scipy import signal

from sciscripts.Analysis.Analysis import FilterSignal
print('[IO.SigGen] Done.')

SoundTTLVal = 0.1; LaserTTLVal = 1

def FreqStr2Int(Freq):
    Freq = Freq.split('-')
    IntFreq = sum([float(_) for _ in Freq])/len(Freq)
    return(IntFreq)


def ApplyRamp(Signal, Rate, RampRiseDur, RampFallDur, Mode='linear'):
    Ramp = np.ones((Rate*len(Signal)), dtype=np.float32)
    Ramp[:Rate*RampRiseDur] = np.linspace(0, 1, Rate*RampRiseDur)
    Ramp[-Rate*RampRiseDur:] = np.linspace(1, 0, Rate*RampRiseDur)

    Signal *= Ramp
    return(Signal)


## Level 0
def ApplySoundAmpF(SoundPulseFiltered, Rate, SoundAmpF, NoiseFrequency,
                   SoundPauseBeforePulseDur=0, SoundPauseAfterPulseDur=0):
    """Returns an array of dimensions [Data, AmpF, Freq]."""

    print('Applying amplification factors...')
    # Preallocating memory
    TotalDur = round(Rate * (SoundPauseBeforePulseDur+SoundPauseAfterPulseDur))+SoundPulseFiltered.shape[0]
    if type(NoiseFrequency[0]) == list:
        Freqs = ['-'.join([str(_) for _ in F]) for F in NoiseFrequency]
    else:
        Freqs = [str(F) for F in NoiseFrequency]

    Start = int(round(SoundPauseBeforePulseDur*Rate))
    End = -int(round(SoundPauseAfterPulseDur*Rate))
    if End == 0: End = TotalDur

    SoundUnit = np.zeros((TotalDur, len(SoundAmpF[list(SoundAmpF)[0]]), len(Freqs)), dtype='float32')

    for F,Freq in enumerate(Freqs):
        if Freq not in SoundAmpF:
            # FAmpF = SoundAmpF[list(SoundAmpF)[0]]
            # Estimate closest calibrated frequency
            IntFreq = [[F,F] for F in SoundAmpF.keys()]
            IntFreq = list(map(list, zip(*IntFreq)))

            IntFreq[1] = [FreqStr2Int(Freq) for Freq in IntFreq[1]]

            RealFKey = FreqStr2Int(FKey)
            RealFKey = min(IntFreq[1], key=lambda x:abs(x-RealFKey))
            RealFKey = IntFreq[0][IntFreq[1].index(RealFKey)]

            FAmpF = SoundAmpF[RealFKey]
            # print('FKey:', RealFKey)
        else:
            FAmpF = SoundAmpF[Freq]
            # print('FKey:', FKey)

        for A,AmpF in enumerate(FAmpF):
            SoundUnit[Start:End,A,F] = SoundPulseFiltered[:,F] * AmpF

    return(SoundUnit)


def BandpassFilterSound(SoundPulse, Rate, NoiseFrequency):
    """Returns an array of dimensions [Data,Freq]."""

    # Preallocating memory
    SoundPulseFiltered = np.zeros((SoundPulse.shape[0], len(NoiseFrequency)),
                                  dtype=SoundPulse.dtype)
    # Freqs = ['-'.join([str(_) for _ in F]) for F in NoiseFrequency]
    PulseAmp = (max(SoundPulse)-min(SoundPulse))/2

    print('Filtering sound: ', end='')
    for F, Freq in enumerate(NoiseFrequency):
        print('-'.join([str(_) for _ in Freq]), end='...')

        SoundPulseFiltered[:,F] = FilterSignal(SoundPulse, Rate, Freq)
        SoundPulseFiltered[:,F] = SoundPulseFiltered[:,F].astype('float32')
        PulseFilteredAmp = (max(SoundPulseFiltered[:,F])-min(SoundPulseFiltered[:,F]))/2
        FilterAmpF = PulseAmp/PulseFilteredAmp
        SoundPulseFiltered[:,F] = SoundPulseFiltered[:,F]*FilterAmpF
        SoundPulseFiltered[:,F][-1] = 0

    print(end='\n')
    return(SoundPulseFiltered)


def Noise(Rate, SoundPulseDur):
    print('Generating noise...')
    Noise = np.random.uniform(-1, 1, size=round(Rate*SoundPulseDur))
    Noise[-1] = 0
    Noise = np.array(Noise, dtype=np.float32)

    return(Noise)


def SineWave(Rate, Freq, AmpF, Time):
    """
    Generates a single tone or a polynomial tone.
    Example of an ascending tone:
        Freq = [800, 1600]
        Freq = [(Freq[1] - Freq[0])/Time, Freq[0]]
        Time = np.linspace(0, Time, int(Rate*Time))
        Sine = SineWave(48000, Freq, 1, Time)
    """
    print('Generating sine wave...')

    if type(Freq) in [int, float]:
        ## Ensure that there will be a sample at each peak
        P = 1/(Freq*4)
        TimeShift = (P*Rate) - int(P*Rate)
        Shift = 2 * np.pi * Freq * TimeShift/Rate

        Pulse = np.sin((2 * np.pi * Freq * np.arange(Time*Rate)/Rate) - Shift) * AmpF

    else:
        Pulse = signal.sweep_poly(Time, Freq)

    Pulse = Pulse.astype('float32')
    Pulse[-1] = 0

    return(Pulse)


def TTLSqPulse(Rate, PulseDur, TTLAmpF, TTLVal, PauseBeforePulseDur=0,
           PauseAfterPulseDur=0):
    Pulse = np.concatenate([
                np.zeros(PauseBeforePulseDur*Rate, dtype=np.float32),
                np.ones(PulseDur*Rate, dtype=np.float32) * TTLAmpF * TTLVal,
                np.zeros(PauseAfterPulseDur*Rate, dtype=np.float32)])

    return(Pulse)


def SqWave(Rate, PulseDur, TTLAmpF, TTLVal, PauseBeforePulseDur=0,
           PauseAfterPulseDur=0):

    print('Generating Sound TTL...')
    TTLSpace = PulseDur + PauseAfterPulseDur
    if TTLSpace < 2*PulseDur:
        TTLPulse = np.concatenate([
                  np.array([TTLVal] * round(Rate*PulseDur/2), dtype=np.float32),
                  np.array([TTLVal*-1] * round(Rate*PulseDur/2), dtype=np.float32)
                  ])
    else:
        TTLPulse = np.concatenate([
                  np.array([TTLVal] * round(Rate*PulseDur), dtype=np.float32),
                  np.array([TTLVal*-1] * round(Rate*PulseDur), dtype=np.float32)
                  ])

    TTLPulse[-1] = 0

    if PauseBeforePulseDur == 0:
        if PauseAfterPulseDur == 0:
            TTLUnit = TTLPulse
        else:
            TTLPauseAfterPulse = np.zeros(round((PauseAfterPulseDur-PulseDur) * Rate),
                            dtype=np.float32)
            TTLUnit = np.concatenate([TTLPulse, TTLPauseAfterPulse])
    else:
        TTLPauseBeforePulse = np.zeros(round(PauseBeforePulseDur * Rate), dtype=np.float32)
        if PauseAfterPulseDur == 0:
            TTLUnit = np.concatenate([TTLPauseBeforePulse, TTLPulse])
        else:
            TTLPauseAfterPulse = np.zeros(round((PauseAfterPulseDur-PulseDur) * Rate),
                            dtype=np.float32)
            TTLUnit = np.concatenate([TTLPauseBeforePulse, TTLPulse, TTLPauseAfterPulse])

    TTLUnit = (TTLUnit * TTLAmpF)

    return(TTLUnit)


def TTLSqWave(Rate, PulseDur, TTLAmpF, TTLVal, PauseBeforePulseDur=0,
           PauseAfterPulseDur=0):

    print('Generating Sound TTL...')
    if PulseDur < 0.1:
        TTLPulse = np.concatenate([
            np.array([TTLVal] * round(Rate*PulseDur/2), dtype=np.float32),
            np.array([TTLVal*-1] * round(Rate*PulseDur/2), dtype=np.float32)
        ])
    else:
        TTLPulse = np.concatenate([
            np.array([TTLVal] * round(Rate*0.01), dtype=np.float32),
            np.zeros(int(Rate*(PulseDur-0.02)), dtype=np.float32),
            np.array([TTLVal*-1] * round(Rate*0.01), dtype=np.float32)
        ])

    TTLPulse[-1] = 0

    TTLUnit = np.concatenate([
        np.zeros(int(PauseBeforePulseDur*Rate), dtype=np.float32),
        TTLPulse,
        np.zeros(int(PauseAfterPulseDur*Rate), dtype=np.float32)
    ])

    TTLUnit = TTLUnit * TTLAmpF

    return(TTLUnit)


## Level 1
def LaserStim(Rate, LaserPulseDur, LaserDur, LaserFreq, System, TTLAmpF=1, LaserPauseBeforePulseDur=0, LaserPauseAfterPulseDur=0, Ch=1, LaserType='Sq', **Kws):
    """
    if LaserType == 'Sq':
        Generate square waves in one channel that works as TTLs for laser.

        WARNING: The signal generated is composed of square WAVES, not pulses,
        meaning that it reaches positive AND NEGATIVE values. If your device
        handles only positive voltage, use a diode on the input of your device.

        https://en.wikipedia.org/wiki/Diode

    elif LaserType == 'Sin':
        Generate sine waves in one channel.

        WARNING: The signal generated is a sine wave that reaches positive
        AND NEGATIVE values. If your device handles only positive voltage,
        use a DC offset circuit to shift the wave to the positive range.

        https://en.wikipedia.org/wiki/Voltage_divider
    """

    if LaserType == 'Sq':
        LaserUnit = TTLSqWave(Rate, LaserPulseDur*2, TTLAmpF, LaserTTLVal, LaserPauseBeforePulseDur, LaserPauseAfterPulseDur)
        LaserUnit = LaserUnit[:-int(LaserPulseDur*Rate)]

    elif LaserType == 'Sin':
        LaserUnit = SineWave(Rate, LaserFreq, TTLAmpF*LaserTTLVal, LaserDur)

    Laser = np.zeros((LaserUnit.shape[0], 2), dtype='float32')
    Laser[:,Ch-1] = LaserUnit.T
    Laser = np.ascontiguousarray(Laser)

    print('Done generating laser stimulus.')
    return(Laser)


def SoundStim(Rate, SoundPulseDur, SoundAmpF, NoiseFrequency,
              System, TTLAmpF=1, SoundPauseBeforePulseDur=0, SoundPauseAfterPulseDur=0, TTLs=True,
              Map=[1,2], SoundType='Noise', **Kws):
    """
    Generate sound pulses in one channel and TTLs in the other channel.
    Returns an array of dimensions [Data, Channel, AmpF, Freq].

    WARNING: The signal generated in the TTLs channel is composed of square
    WAVES, not pulses, meaning that it reaches positive AND NEGATIVE values.
    If your device  handles only positive voltage, use a diode on the input
    of your device.

    https://en.wikipedia.org/wiki/Diode
    """

    TotalDur = round(Rate * (SoundPauseBeforePulseDur+SoundPulseDur+SoundPauseAfterPulseDur))

    # if type(NoiseFrequency[0]) == list:
    if SoundType.lower() == 'noise':
        SoundPulse = Noise(Rate, SoundPulseDur)
        print('   ', end='')
        SoundPulseFiltered = BandpassFilterSound(SoundPulse, Rate, NoiseFrequency)
        print('')

    elif SoundType.lower() == 'tone':
        print('Generating tones... ', end='')
        SoundPulseFiltered = np.zeros((int(Rate*SoundPulseDur), len(NoiseFrequency)), dtype='float32')
        for F,Freq in enumerate(NoiseFrequency):
            if type(Freq) in [int, float]:
                SoundPulseFiltered[:,F] = SineWave(Rate, Freq, 1, SoundPulseDur)
            else:
                Freq = [(Freq[1] - Freq[0])/SoundPulseDur, Freq[0]]
                Time = np.linspace(0, SoundPulseDur, int(Rate*SoundPulseDur))
                SoundPulseFiltered[:,F] = SineWave(Rate, Freq, 1, Time)

        print('Done.')

    SoundUnit = ApplySoundAmpF(SoundPulseFiltered, Rate, SoundAmpF,
                               NoiseFrequency, SoundPauseBeforePulseDur,
                               SoundPauseAfterPulseDur)

    if TTLs:
        SoundTTLUnit = TTLSqWave(Rate, SoundPulseDur, TTLAmpF, SoundTTLVal,
                              SoundPauseBeforePulseDur,
                              SoundPauseAfterPulseDur)
    else:
        SoundTTLUnit = np.zeros(TotalDur, dtype='float32')


    Sound = np.zeros(((SoundUnit.shape[0], 2)+ SoundUnit.shape[1:]), dtype=SoundUnit.dtype)
    for F in range(Sound.shape[3]):
        for A in range(Sound.shape[2]):
            Sound[:, Map[0]-1, A, F] = SoundTTLUnit
            Sound[:, Map[1]-1, A, F] = SoundUnit[:,A,F]

    Sound = np.ascontiguousarray(Sound)
    print('Done generating sound stimulus.')
    return(Sound)


## Level 2
def SoundLaserStim(Rate, SoundPulseDur, SoundAmpF, NoiseFrequency, System, LaserPulseDur, LaserType, LaserDur, LaserFreq, TTLAmpF=1, SoundPauseBeforePulseDur=0, SoundPauseAfterPulseDur=0, TTLs=True, Map=[1,2], SoundType='Noise', LaserPauseBeforePulseDur=0, LaserPauseAfterPulseDur=0, **Kws):
    """ Generate sound pulses in one channel and a mix of square waves that
        works as TTLs for both sound and laser in the other channel.

        WARNING: The signal generated in the TTLs channel is composed of square
        WAVES, not pulses, meaning that it reaches positive AND NEGATIVE values.
        If your device  handles only positive voltage, use a diode on the
        input of your device.

        https://en.wikipedia.org/wiki/Diode
    """

    SoundLaser = SoundStim(
        Rate, SoundPulseDur, SoundAmpF, NoiseFrequency, System, TTLAmpF, SoundPauseBeforePulseDur, SoundPauseAfterPulseDur, TTLs, Map, SoundType
    )

    LaserTTLAmpF = LaserTTLVal - SoundTTLVal
    SoundTTLAmpF = SoundTTLVal * (LaserTTLAmpF/LaserTTLVal)

    SoundTTLUnit = TTLSqWave(Rate, SoundPulseDur, TTLAmpF, SoundTTLAmpF,
                          SoundPauseBeforePulseDur,
                          SoundPauseAfterPulseDur)

    if LaserType == 'Sq':
        LaserUnit = TTLSqWave(Rate, LaserPulseDur*2, TTLAmpF, LaserTTLAmpF,
                       LaserPauseBeforePulseDur, LaserPauseAfterPulseDur)
        LaserUnit = LaserUnit[:-int(LaserPulseDur*Rate)]

    elif LaserType == 'Sin':
        LaserUnit = SineWave(Rate, LaserFreq, TTLAmpF*LaserTTLVal, LaserDur)


    for F in range(SoundLaser.shape[3]):
        for A in range(SoundLaser.shape[2]):
            SoundLaser[:, Map[0]-1, A, F] = SoundTTLUnit+LaserUnit

    SoundLaser = np.ascontiguousarray(SoundLaser)

    print('Done generating sound and laser stimulus.')
    return(SoundLaser)

