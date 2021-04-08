import numpy
from extended_int import int_inf
from functools import reduce 
from FuncToWav import constants as c
from math import sin
from FuncToWav.helper import heaviside, combineFuncs
from typing import Callable

class SongBuilder:
    length: int
    numToFreq: Callable[[float], float]
    sampleRate: int
    notes: []

    def __init__(self, sampleRate: int = 48000):
        self.length = 0
        self.numToFreq = lambda num: round((2**((num-49)/12)*440),3)
        self.notes = []

    def __keyToNum__(self, scale: str, octave: str) -> int:
        if scale.lower() not in c.KEY_TO_NUM:
            raise ValueError("The letter code is not one of the scale")
        
        num = int(octave)*12+c.KEY_TO_NUM[scale.lower()]-8

        if num < 1 or num > 88:
            raise ValueError("Unsupported tone")

        return num

    def keyToNum(self, key: str) -> int:
        if len(key) == 3:
            scale = key[:2]
            octave = key[2]
        elif len(key) == 2:
            scale = key[0]
            octave = key[1]
        elif len(key) == 1:
            scale = key
            octave = 4
        else:
            raise ValueError("It's not possible to convert the input to key number")

        return self.__keyToNum__(scale, octave)

    def appendToSong(self, key: str, startTime: int, duration: int = None, endTime: int = int_inf):
        if (duration == None) and (endTime == int_inf):
            endTime = int_inf
        elif (duration == None) and (endTime != int_inf):
            endTime = endTime
            self.length = self.length if self.length >= startTime+duration else startTime+duration
        elif (duration != None) and (endTime == int_inf):
            endTime = startTime+duration
            self.length = self.length if self.length >= startTime+duration else startTime+duration
        else:
            if startTime+duration != endTime:
                raise ValueError("the note duration + note start timing must match end timing")

        part = {
            c.FREQUENCY: self.numToFreq(self.keyToNum(key)),
            c.START_TIME: startTime,
            c.END_TIME: endTime
        }

        self.notes.append(part)

    def freqToFunc(self, part: dict) -> Callable[[float], float]:
        freq = part[c.FREQUENCY]
        sTime = part[c.START_TIME]
        eTime = part[c.END_TIME]
        return lambda x: sin(freq * x) * heaviside(x, sTime=sTime, eTime=eTime)

    def buildSong(self) -> Callable[[float], float]:
        return reduce(combineFuncs, self.notes)
