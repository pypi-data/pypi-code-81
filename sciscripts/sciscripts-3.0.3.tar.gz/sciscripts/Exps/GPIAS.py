#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20171123
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import random
from datetime import datetime

from sciscripts.IO import Arduino, DAqs, SigGen, SoundCard, Txt



def PlayTrial(Sound, Stim, ArduinoObj, RealFreq, RealTrial, SBSSamples):
    Sound['BetweenStim'] = np.ascontiguousarray(Sound['BetweenStim'][:SBSSamples,:,0,RealFreq])
    for K in Sound:
        if K != 'BetweenStim':
            Sound[K] = np.ascontiguousarray(Sound[K][:,:,0,RealFreq])

    Stim.write(Sound['BetweenStim'])
    if ArduinoObj: ArduinoObj.write(b'd')
    Stim.write(Sound['BG'])
    Stim.write(Sound[RealTrial])
    Stim.write(Sound['BGPrePulse'])
    Stim.write(Sound['LoudPulse'])
    Stim.write(Sound['BGAfterPulse'])
    if ArduinoObj: ArduinoObj.write(b'w')


def Play(Sound, Stim, ArduinoObj, NoiseFrequency, SoundBetweenStimDur, NoOfTrials, SoundBGAmpF, SoundPulseAmpF, Rate, DataInfo, PrePost=0, **kwargs):
    if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}
    for K in Sound.keys():
        Sound[K] = DAqs.Normalize(Sound[K], DataInfo['Audio']['System'], 'Out')

    print('Pseudo-randomizing frequencies...')
    TrialsStr = ['NoGap', 'Gap']
    Freqs = [In for In, El in enumerate(NoiseFrequency)]*NoOfTrials
    np.random.shuffle(Freqs)

    FreqSlot = [[0] for _ in range(len(Freqs)*2)]
    for FE in range(len(Freqs)):
        FreqSlot[FE*2] = (Freqs[0:FE+1].count(Freqs[FE])-1)*2
        FreqSlot[FE*2+1] = (Freqs[0:FE+1].count(Freqs[FE])-1)*2+1

    FreqOrder = [[0]]
    Rec = -1

    print("Running...")
    Stim.start()
    # Play the Pre-trials
    for Pre in range(PrePost):
        Rec += 1
        RealFreq = -1
        FreqOrder[len(FreqOrder)-1] = [-1, -1]
        FreqOrder.append([0])
        SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

        print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' Pre-trial', 'Rec', Rec)
        PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, 'NoGap', SBSDur*Rate)

    # Play the test trials
    for Hz in range(len(Freqs)):
        Trials = [0, 1]
        random.shuffle(Trials)
        print(str(Hz+1), 'of', str(len(Freqs)))

        for Trial in Trials:
            Rec += 1
            RealFreq = Freqs[Hz]
            RealTrial = FreqSlot[Hz*2+Trial]
            FreqOrder[len(FreqOrder)-1] = [Freqs[Hz], RealTrial]
            FreqOrder.append([0])
            SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

            print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' trial ', TrialsStr[Trial], 'Rec', Rec)
            PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, TrialsStr[Trial], SBSDur*Rate)

    # Play the Post-trials
    for Post in range(PrePost):
        Rec += 1
        RealFreq = -1
        FreqOrder[len(FreqOrder)-1] = [-1, -2]
        FreqOrder.append([0])
        SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

        print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' Post-trial', 'Rec', Rec)
        PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, 'NoGap', SBSDur*Rate)

    Stim.stop()
    FreqOrder.remove([0])

    DataInfo['ExpInfo']['FreqOrder'] = FreqOrder
    DataInfo['ExpInfo']['FreqSlot'] = FreqSlot
    DataInfo['ExpInfo']['Freqs'] = Freqs

    Txt.Write(DataInfo, DataInfo['InfoFile'])


def Run(AnimalName, StimType, BGIntensity, PulseIntensity,
        NoiseFrequency, SoundBGDur, SoundGapDur,
        SoundBGPrePulseDur, SoundLoudPulseDur,
        SoundBGAfterPulseDur, SoundBetweenStimDur, NoOfTrials,
        System, Setup, StimCh, TTLCh, RecCh, AnalogTTLs=True,
        Rate=192000, BlockSize=384, Channels=2, BaudRate=115200, TTLAmpF = 1,
        PrePost=0, **Kws):

    SoundBGAmpF = DAqs.dBToAmpF(BGIntensity, System, Setup)
    SoundPulseAmpF = DAqs.dBToAmpF(PulseIntensity, System, Setup)

    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    InfoFile = '-'.join([Date, AnimalName, 'GPIAS.dict'])
    Kws = {**locals()}
    DataInfo = Txt.InfoWrite(**Kws)

    Map = [2,1] if Setup == 'GPIAS' else [1,2]
    Sound = SigGen.GPIAS(Map=Map, **DataInfo['Audio'])
    Stim = SoundCard.AudioSet(Rate, BlockSize, Channels, ReturnStream='Out')
    ArduinoObj = Arduino.CreateObj(BaudRate)
    if not ArduinoObj:
        print('No Arduino detected!!!')
        print('NO DIGITAL TTLs WILL BE DELIVERED!!!')
        print('YOU HAVE BEEN WARNED!!!')
        print('Analog TTLs will still work.')

    try:
        Play(Sound, Stim, ArduinoObj, DataInfo=DataInfo, **DataInfo['Audio'])
    except KeyboardInterrupt:
            print(''); print('=====')
            print('Sorry for the wait. Rebooting Arduino...')
            if ArduinoObj: Arduino.Reset(ArduinoObj)
            print('Bye!')
            print('====='); print('')

    print('Finished', AnimalName, 'GPIAS.')

