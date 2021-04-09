#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti
@date: 20171123
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

from datetime import datetime

from sciscripts.IO import Arduino, DAqs, SigGen, SoundCard, Txt


## Level 0
def Play(Sound, Stim, Intensities, SoundPulseNo, DataInfo, Trigger=False, ArduinoObj=None):
    Sound = DAqs.Normalize(Sound, DataInfo['Audio']['System'], 'Out')
    if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}

    if Trigger:
        if ArduinoObj: ArduinoObj.write(b'T')
        else:
            print('There is no Arduino board connected.')
            print('Cannot run stimulation with Trigger.')
            return(None)

    try:
        Stim.start()
        print('Playing', DataInfo['Audio']['Freqs'][0], 'at', str(Intensities[0]), 'dB')
        for Pulse in range(SoundPulseNo): Stim.write(Sound[:,:,0,0])
        Stim.stop()
    except KeyboardInterrupt:
        print(''); print('=====')
        print('Sorry for the wait.')
        print('The sound was played for',
              str(((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])//60)+"'"+\
              str(((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])%60)+'"')
        print('====='); print('')

    if Trigger: Arduino.Reset(ArduinoObj)

    DataInfo['Audio']['SoundPulseNo'] = 1
    DataInfo['Audio']['SoundPulseDur'] = ((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])/60
    DataInfo['ExpInfo']['0'] = {'DVCoord': None,
                                'StimType': DataInfo['Animal']['StimType'],
                                'Hz': DataInfo['Audio']['Freqs'][0]}

    Txt.Write(DataInfo, DataInfo['InfoFile'])
    print('Done.')
    return(None)


## Level 1
def Run(AnimalName, StimType, Intensities, NoiseFrequency, SoundPulseDur, System, Setup, Rate=192000, BlockSize=384, Channels=2, Trigger=False):
    SoundPulseNo = round((SoundPulseDur*60)/20)
    SoundPulseDur = 20

    SoundAmpF = DAqs.dBToAmpF(Intensities, System, Setup)

    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    InfoFile = '-'.join([Date, AnimalName, 'AcousticNoiseTrauma.dict'])
    Kws = {**locals()}
    DataInfo = Txt.InfoWrite(**Kws)

    if Trigger:
        ArduinoObj = Arduino.CreateObj(115200)
        if not ArduinoObj:
            print('There is no Arduino board connected.')
            print('Cannot run stimulation with Trigger.')
            return(None)
    else:
        ArduinoObj = None

    Stim = SoundCard.AudioSet(ReturnStream='Out', **DataInfo['Audio'])
    Map = [2,1] if Setup == 'GPIAS' else [1,2]
    Sound = SigGen.SoundStim(Rate, SoundPulseDur, SoundAmpF, NoiseFrequency,
                             System, 0, TTLs=False, Map=Map)

    Play(Sound, Stim, Intensities, SoundPulseNo, DataInfo, Trigger=Trigger, ArduinoObj=ArduinoObj)
    return(None)

