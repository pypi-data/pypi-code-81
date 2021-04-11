#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import errno
import numpy as np
import os

from glob import glob
from sciscripts.IO import Txt


def PathToDict(Path, Value=None):
    Dict = {}
    Head = Path.split('/')[0]
    Tail = Path.split('/')[1:]

    if not Tail: Dict[Head] = Value
    else:
        Dict[Head] = PathToDict('/'.join(Tail), Value)

    return(Dict)


def MergeDicts(D1, D2):
    # Based on Paul Durivage's code available at
    # https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    for K, V in D2.items():
        if K in D1 and type(D1[K]) == dict and type(D2[K]) == dict:
            MergeDicts(D1[K], D2[K])
        else:
            D1[K] = D2[K]


def DictToList(Data):
    Keys = sorted(Data.keys(), key=lambda x: int(x.split('_')[-1]))
    Data = [
        DictToList(Data[K])
            if type(Data[K]) == dict
            and not False in ['_' in _ for _ in Data[K].keys()]
            and len(np.unique(['_'.join(_.split('_')[:-1]) for _ in Data[K].keys()])) == 1
        else Data[K]
        for K in Keys
    ]

    return(Data)


def Read(File, ChList=[], Info={}, Verbose=True, AsMMap=True):
    """
    Read flat interleaved binary data and return it as a numpy array. Data
    will be represented as Data[Channels, Samples].

    This function needs:
        - a text file in the same path but ending in
          "-Info.dict" containing a dictionary with the data
          info. The minimal information needed is Info['Shape'] and
          Info['DType']
        OR
        - an Info dict containing Info['Shape'] and Info['DType']
    """

    if '.' not in File:
        Data = {}
        Files = [glob(_.split('-Info.dict')[0]+'.*')[0]
                 for _ in glob(File+'/**/*.dict', recursive=True)]

        Paths = ['/'.join(_.split('/')[:-1]) for _ in Files]
        if not len(Paths):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), File)

        LastCommon = os.path.commonprefix(Paths).split('/')

        while LastCommon[-1] not in Paths[0].split('/'):
            LastCommon = LastCommon[:-1]

        if len(LastCommon) == 1:
            LastCommon = LastCommon[-1]
        elif len(LastCommon[-1]) and LastCommon[-2] != LastCommon[-1].split('_')[0] :
            LastCommon = LastCommon[-1]
        else:
            LastCommon = LastCommon[-2]

        # LastCommon = LastCommon[-1]
        LastCommon += '/'

        for d,D in enumerate(Files):
            Path = '.'.join(D.split('.')[:-1])
            Path = Path.split(LastCommon)[-1]
            if Verbose: print('Loading', Path, '...')
            MergeDicts(Data, PathToDict(Path, Read(D, ChList, Info, AsMMap=AsMMap)[0]))

        if not False in ['_' in _ for _ in Data.keys()]:
            if len(np.unique(['_'.join(_.split('_')[:-1]) for _ in Data.keys()])) == 1:
                Data = DictToList(Data)

        if Verbose: print('Done.')
        return(Data, None)

    else:
        InfoFile = '.'.join(File.split('.')[:-1]) + '-Info.dict'
        if not Info: Info = Txt.Read(InfoFile)

        if os.stat(File).st_size != 0:
            if AsMMap:
                Data = np.memmap(File, dtype=Info['DType'], mode='c').reshape(Info['Shape'])
            else:
                Data = np.fromfile(File, dtype=Info['DType']).reshape(Info['Shape'])

            if ChList: Data = Data[:,[Ch-1 for Ch in ChList]]
        else:
            Data = np.array([], dtype=Info['DType'])

        return(Data, Info)


def Write(Data, File, Info={}):
    """ Write numpy array to flat interleaved binary file. Data will be
        represented as ch1s1-ch2s1-ch3s1-...-chNs1-ch1s2-ch2s2...chNsN.

        Also, write a text file containing data info for data loading. """

    if type(Data) == dict or 'AsdfObject' in str(type(Data)):
        for K,V in Data.items(): Write(V, File+'/'+K, Info)

    elif type(Data) in [list, tuple]:
        for E,El in enumerate(Data):
            Write(El, File+'/'+File.split('/')[-1]+'_'+str(E), Info)

    elif type(Data) in [int, float, str]:
        Write(np.array(Data).reshape(1), File, Info)

    else:
        if '.' not in File: File +='.dat'
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)

        # Get info and generate path
        Info['Shape'] = Data.shape
        Info['DType'] = str(Data.dtype)
        Info['Flags'] = {}

        for Flag in ['C_CONTIGUOUS', 'F_CONTIGUOUS', 'OWNDATA', 'WRITEABLE',
                     'ALIGNED', 'UPDATEIFCOPY']:
            Info['Flags'][Flag] = Data.flags[Flag]

        InfoFile = '.'.join(File.split('.')[:-1]) + '-Info.dict'

        # Write text info file
        Txt.Write(Info, InfoFile)

        # Write interleaved data
        with open(File, 'wb') as F: Data.reshape(np.product(Data.shape)).tofile(F)

    return(None)

