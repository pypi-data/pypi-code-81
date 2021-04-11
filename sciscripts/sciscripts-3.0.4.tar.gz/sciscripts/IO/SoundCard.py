# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script that defines functions allowing the use of a computer's sound
board as an analog I/O board.

"""

print('[IO.SoundCard] Importing dependencies...')
import sounddevice as SD

from sciscripts.IO import DAqs
print('[IO.SoundCard] Done.')

## Level 0
def AudioSet(Rate=None, BlockSize=None, Channels=2, ReturnStream=None, **Kws):
    if 'system' in [_['name'] for _ in SD.query_devices()]:
        SD.default.device = 'system'
    else:
        SD.default.device = 'default'

    RateStd = [_['name'] for _ in SD.query_devices()].index(SD.default.device[0])
    RateStd = int(SD.query_devices()[RateStd]['default_samplerate'])

    SD.default.channels = Channels
    if Rate:
        SD.default.samplerate = Rate
        try:
            SD.check_output_settings()
        except Exception as e:
            Msg = f'\n\nThe selected sampling rate of {Rate} is not valid.\nThe default sampling rate is {RateStd}.\nTo use the audio card at the default sampling rate, use Rate=None.'
            raise Exception(Msg) from e

    if BlockSize: SD.default.blocksize = BlockSize

    if type(ReturnStream) == str:
        if ReturnStream.lower() == 'out':
            Stim = SD.OutputStream(dtype='float32')
        elif ReturnStream.lower() == 'in':
            Stim = SD.InputStream(dtype='float32')
        elif ReturnStream.lower() == 'both':
            Stim = SD.Stream(dtype='float32')
    else:
        Stim = None

    return(Stim)


def Write(Data, ChannelMap=None, System=None):
    AudioSet()
    if System: Data = DAqs.Normalize(Data, System, 'Out')
    SD.play(Data, blocking=True, mapping=ChannelMap)
    return(None)


def Read(Samples, ChannelMap=None, System=None):
    AudioSet()
    Rec = SD.rec(Samples, blocking=True, mapping=ChannelMap)
    if System: Rec = DAqs.Normalize(Rec, System, 'In')
    return(Rec)


def ReadWrite(Data, System=None, OutMap=None, InMap=None):
    AudioSet()
    if System: Data = DAqs.Normalize(Data, System, 'Out')
    InCh = len(InMap) if InMap else None
    Rec = SD.playrec(Data, blocking=True, output_mapping=OutMap, input_mapping=InMap, channels=InCh)
    if System: Rec = DAqs.Normalize(Rec, System, 'In')
    return(Rec)


