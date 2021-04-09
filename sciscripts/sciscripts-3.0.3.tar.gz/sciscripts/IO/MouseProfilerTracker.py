#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20200920
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""
import numpy as np
from sciscripts.IO import XML


def TrackingRead(Files, CoordFiles, Recs, Behs=True, Coords=True):
    Data = {}
    for F, File in enumerate(Files):
        Rec = File.split('/')[-1].split('.')[0]
        Group, Rec = Recs[Rec]

        if Group not in Data.keys(): Data[Group] = {}
        Data[Group][Rec] = {}

        Root = XML.ReadTree(File)[1]
        CoordRoot = XML.ReadTree(CoordFiles[F])[1]


        if Behs:
            Data[Group][Rec]['Behaviours'] = {
                ''.join([b.capitalize() for b in Behav.get('type').split('_')]):
                    np.array([[Event.get('startFrame'), Event.get('endFrame')] for Event in Behav], dtype='int16')
                for Behav in Root}

        if Coords:
            Data[Group][Rec]['Coords'] = {}
            for Animal in CoordRoot[2]:
                if Animal.tag not in Data[Group][Rec]['Coords']:
                    Data[Group][Rec]['Coords'][Animal.tag] = {}

                Keys = list(Animal[0].keys())
                Data[Group][Rec]['Coords'][Animal.tag] = {Key: np.array([F.get(Key) for F in Animal], dtype='float32')
                                                          for Key in Keys if Key != 't'}

        Data[Group][Rec]['t'] = np.array([F.get('t') for F in CoordRoot[2][0]], dtype='float32')

    return(Data)


