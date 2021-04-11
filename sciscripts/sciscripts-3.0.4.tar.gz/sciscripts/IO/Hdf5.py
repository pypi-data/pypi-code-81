# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Functions for manipulating hdf5 files.
"""

import h5py, os
import numpy as np

from sciscripts.IO import Txt


## Level 0
def Data2Hdf5(Data, Path, OpenedFile, Overwrite=False):
    if type(Data) == dict:
        for K, Key in Data.items(): Data2Hdf5(Key, Path+'/'+K, OpenedFile, Overwrite)

    elif type(Data) == list:
        Skip = False
        for d, D in enumerate(Data):
            if type(D) in [list, tuple] or 'numpy' in str(type(D)):
                Skip = True
                Data2Hdf5(D, Path+'/'+'ToMerge'+'_'+str(d), OpenedFile, Overwrite)

        if Skip: return(None)

        if True in [D == str(D) for D in Data]: Data = np.string_(Data)
        if Overwrite:
            if Path in OpenedFile: del(OpenedFile[Path])

        else: OpenedFile[Path] = Data

    elif type(Data) == tuple or 'numpy' in str(type(Data)):
        if Overwrite:
            if Path in OpenedFile: del(OpenedFile[Path])

        OpenedFile[Path] = Data

    elif type(Data) == str:
        if Path not in OpenedFile: OpenedFile.create_group(Path)
        OpenedFile[Path] = np.string_(Data)

    else: print('Data type', type(Data), 'at', Path, 'not understood.')

    return(None)


def Hdf52Dict(Path, F, StructureOnly=False, Copy=False):
    Dict = {}; Attrs = {}
    if type(F[Path]) == h5py._hl.group.Group:
        if list(F[Path].attrs):
            for Att in F[Path].attrs.keys(): Attrs[Att] = Hdf52Dict(Att, F[Path].attrs, StructureOnly, Copy)

        Keys = sorted(F[Path].keys())
        MergeKeys = [_ for _ in Keys if 'ToMerge' in _]

        if MergeKeys:
            MaxInd = max([int(_.split('_')[1]) for _ in MergeKeys])+1
            ToMerge = [[] for _ in range(MaxInd)]
            A = [[] for _ in range(MaxInd)]

            for Group in MergeKeys:
                Ind = int(Group.split('_')[1])
                ToMerge[Ind], A[Ind] = Hdf52Dict(Path+'/'+Group, F, StructureOnly, Copy)

            return(ToMerge, A)

        for Group in F[Path].keys(): Dict[Group], Attrs[Group] = Hdf52Dict(Path+'/'+Group, F, StructureOnly, Copy)
        return(Dict, Attrs)

    elif type(F[Path]) == h5py._hl.dataset.Dataset:
        if list(F[Path].attrs):
            for Att in F[Path].attrs.keys(): Attrs[Att] = Hdf52Dict(Att, F[Path].attrs, StructureOnly, Copy)

        if StructureOnly: return(None)
        else:
            if Copy: return(F[Path][()], Attrs)
            else: return(F[Path], Attrs)

    elif 'numpy' in str(type(F[Path])) or type(F[Path]) in [str, list, tuple, dict]:
        if StructureOnly: return(None)
        else: return(F[Path])

    else:
        print('Type', type(F[Path]), 'not supported.')
        return(None)


def ReturnCopy(Dataset):
    Array = np.zeros(Dataset.shape, dtype=Dataset.dtype)
    try:
        Dataset.read_direct(Array)
    except Exception as e:
        print("ERROR:", e)
        print(Dataset)
        print(Array)
        print('='*60)
        print('')

    if Array.size == 1: Array = Array[()]
    return(Array)


## Level 1
def DatasetLoad(Path, File):
    F = h5py.File(File, 'r')
    if Copy:
        Dataset = F[Path][()]
        F.close()
    else:
        Dataset = F[Path]

    return(Dataset)


def Load(Path, File, StructureOnly=False, Copy=False):
    F = h5py.File(File, 'r')
    Data, Attrs = Hdf52Dict(Path, F, StructureOnly, Copy)
    if Copy: F.close()

    return(Data, Attrs)


def Write(Data, Path, File, Overwrite=False):
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)

    with h5py.File(File, 'a') as F: Data2Hdf5(Data, Path, F, Overwrite)

    return(None)


# Level 2
def Hdf5Info2TxtInfo(Files):
    """
    Function for converting old .hdf5 InfoFiles to new .dict InfoFiles.
    """
    for File in Files:
        a,b = Load('/',File)
        Info = {**b['DataInfo'], **a['DataInfo']}
        Info = Txt.Dict_OldToNew(Info)
        Info['Animal']['StimType'] = ['Sound', File.split('/')[7].split('-')[1]]
        if type(Info['DAqs']['RecCh']) not in [list, np.ndarray]:
            Info['DAqs']['RecCh'] = [Info['DAqs']['RecCh']]
        Txt.Write(Info, File[:-4]+'dict')

    return(None)
