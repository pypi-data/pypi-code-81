#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: malfatti
@date: 2019-07-27

Loads data recorded by Open Ephys in Binary format as dictionary with numpy
memmaps.

Warning:
    Data placed inside dictionaries is affected when passed to functions.
    Therefore, if you do, for example:

        FilteredData = MyFilterFunction(Data['100']['0']['0'], Rate['100']['0'], Frequencies)

    the data in Data['100']['0']['0'] will be filtered! To avoid this behaviour, pass the
    data with the .copy() method:

        FilteredData = MyFilterFunction(Data['100']['0']['0'].copy(), Rate['100']['0'], Frequencies)

    then the data in Data['100']['0']['0'] will remain unaltered.

"""

import numpy as np
from ast import literal_eval
from glob import glob

from sciscripts.IO.OpenEphys import OpenEphys


def Load(Folder, Processor=None, Experiment=None, Recording=None, Unit='uV', ChannelMap=[], ImpedanceFile=''):
    """
    Loads data recorded by Open Ephys in Binary format as numpy memmap.

        DatLoad(Folder, Processor=None, Experiment=None, Recording=None, Unit='uV', ChannelMap=[])

    Parameters
        Folder: str
            Folder containing at least the subfolder 'experiment1'.

        Processor: str or None, optional
            Processor number to load, according to subsubsubfolders under
            Folder>experimentX/recordingY/continuous . The number used is the one
            after the processor name. For example, to load data from the folder
            'Channel_Map-109_100.0' the value used should be '109'.
            If not set, load all processors.

        Experiment: int or None, optional
            Experiment number to load, according to subfolders under Folder.
            If not set, load all experiments.

        Recording: int or None, optional
            Recording number to load, according to subsubfolders under Folder>experimentX .
            If not set, load all recordings.

        Unit: str or None, optional
            Unit to return the data, either 'uV' or 'mV' (case insensitive). In
            both cases, return data in float32. Defaults to 'uV'.
            If anything else, return data in int16.

        ChannelMap: list, optional
            If empty (default), load all channels.
            If not empty, return only channels in ChannelMap, in the provided order.
            CHANNELS ARE COUNTED STARTING AT 0.

    Returns:
        Data: dict
            Dictionary with data in the structure Data[Processor][Experiment][Recording].

        Rate: dict
            Dictionary with sampling rates in the structure Rate[Processor][Experiment].


    Example:
        import Binary

        Folder = '/home/user/PathToData/2019-07-27_00-00-00'
        Data, Rate = Binary.Load(Folder)

        ChannelMap = [0,15,1,14]
        Recording = 3
        Data2, Rate2 = Binary.Load(Folder, Recording=Recording, ChannelMap=ChannelMap, Unit='Bits')

    Warning:
        Data placed inside dictionaries is affected when passed to functions.
        Therefore, if you do, for example:

            FilteredData = MyFilterFunction(Data['100']['0']['0'], Rate['100']['0'], Frequencies)

        the data in Data['100']['0']['0'] will be filtered! To avoid this behaviour, pass the
        data with the .copy() method:

            FilteredData = MyFilterFunction(Data['100']['0']['0'].copy(), Rate['100']['0'], Frequencies)

        then the data in Data['100']['0']['0'] will remain unaltered.
    """
    Files = sorted(glob(Folder+'/**/*.dat', recursive=True))
    InfoFiles = sorted(glob(Folder+'/*/*/structure.oebin'))

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Data, Rate = {}, {}
    for F,File in enumerate(Files):
        Exp, Rec, _, Proc = File.split('/')[-5:-1]
        Exp = str(int(Exp[10:])-1)
        Rec = str(int(Rec[9:])-1)
        Proc = Proc.split('.')[0].split('-')[-1]
        if '_' in Proc: Proc = Proc.split('_')[0]

        if Proc not in Data.keys(): Data[Proc], Rate[Proc] = {}, {}

        if Experiment:
            if int(Exp) != Experiment-1: continue

        if Recording:
            if int(Rec) != Recording-1: continue

        if Processor:
            if Proc != Processor: continue

        print('Loading recording', int(Rec)+1, '...')
        if Exp not in Data[Proc]: Data[Proc][Exp] = {}
        Data[Proc][Exp][Rec] = np.memmap(File, dtype='int16', mode='c')


        Info = literal_eval(open(InfoFiles[F]).read())
        ProcIndex = [Info['continuous'].index(_) for _ in Info['continuous']
                     if str(_['source_processor_id']) == Proc][0]

        ChNo = Info['continuous'][ProcIndex]['num_channels']
        if Data[Proc][Exp][Rec].shape[0]%ChNo:
            print('Rec', Rec, 'is broken')
            del(Data[Proc][Exp][Rec])
            continue

        SamplesPerCh = Data[Proc][Exp][Rec].shape[0]//ChNo
        Data[Proc][Exp][Rec] = Data[Proc][Exp][Rec].reshape((SamplesPerCh, ChNo))
        Rate[Proc][Exp] = Info['continuous'][ProcIndex]['sample_rate']

    for Proc in Data.keys():
        for Exp in Data[Proc].keys():
            if Unit.lower() in ['uv', 'mv']:
                ChInfo = Info['continuous'][ProcIndex]['channels']
                Data[Proc][Exp] = OpenEphys.BitsToVolts(Data[Proc][Exp], ChInfo, Unit)

            if ImpedanceFile:
                Data[Proc][Exp] = OpenEphys.VoltageToCurrent(Data[Proc][Exp], ImpedanceFile)

            if ChannelMap: Data[Proc][Exp] = OpenEphys.ApplyChannelMap(Data[Proc][Exp], ChannelMap)

    print('Done.')

    return(Data, Rate)


def LoadOld(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None):
    """
    Loads data recorded by Open Ephys in Binary format as numpy memmap.
    Specific for loading files recorded from a time when Open Ephys binary
    files were all on a single folder.
    """
    Files = sorted(glob(Folder+'/*.dat'))
    RecChs = SettingsXML.GetRecChs(Folder+'/settings.xml')[0]

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Data = {Proc: {} for Proc in RecChs.keys()}
    Rate = {Proc: [] for Proc in RecChs.keys()}
    for File in Files:
        Exp, Proc, Rec = File.split('/')[-1][10:-4].split('_')

        if Experiment:
            if Exp != Experiment: continue

        if Recording:
            if Rec != Recording: continue

        if Processor:
            if Proc != Processor: continue


        Data[Proc][Rec] = np.memmap(File, dtype='int16')
        Rate[Proc] = SettingsXML.GetSamplingRate(Folder+'/settings.xml')
        Rate[Proc] = [np.array(Rate[Proc])]

        ChNo = len(RecChs[Proc])
        if Data[Proc][Rec].shape[0]%ChNo:
            print('Rec', Rec, 'is broken')
            del(Data[Proc][Rec])
            continue

        SamplesPerCh = Data[Proc][Rec].shape[0]//ChNo

        Data[Proc][Rec] = Data[Proc][Rec].reshape((SamplesPerCh, ChNo))

    for Proc in Data.keys():
        if Unit.lower() in ['uv', 'mv']:
            Data[Proc] = DataTouV(Data[Proc], RecChs[Proc], Unit)
            if ImpedanceFile:
                Data[Proc] = VoltageToCurrent(Data[Proc], ImpedanceFile)

        if ChannelMap: Data[Proc] = OpenEphys.ApplyChannelMap(Data[Proc], ChannelMap)
        if len(np.unique(Rate[Proc])) == 1: Rate[Proc] = Rate[Proc][0]

    return(Data, Rate)


def LoadXML(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None):
    """
    Loads data recorded by Open Ephys in Binary format as numpy memmap.
    Specific for loading files recorded from a time when Open Ephys binary
    files had no .oebin auxiliary file, so all info had to be extracted from
    the settings.xml file.
    """
    Files = sorted(glob(Folder+'/**/*.dat', recursive=True))
    RecChs = SettingsXML.GetRecChs(Folder+'/settings.xml')[0]

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Data = {Proc: {} for Proc in RecChs.keys()}
    Rate = {Proc: [] for Proc in RecChs.keys()}
    for File in Files:
        Exp, Rec, _, Proc = File.split('/')[-5:-1]
        print('Loading', Rec, '...')
        Exp = str(int(Exp[10:])-1)
        Rec = str(int(Rec[9:])-1)
        Proc = Proc.split('.')[0].split('-')[-1]
        if '_' in Proc: Proc = Proc.split('_')[0]

        if Experiment:
            if Exp != Experiment: continue

        if Recording:
            if Rec != Recording: continue

        if Processor:
            if Proc != Processor: continue

        Data[Proc][Rec] = np.memmap(File, dtype='int16')
        Rate[Proc] = SettingsXML.GetSamplingRate(Folder+'/settings.xml')
        Rate[Proc] = [np.array(Rate[Proc])]

        # with open(File, 'rb') as F: Raw = F.read()
        # Data[Proc][Rec] = np.fromstring(Raw, 'int16')
        ChNo = len(RecChs[Proc])
        if Data[Proc][Rec].shape[0]%ChNo:
            print('Rec', Rec, 'is broken')
            del(Data[Proc][Rec])
            continue

        SamplesPerCh = Data[Proc][Rec].shape[0]//ChNo

        Data[Proc][Rec] = Data[Proc][Rec].reshape((SamplesPerCh, ChNo))

    for Proc in Data.keys():
        if Unit.lower() in ['uv', 'mv']:
            Data[Proc] = DataTouV(Data[Proc], RecChs[Proc], Unit)
            if ImpedanceFile:
                Data[Proc] = VoltageToCurrent(Data[Proc], ImpedanceFile)

        if ChannelMap: Data[Proc] = OpenEphys.ApplyChannelMap(Data[Proc], ChannelMap)
        if len(np.unique(Rate[Proc])) == 1: Rate[Proc] = Rate[Proc][0]

    return(Data, Rate)


