# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Functions for manipulating specific .mat files.
"""

import numpy as np
import os
# from glob import glob
from scipy import io#, signal

# from sciscripts.Analysis.Analysis import FilterSignal
# from sciscripts.Analysis import GPIAS
# from sciscripts.IO import Asdf, Hdf5

def StructToData(Struct):
    if type(Struct) == dict:
        Data = {K: StructToData(V) for K,V in Struct.items()}
    elif type(Struct) in [list, tuple, np.ndarray]:
        Data = [StructToData(_) for _ in Struct]
    elif 'struct' in str(type(Struct)):
        S = {K: getattr(Struct, K) for K in dir(Struct) if K[0] != '_'}
        Data = {K: StructToData(V) for K,V in S.items()}
    else:
        Data = Struct

    if np.array(Data).dtype != np.dtype('O') \
        and type(Data) not in [int, float, str]:
        Data = np.array(Data)

    return(Data)


def Read(File):
    S = io.loadmat(File, squeeze_me=True, struct_as_record=False)#, simplify_cells=True)
    Data = StructToData(S)
    return(Data)


def Write(Data, File):
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)

    if type(Data) != dict:
        io.savemat(File, {'Data': Data})
    else:
        io.savemat(File, Data)

    return(None)


def Fig2Dict(Fig, Dict={}):
    for K in ['Data', 'Color', 'LineStyle', 'LineLabel', 'SubPlot', 'Title', 'XLabel', 'YLabel']:
        if K not in Dict: Dict[K] = []

    if type(Fig) == dict:
        Keys = [k for k in Fig.keys() if k[0] != '_']

        if 'properties' in Keys:
            if 'ApplicationData' in Fig['properties']:
                if 'SubplotGridLocation' in Fig['properties']['ApplicationData']:
                    Dict['_CurrentSubPlot'] = Fig['properties']['ApplicationData']['SubplotGridLocation']

            if  'Rotation' in Fig['properties'] \
                and 'String' in Fig['properties'] \
                and 'Description' in Fig['properties']:

                if Fig['properties']['Description'] == 'AxisRulerBase Label':
                    if Fig['properties']['Rotation'] == 0:
                        Dict['_CurrentXLabel'] = Fig['properties']['String']
                    elif Fig['properties']['Rotation'] == 90:
                        Dict['_CurrentYLabel'] = Fig['properties']['String']

                elif Fig['properties']['Description'] == 'Axes Title':
                    Dict['_CurrentTitle'] = Fig['properties']['String']
                    if type(Dict['_CurrentTitle']) == np.ndarray:
                        Dict['_CurrentTitle'] = '\n'.join(Dict['_CurrentTitle'])

            if 'XData' in Fig['properties']:
                Dict['Data'] += [np.array([
                    Fig['properties'][_+'Data']
                    for _ in ['X', 'Y', 'Z']
                    if _+'Data' in Fig['properties']
                ]).T]

                if 'DisplayName' in Fig['properties']:
                    DN = Fig['properties']['DisplayName']
                else:
                    DN = ''

                Color = Fig['properties']['Color'] if 'Color' in Fig['properties'] else np.array([0,0,0])
                LineStyle = Fig['properties']['LineStyle'] if 'LineStyle' in Fig['properties'] else 'none'
                Dict['Color'] += [Color]
                Dict['LineStyle'] += [LineStyle]
                Dict['LineLabel'] += [DN]

                for Info in ['SubPlot', 'Title', 'XLabel', 'YLabel']:
                    if '_Current'+Info in Dict:
                        Dict[Info] += [Dict['_Current'+Info]]
                    else:
                        Dict[Info] += ['']

        for K,V in Fig.items():
            if K == 'properties': continue
            if K == 'children' and type(V) != dict: continue
            Fig2Dict(V, Dict)

        if 'children' in Keys and type(Fig['children']) != dict:
            for Children in reversed(Fig['children']):
                Fig2Dict(Children, Dict)

    return(Dict)


# def DataToMMSS(FileName, StimType=['Sound'], Override={}):
#     DirList = glob('KwikFiles/*'); DirList.sort()
#     for Stim in StimType:
#         if Override != {}:
#             if 'Stim' in Override.keys():
#                 Stim = Override['Stim']
#
#         Exps = Hdf5.ExpPerStimLoad(Stim, DirList, FileName)
#
#         for FInd, RecFolder in enumerate(Exps):
#             Path = os.getcwd() + '/' + RecFolder
#             ClusterFile = Path + '/SpkClusters.hdf5'
#             Clusters = Hdf5.ClustersLoad(ClusterFile)
#
#             Path = os.getcwd() + '/' + RecFolder +'/SepRec/'
#             os.makedirs(Path, exist_ok=True)
#
#             for Rec in Clusters.keys():
#                 RecS = "{0:02d}".format(int(Rec))
#
#                 print('Writing files for clustering... ', end='')
#                 WF = []; ST = []; ChList = []
#                 for Ch in Clusters[RecS].keys():
#                     WF.append(Clusters[RecS][Ch]['Spikes'][:])
#                     ST.append(Clusters[RecS][Ch]['Timestamps'][:])
#                     ChList.append(Ch)
#
#                 data = {'waveforms': np.array(WF, dtype='object'),
#                         'spiketimes': np.array(ST, dtype='object'),
#                         'ChList': np.string_(ChList)}
#
#                 MatName = ''.join(['Exp_', RecS, '.mat'])
#                 io.savemat(Path+MatName, {'data': data})
#                 print('Done.')
#     return(None)
#
#
# def KlustaPSTH2Mat(DataFiles, MatFile):
#     FiringPattern = {}
#     for A, DataFile in enumerate(DataFiles):
#         UnitRec = Asdf.Read(DataFile)
#         if not UnitRec['PSTH']: continue
#         print(DataFile)
#
#         Key = 'File'+str(A)
#         FiringPattern[Key] = np.array([], dtype='float32')
#         FiringPattern[Key+'_StimType'] = np.array([], dtype=UnitRec['StimType'].dtype)
#         for U, Unit in enumerate(UnitRec['PSTH']):
#             if not Unit.mean(): continue
#             if UnitRec['SpkResp'][U] > 0.05: continue
#
#             FP = Unit.mean(axis=1)
#
#             FiringPattern[Key+'_StimType'] = np.hstack((FiringPattern[Key+'_StimType'],
#                                                         UnitRec['StimType'][U]))
#             if not len(FiringPattern[Key]): FiringPattern[Key] = np.array([FP]).T
#             else: FiringPattern[Key] = np.hstack((FiringPattern[Key],
#                                                      np.array([FP]).T))
#
#         if not len(FiringPattern[Key]):
#             del(FiringPattern[Key])
#             del(FiringPattern[Key+'_StimType'])
#
#     io.savemat(MatFile, FiringPattern)
#
#
# def GPIASMat2Asdf(Folders, Freqs):
#     # Folders = sorted(glob(os.environ['DATAPATH']+'/../DeadFiles/Data/Recovery/2016021?-Recovery-GPIAS'))
#     # Freqs = [[8000,10000],[10000,12000],[12000,14000],[14000,16000]]
#
#     for Folder in Folders:
#         Animals = sorted([_[:-1] for _ in glob(Folder+'/*/')])
#         InfoFiles = sorted(glob(Folder+'/*.mat'))
#
#         for A,Animal in enumerate(Animals):
#             Files = glob(Animal+'/*.mat')
#
#             GPIASData = GPIAS.PreallocateDict(Freqs)
#
#             for File in Files:
#                 Freq = '-'.join([str(int(_)*1000) for _ in File.split('F')[-1].split('.')[0].split('_')])
#                 Data = io.loadmat(File)
#
#                 for Key in ['IndexTrace', 'Trace']:
#                     for Tr in ['Gap', 'NoGap']: GPIASData[Key][Freq][Tr].append(Data[Tr][0,:]*1000)
#
#             DataInfo = io.loadmat(InfoFiles[A])
#             GPIASData['Rate'] = DataInfo['Rate'][0]
#             GPIASData['TTLs'] = DataInfo['PulseStart'][0]
#
#             GPIASData = {'100': GPIASData}
#
#             Asdf.Write(GPIASData, Animal.split('..')[0] + '/'.join(Animal.split('..')[1].split('/')[3:])+'.asdf')

