# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This script can be used to calibrate the sound card in and out amplification
factor. This is mandatory for using submodules from sciscripts.Exps with the
default arguments.

It is very important to set the volume of the sound card to unit level
(usually 0dB, which is 100% of the intensity) so you know that no kind of
frequency filter is being applied.
"""

print('[Exps.SoundMeasurements] Loading dependencies...')
import os
import numpy as np
from datetime import datetime
from time import sleep

from sciscripts.IO import IO, SigGen, SoundCard, Txt
from sciscripts.IO.DAqs import CalibrationPath
print('[Exps.SoundMeasurements] Done.')


## Level 0
def GetSoundAmpF(Start=np.log10(1e-5), Stop=np.log10(1), Len=320):
    SoundAmpF = np.hstack((
                    np.flipud(np.logspace(Start, Stop, Len-1)),
                    np.array(0.0)
                ))
    SoundAmpF = np.array([round(_,6) for _ in SoundAmpF])
    return(SoundAmpF)


def PlayRec(DataPath, System, Setup, SoundAmpF, NoiseFrequency, SoundPulseDur,
            Rate, BlockSize=None, **Kws):
    print('Sound measurement running...')
    Map = [2,1] if Setup == 'GPIAS' else [1,2]
    SoundCard.AudioSet(Rate, BlockSize, Channels=2)

    for Freq in NoiseFrequency:
        FKey = str(Freq[0]) + '-' + str(Freq[1])
        Sound = SigGen.SoundStim(Rate, SoundPulseDur, SoundAmpF,
                                    [Freq], System, 0,
                                    TTLs=False, Map=Map)

        for A in range(Sound.shape[2]):
            AKey = str(SoundAmpF[FKey][A]).replace('.', '_')
            print(FKey, AKey)
            SoundRec = SoundCard.ReadWrite(Sound[:,:,A,0], System=System, InMap=[1])
            SoundRec = SoundRec[2000:] # Temp override
            IO.Bin.Write(SoundRec, DataPath+'/SoundRec/'+FKey+'/'+AKey+'.dat')

        print('Done playing/recording', FKey + '.')
        del(Sound, SoundRec)

    print('Finished recording \O/')
    return(None)


def WarnUser(FullTime):
    print('')
    print('Full test will take', FullTime, 'min to run.')
    print('Current time: ', datetime.now().strftime("%H:%M:%S"))
    input('Press any key to start... ')
    print('This can be loud - cover your ears!!')
    print('')
    for i in range(5, 0, -1): print(i, end=' '); sleep(1)
    print('')


## Level 1
def CalibrateInput(Repetitions, TestAmp, SBOutAmpF, Freq, WaveDur, Rate, BlockSize=None, Channel=1):
    """
    Read signal from sound card input. You have to apply a known amplitude
    signal (a sine wave, for example) to the sound card input, so you can
    check if the voltage you applied is the voltage being read by the sound
    card.
    """
    SoundCard.AudioSet(Rate, BlockSize, Channels=1)
    Pulse = SigGen.SineWave(Rate, Freq, TestAmp*SBOutAmpF, WaveDur)
    SBInAmpF = np.zeros(Repetitions, dtype=np.float32)
    print('Connect the system output to the system input')
    input('and press enter to proceed.')

    for aa in range(Repetitions):
        print('Measuring... ', end='')
        Rec = SoundCard.ReadWrite(Pulse, OutMap=[Channel], InMap=[Channel])
        print('Done.')

        #SBInAmpF[aa] = (max(Rec)-(min(Rec)))/2
        SBInAmpF[aa] = (max(Rec[2000:])-(min(Rec[2000:])))/2
        print(SBInAmpF[aa])

    # SBInAmpF is the real amplitude divided by the measured amplitude
    SBInAmpF = TestAmp/SBInAmpF.mean()
    print('SBInAmpF = ', str(SBInAmpF))

    return(SBInAmpF)


def CalibrateOutput(Freq, WaveDur, Rate, BlockSize=None, Channel=1):
    """
    Write sine waves of 1V to sound card output. This function helps to get the
    sound card amplification factor, which is how much it is increasing or
    decreasing the signal written to it.
    """
    SoundCard.AudioSet(Rate, BlockSize, Channels=1)
    Pulse = SigGen.SineWave(Rate, Freq, 1, WaveDur)

    print('Plug the output in an oscilloscope')
    input('and press enter to start.')
    SoundCard.Write(Pulse, [Channel]);
    # SBOutAmpF is the generated signal divided by the measured signal
    Amp = input('Measured amplitude: ')
    SBOutAmpF = 1/float(Amp)

    return(SBOutAmpF)


def GetBasalNoise(Duration, Rate, BlockSize=None):
    SoundCard.AudioSet(Rate, BlockSize, Channels=1)
    Noise = SoundCard.Read(Duration*Rate)
    return(Noise)


## Level 2
def RunCalibration(Freq, WaveDur, Repetitions, System, Rate, BlockSize=None, Channel=1, **Kws):
    DataPath = CalibrationPath + '/' + System

    AmpF = {}
    AmpF['OutAmpF'] = CalibrateOutput(Freq, WaveDur, Rate, BlockSize, Channel)
    AmpF['InAmpF'] = CalibrateInput(Repetitions, 1, AmpF['OutAmpF'], Freq, WaveDur, Rate, BlockSize, Channel)
    Noise = GetBasalNoise(WaveDur, Rate, BlockSize)
    Noise *= AmpF['InAmpF']

    IO.Txt.Write(AmpF, DataPath+'/AmpF.txt')
    IO.DataWriter(Noise, DataPath+'/Noise.dat', 'dat')

    print('Calibration finished for', System)
    return(None)


def RunMeasurement(NoiseFrequency, SoundPulseDur, Rate, System, Setup, MicSens_dB=None, MicSens_VPa=None, BlockSize=None, **Kws):
    """
    Generate white noise sound pulses at several frequencies and
    intensities, play and record them at the same time, creating a dataset that
    allows SciScripts to know which voltage corresponds to which intensity.
    """
    if MicSens_dB == None and MicSens_VPa == None:
        raise ValueError('At least one of MicSens_dB or MicSens_VPa must be provided.')

    Group = '/'.join([System, Setup])
    DataPath = CalibrationPath + '/' + Group

    AmpF = IO.Txt.Read(CalibrationPath+'/'+System+'/AmpF.txt')
    OutMax = 1/AmpF['OutAmpF']

    if 'SoundAmpF' in Kws: SoundAmpF = Kws['SoundAmpF']
    else: SoundAmpF = GetSoundAmpF(Stop=np.log10(OutMax))

    Freqs = [str(Freq[0]) + '-' + str(Freq[1]) for Freq in NoiseFrequency]
    SoundAmpF = {Freq: SoundAmpF for Freq in Freqs}

    InfoFile = DataPath + '/SoundMeasurement.dict'
    Kws = {**locals()}
    os.makedirs(DataPath, exist_ok=True)
    # if os.path.isfile(InfoFile): Kws = {**Txt.Read(InfoFile), **Kws}
    DataInfo = Txt.InfoWrite(**Kws)
    # print(SoundAmpF, NoiseFrequency, SoundPulseDur)
    FullTime = (len(SoundAmpF[Freqs[0]])*len(NoiseFrequency)*(SoundPulseDur))/60
    FullTime = str(round(FullTime, 2))
    WarnUser(FullTime)
    print(DataPath)
    PlayRec(DataPath, **DataInfo['Audio'])
    return(None)

