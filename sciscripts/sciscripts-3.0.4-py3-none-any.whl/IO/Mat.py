# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Functions for manipulating general .mat files.
"""

import numpy as np
import os
from scipy import io#, signal


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


def Read(File, loadmatArgs={}):
    Args = {'squeeze_me': True, 'struct_as_record': False, 'simplify_cells': False}
    Args = {**Args, **loadmatArgs}
    S = io.loadmat(File, **Args)
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


