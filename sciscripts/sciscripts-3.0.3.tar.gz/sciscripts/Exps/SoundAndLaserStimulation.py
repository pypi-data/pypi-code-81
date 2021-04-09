#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to generate pulses and send to the soundboard, and then to a
sound amplifier and an Arduino board. Basically it generates sound pulses,
sound square waves (TTLs), and laser square waves. The square waves will be
sent to the left channel and the sound pulses will be sent to the right
channel.
"""

from datetime import datetime
import numpy as np
from time import sleep

from sciscripts.IO import Arduino, DAqs, SigGen, Txt
from sciscripts.IO.SoundCard import AudioSet


def Prepare(AnimalName, StimType, StimCh, TTLCh, System, Setup,
            RecCh=None, SoundType=None,
            Intensities=None, NoiseFrequency=None, SoundPulseNo=None,
            SoundPauseBeforePulseDur=None, SoundPulseDur=None, SoundPauseAfterPulseDur=None,
            PauseBetweenIntensities=None,
            LaserStimBlockNo=None, LaserPulseNo=None, LaserPauseBeforePulseDur=None,
            LaserPulseDur=None, LaserPauseAfterPulseDur=None,
            LaserPauseBetweenStimBlocksDur=None, LaserType=None, LaserDur=None, LaserFreq=None,
            AnalogTTLs=True, Rate=192000, BlockSize=384, Channels=2,
            BaudRate=115200, TTLAmpF=1, Probe=None, Adaptor=None, Remapped=False, ChSpacing=None, TTLs=True, StimulationDelay=0, **Kws):
    SoundAmpF = DAqs.dBToAmpF(Intensities, System, Setup)
    if 'SoundAmpF' in Kws.keys():
        SoundAmpF = Kws['SoundAmpF']
        # print(SoundAmpF)

    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    InfoFile = '-'.join([Date, AnimalName, '_'.join(StimType)+'.dict'])
    Kws = {**locals()}
    DataInfo = Txt.InfoWrite(**Kws)
    # print(DataInfo['Audio'])

    if type(PauseBetweenIntensities) == list:
        PauseBetweenIntensities = max(PauseBetweenIntensities)

    if type(LaserPauseBetweenStimBlocksDur) == list:
        LaserPauseBetweenStimBlocksDur = max(LaserPauseBetweenStimBlocksDur)

    Stimulation = {}
    Stimulation['Stim'] = AudioSet(Rate, BlockSize, Channels, 'Out')
    Stimulation['ArduinoObj'] = Arduino.CreateObj(BaudRate)
    if not Stimulation['ArduinoObj']:
        print('No Arduino detected!!!')
        print('NO DIGITAL TTLs WILL BE DELIVERED!!!')
        print('YOU HAVE BEEN WARNED!!!')
        print('Analog TTLs will still work.')

    if 'Sound' in StimType:
        if DataInfo['Audio']['Setup'] == 'GPIAS': Map = [2,1]
        else: Map = [1,2]

        Stimulation['Sound'] = SigGen.SoundStim(TTLs=TTLs, Map=Map, **DataInfo['Audio'])

        Stimulation['SoundPause'] = np.zeros(
                (PauseBetweenIntensities*Rate,2), dtype='float32')

    if 'Laser' in StimType:
        Stimulation['Laser'] = SigGen.LaserStim(
                Rate=Rate,
                TTLAmpF=DataInfo['Audio']['TTLAmpF'],
                System=System,
                **DataInfo['Laser'])

        Stimulation['LaserPause'] = np.zeros(
                (LaserPauseBetweenStimBlocksDur*Rate,2), dtype='float32')

    if 'SoundLaser' in StimType:
        Stimulation['SoundLaser'] = SigGen.SoundLaserStim(
            **DataInfo['Audio'],
            **DataInfo['Laser']
        )

        Stimulation['SoundLaserPause'] = np.zeros(
                (PauseBetweenIntensities*Rate,2), dtype='float32')

    return(Stimulation, InfoFile)


def PlaySound(Sound, Pause, Stim, ArduinoObj, InfoFile, StimType, DV='Out', ToDel=False):
    DataInfo = Txt.Read(InfoFile)
    if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}
    RandomFKeys = np.random.permutation(DataInfo['Audio']['Freqs'])

    Sound = DAqs.Normalize(Sound, DataInfo['Audio']['System'], 'Out')
    Pause = DAqs.Normalize(Pause, DataInfo['Audio']['System'], 'Out')

    if ToDel:
        ttls = np.zeros(int(192000*0.05), dtype='float32')
        ttls[:int(192000*0.005)] = 1.7
        ttls[int(192000*0.005):int(192000*0.01)] = -1.7
        pause = np.tile(ttls, Pause.shape[0]//ttls.shape[0])
        ttls = np.tile(ttls, 10)
        for a in range(Sound.shape[2]):
            for b in range(Sound.shape[3]):
                Sound[:,0,a,b] += ttls
        Pause[:,0] = pause


    Stim.start()
    while True:
        try:
            print('Remember to change folder name in OE!')
            print('Choose frequency:')
            print('-1)', 'Baseline (No stimulus)')
            for Ind, K in enumerate(DataInfo['Audio']['Freqs']): print(str(Ind) + ')' , K)
            print(str(len(DataInfo['Audio']['Freqs'])) + ')', 'Cancel')
            print('')
            print('Random suggestion:')
            print(RandomFKeys)
            print('')
            F = input(': ')

            if F == str(len(DataInfo['Audio']['Freqs'])): break
            if F == str(-1):
                Rec = "{0:02d}".format(len(DataInfo['ExpInfo']))
                DataInfo['ExpInfo'][Rec] = {'DV': DV, 'StimType': StimType, 'Hz': 'Baseline'}
                Txt.Write(DataInfo, InfoFile)
                continue

            F = int(F)
            try:
                FKey = DataInfo['Audio']['Freqs'][F]
            except IndexError:
                print('=== Wrong Freq index. Stopping... ===')
                print('')
                break

            if ArduinoObj: ArduinoObj.write(b'C'); sleep(DataInfo['DAqs']['StimulationDelay'])

            for A, AmpF in enumerate(DataInfo['Audio']['Intensities']):
                if type(DataInfo['Audio']['PauseBetweenIntensities']) == list:
                    PauseLow = DataInfo['Audio']['PauseBetweenIntensities'][0]
                    PauseHigh = DataInfo['Audio']['PauseBetweenIntensities'][1]+1
                    PauseEnd = np.random.randint(PauseLow,PauseHigh)
                    PauseEnd = int(PauseEnd*DataInfo['Audio']['Rate'])
                else:
                    PauseEnd = Pause.shape[0]

                SS = np.concatenate([Sound[:,:,A,F] for _ in range(DataInfo['Audio']['SoundPulseNo'])])

                print('Playing', FKey, 'at', str(AmpF), 'dB,', A+1, 'of', len(DataInfo['Audio']['Intensities']))
                if ArduinoObj: ArduinoObj.write(b'd')
                Stim.write(SS)
                if ArduinoObj: ArduinoObj.write(b'w')
                Stim.write(Pause[:PauseEnd,:])
                del(SS)

            if ArduinoObj: ArduinoObj.write(b'C')

            Rec = "{0:02d}".format(len(DataInfo['ExpInfo']))
            DataInfo['ExpInfo'][Rec] = {'DV': DV, 'StimType': StimType, 'Hz': FKey}
            Txt.Write(DataInfo, InfoFile)

            print('Played Freq', FKey, 'at', DV, 'µm DV')
        except KeyboardInterrupt:
            print(''); print('=====')
            print('Sorry for the wait. Rebooting Arduino...')
            if ArduinoObj:
                ArduinoObj.write(b'w')
                ArduinoObj.write(b'C')
                Arduino.Reset(ArduinoObj)
            print('Resuming loop...')
            print('====='); print('')
            continue

    Stim.stop()
    return(None)


def PlayLaser(Laser, LaserStimBlockNo, Pause, Stim, ArduinoObj, InfoFile, StimType, DV='Out'):
    DataInfo = Txt.Read(InfoFile)
    if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}
    Laser = DAqs.Normalize(Laser, DataInfo['Audio']['System'], 'Out')

    if not ArduinoObj:
        print('No Arduino detected!!!')
        print('NO DIGITAL TTLS WILL BE DELIVERED!!')
        print('Laser TTLs will still work.')

    Stim.start()
    while True:
        try:
            print('What to do?')
            print('-1) Baseline (No stimulus)')
            print('0) Run stimulation')
            print('1) Cancel')
            Ans = input(': ')

            if Ans == '1': break
            if Ans == str(-1):
                Rec = "{0:02d}".format(len(DataInfo['ExpInfo']))
                DataInfo['ExpInfo'][Rec] = {'DV': DV, 'StimType': StimType, 'Hz': 'Baseline'}
                Txt.Write(DataInfo, InfoFile)
                continue

            if ArduinoObj: ArduinoObj.write(b'C'); sleep(DataInfo['DAqs']['StimulationDelay'])

            for Block in range(LaserStimBlockNo):
                # LL = np.concatenate([Laser for _ in range(DataInfo['Laser']['LaserPulseNo'])])
                print('Running laser stimulation, block', Block+1, 'of', LaserStimBlockNo)
                if type(DataInfo['Laser']['LaserPauseBetweenStimBlocksDur']) == list:
                    PauseLow = DataInfo['Laser']['LaserPauseBetweenStimBlocksDur'][0]
                    PauseHigh = DataInfo['Laser']['LaserPauseBetweenStimBlocksDur'][1]+1
                    PauseEnd = np.random.randint(PauseLow,PauseHigh)
                    PauseEnd = int(PauseEnd*DataInfo['Audio']['Rate'])
                else:
                    PauseEnd = Pause.shape[0]


                if ArduinoObj: ArduinoObj.write(b'd')
                for Pulse in range(DataInfo['Laser']['LaserPulseNo']):
                    Stim.write(Laser)
                if ArduinoObj: ArduinoObj.write(b'w')

                Stim.write(Pause[:PauseEnd,:])
                # del(LL)

            if ArduinoObj: ArduinoObj.write(b'C')

            Rec = "{0:02d}".format(len(DataInfo['ExpInfo']))
            if DataInfo['Laser']['LaserType'] == 'Sin':
                DataInfo['ExpInfo'][Rec] = {'DV': DV, 'StimType': StimType, 'Hz': DataInfo['Laser']['LaserFreq']}
            else:
                DataInfo['ExpInfo'][Rec] = {'DV': DV, 'StimType': StimType, 'Hz': 'LaserPulses'}

            Txt.Write(DataInfo, InfoFile)

            print('Finished laser stimulation at', DV, 'µm DV')
        except KeyboardInterrupt:
            print(''); print('=====')
            print('Sorry for the wait. Rebooting Arduino...')
            if ArduinoObj:
                ArduinoObj.write(b'w')
                ArduinoObj.write(b'C')
                Arduino.Reset(ArduinoObj)
            print('Resuming loop...')
            print('====='); print('')
            continue

    Stim.stop()
    return(None)


def Play(Stimulation, InfoFile, StimType, DV, ToDel=False):
    DataInfo = Txt.Read(InfoFile)

    if 'Sound' in StimType and 'Laser' in StimType:
        PlaySound(Stimulation['SoundLaser'].copy(), Stimulation['SoundLaserPause'],
                  Stimulation['Stim'], Stimulation['ArduinoObj'], InfoFile,
                  StimType, DV)

    elif 'Sound' in StimType and 'Laser' not in StimType:
        PlaySound(Stimulation['Sound'].copy(), Stimulation['SoundPause'],
                  Stimulation['Stim'], Stimulation['ArduinoObj'], InfoFile,
                  StimType, DV, ToDel)

    elif 'Sound' not in StimType and 'Laser' in StimType:
        PlayLaser(Stimulation['Laser'].copy(), DataInfo['Laser']['LaserStimBlockNo'],
                  Stimulation['LaserPause'], Stimulation['Stim'],
                  Stimulation['ArduinoObj'], InfoFile, StimType, DV)

    else:
        print(""" StimType should contain 'Sound', 'Laser' or both, otherwise,
                  this function is useless :)""")

    return(None)
