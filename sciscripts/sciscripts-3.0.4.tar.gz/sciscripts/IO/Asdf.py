#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20171007
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np
import asdf

## Level 0
def Write(Data, File):
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
    with asdf.AsdfFile(Data) as F: F.write_to(File)

    return(None)


def ItemPop(I):
    if type(I) == list:
        if True in ['NDArrayType' in str(type(_)) for _ in I]:
            I = [ItemPop(_) for _ in I]
            return(I)
        else:
            return(I)

    elif type(I) == dict:
        I = {Key: ItemPop(Val) for Key, Val in I.items()}
        return(I)

    elif type(I) in [str, float, int]: return(I)

    elif 'NDArrayType' in str(type(I)):
        # I = np.array(I, dtype=I.dtype)
        I = I.copy()
        return(I)

    else:
        print('Type', type(I), 'not understood.')
        return(None)


## Level 1
def Read(File, Lazy=False):
    if Lazy:
        Dict = asdf.open(File, mode='r', copy_arrays=True)
        Dict = Dict.tree
        del(Dict['history'],Dict['asdf_library'])
    else:
        with asdf.open(File, mode='r') as F:
            Dict = {Key: ItemPop(F.tree.get(Key))
                    for Key in F.tree.keys() if 'asdf' not in Key or Key != 'history'}

            if 'history' in Dict.keys(): # somehow...
                del(Dict['history'],Dict['asdf_library'])

    return(Dict)

