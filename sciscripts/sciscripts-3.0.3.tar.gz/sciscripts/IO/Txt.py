#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import os

from ast import literal_eval


def DictFlat(Var, UpKey='', KeySep='_', Flat={}):
    if type(Var) == dict:
        for K, V in Var.items():
            NewKey = UpKey + KeySep + K if UpKey else K
            Flat = {**Flat, **DictFlat(Var[K], NewKey, KeySep, Flat)}
        return(Flat)
    else:
        Flat[UpKey] = Var
        return(Flat)


def Print(value, htchar='    ', itemchar=' ', breaklineat='auto', lfchar='\n', indent=0):
    ''' Modified from y.petremann's code.
        Added options to set item separator for list or tuple and to set a number
        of items per line, or yet, to calculate items per line so it will not
        have more than 80 chars per line.
        Source: https://stackoverflow.com/a/26209900 '''

    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + Print(value[key], htchar, itemchar, breaklineat, lfchar, indent + 1)
            for key in value
        ]

        return '{%s}' % (','.join(items) + lfchar + htchar * indent)

    elif type(value) is list or type(value) is tuple:
        items = [
            itemchar + Print(item, htchar, itemchar, breaklineat, lfchar, indent + 1)
            for item in value
        ]

        if breaklineat == 'auto':
            L = len(items) if len(items) else 1
            bl = int((80 - (len(htchar)*(indent + 1)))/
                (int((sum([len(i)+4 for i in items])-len(itemchar)-1)/L)))

        else: bl = breaklineat

        if not bl: bl = 1

        if len(items) > bl:
            for i in list(range(bl, len(items), bl)):
                items[i] = lfchar + htchar*(indent+1) + '  ' + items[i]

        return '[%s]' % (','.join(items))

    elif type(value) is np.ndarray:
        value = value.tolist()
        items = Print(value, htchar, itemchar, breaklineat, lfchar, indent)
        return items

    else:
        return repr(value)


def Read(File):
    Dict = literal_eval(open(File).read())
    return(Dict)


def Write(Var, File):
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
    with open(File, 'w') as F: F.write(Print(Var))
    return(None)


def InfoWrite(InfoFile, **All):
    DataInfo = {'InfoFile': InfoFile}
    for K in ['AnimalName', 'CageName', 'StimType']:
        if K in All:
            if 'Animal' not in DataInfo: DataInfo['Animal'] = {}
            DataInfo['Animal'][K] = All[K]

    for K in ['StimCh', 'TTLCh', 'RecCh', 'BaudRate', 'AnalogTTLs', 'TTLs', 'StimulationDelay']:
        if K in All:
            if 'DAqs' not in DataInfo: DataInfo['DAqs'] = {}
            DataInfo['DAqs'][K] = All[K]

    for K in ['SoundType', 'Rate', 'BlockSize', 'Channels', 'Intensities',
              'NoiseFrequency', 'SoundPulseNo', 'SoundPauseBeforePulseDur',
              'SoundPulseDur', 'SoundPauseAfterPulseDur', 'PauseBetweenIntensities',
              'System', 'Setup', 'CalibrationFile', 'SoundAmpF',
              'TTLAmpF', 'MicSens_dB', 'MicSens_VPa', 'BGIntensity',
              'PulseIntensity', 'SoundBGDur', 'SoundGapDur',
              'SoundBGPrePulseDur','SoundLoudPulseDur', 'SoundBGAfterPulseDur',
              'SoundBetweenStimDur', 'NoOfTrials', 'SoundBGAmpF',
              'SoundPulseAmpF','PrePost']:
        if K in All:
            if 'Audio' not in DataInfo: DataInfo['Audio'] = {}
            DataInfo['Audio'][K] = All[K]
            if K == 'NoiseFrequency':
                if type(All[K][0]) == list():
                    DataInfo['Audio']['Freqs'] = ['-'.join([str(_) for _ in F])
                                                  for F in All[K]]
                else:
                    DataInfo['Audio']['Freqs'] = [str(F) for F in All[K]]

    for K in ['LaserStimBlockNo', 'LaserPulseNo', 'LaserPauseBeforePulseDur',
              'LaserPulseDur', 'LaserPauseAfterPulseDur',
              'LaserPauseBetweenStimBlocksDur', 'LaserType', 'LaserDur',
              'LaserFreq']:
        if K in All:
            if 'Laser' not in DataInfo: DataInfo['Laser'] = {}
            DataInfo['Laser'][K] = All[K]

    for K in ['Probe', 'Adaptor', 'Remapped', 'ChSpacing']:
        if K in All:
            if 'Probe' not in DataInfo: DataInfo['Probe'] = {}
            DataInfo['Probe'][K] = All[K]

    AllSubKeys = [_ for k in [K.keys() for K in DataInfo.values() if type(K) == dict]
                  for _ in k]
    for K in All:
        if K not in AllSubKeys:
            if 'Others' not in DataInfo: DataInfo['Others'] = {}
            DataInfo['Others'][K] = All[K]

    Write(DataInfo, InfoFile)

    return(DataInfo)


def Dict_OldToNew(Info):
    if 'FileName' in Info: Info['InfoFile'] = Info.pop('FileName')
    if 'ExpInfo' not in Info: Info['ExpInfo'] = {}

    for K in ['Animal', 'DAqs', 'Audio', 'Laser']:
        if K not in Info: Info[K] = {}

    for K in ['AnimalName', 'StimType']:
        if K in Info: Info['Animal'][K] = Info.pop(K)

    for K in ['RecCh', 'SoundCh', 'TTLCh', 'ABRCh', 'GPIASCh', 'PiezoCh', 'BaudRate', 'AnalogTTLs']:
        if K in Info: Info['DAqs'][K] = Info.pop(K)

    for K in ['Rate', 'Intensities', 'NoiseFrequency', 'SoundPulseNo',
              'SoundPauseBeforePulseDur', 'SoundPulseDur',
              'SoundPauseAfterPulseDur', 'PauseBetweenIntensities', 'System',
              'Setup', 'CalibrationFile', 'SoundAmpF', 'BackgroundIntensity',
              'PulseIntensity', 'SoundBackgroundDur', 'SoundGapDur',
              'SoundBackgroundPrePulseDur', 'SoundLoudPulseDur',
              'SoundBackgroundAfterPulseDur', 'SoundBetweenStimDur',
              'NoOfTrials', 'TTLAmpF', 'SoundBackgroundAmpF', 'SoundPulseAmpF']:
        if K in Info: Info['Audio'][K] = Info.pop(K)

    for K in ['LaserStimBlockNo', 'LaserPulseNo', 'LaserPauseBeforePulseDur',
              'LaserPulseDur', 'LaserPauseAfterPulseDur',
              'LaserPauseBetweenStimBlocksDur', 'LaserType', 'LaserDur',
              'LaserFreq']:
        if K in Info: Info['Laser'][K] = Info.pop(K)

    for K in Info['ExpInfo']:
        if 'DVCoord' in Info['ExpInfo'][K]:
            Info['ExpInfo'][K]['DV'] = Info['ExpInfo'][K].pop('DVCoord')

    if '00' in Info['ExpInfo']:
        if 'Hz' in Info['ExpInfo']['00']:
            if type(Info['ExpInfo']['00']['Hz']) == int:
                FreqList = ['-'.join([str(_[0]), str(_[1])]) for _ in Info['Audio']['NoiseFrequency']]
                Exps = list(Info['ExpInfo'].keys())
                for K in Exps:
                    F = FreqList[Info['ExpInfo'][K]['Hz']]
                    Info['ExpInfo'][K]['Hz'] = F

    if 'ABRCh' in Info['DAqs']: Info['DAqs']['RecCh'] = Info['DAqs'].pop('ABRCh')
    if 'GPIASCh' in Info['DAqs']: Info['DAqs']['RecCh'] = Info['DAqs'].pop('GPIASCh')
    if 'PiezoCh' in Info['DAqs']: Info['DAqs']['RecCh'] = Info['DAqs'].pop('PiezoCh')
    if 'SoundCh' in Info['DAqs']: Info['DAqs']['StimCh'] = Info['DAqs'].pop('SoundCh')

    if not Info['ExpInfo']:
        for K in ['FreqOrder', 'FreqSlot', 'Freqs']:
            if K in Info: Info['ExpInfo'][K] = Info.pop(K)

    RemainingKeys = list(Info.keys())
    for K in RemainingKeys:
        if K == 'LaserPrePauseDur': Info['Laser']['LaserPauseBeforePulseDur'] = Info.pop(K)
        elif K == 'LaserPostPauseDur': Info['Laser']['LaserPauseAfterPulseDur'] = Info.pop(K)
        elif K == 'SoundPauseBetweenStimBlocksDur': Info['Audio']['PauseBetweenIntensities'] = Info.pop(K)
        elif K == 'SoundStimBlockNo': Info['Audio'][K] = Info.pop(K)
        elif K == 'SoundPrePauseDur': Info['Audio']['SoundPauseBeforePulseDur'] = Info.pop(K)
        elif K == 'SoundPostPauseDur': Info['Audio']['SoundPauseAfterPulseDur'] = Info.pop(K)

    return(Info)

