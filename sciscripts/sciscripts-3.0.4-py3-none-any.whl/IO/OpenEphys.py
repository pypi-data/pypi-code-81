#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170708
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import OpenEphys, SettingsXML
import numpy as np
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.IO import Bin, Hdf5, Txt


## Level 0
def ApplyChannelMap(Data, ChannelMap):
    print('Retrieving channels according to ChannelMap... ', end='')
    ChannelMap = [_-1 for _ in ChannelMap]
    for R, Rec in Data.items():
        if Rec.shape[1] < len(ChannelMap):
            print('Not remapping rec', R+':', 'not enough channels in recording.')
            continue

        Data[R] = Data[R][:,ChannelMap]

    return(Data)


def BitsToVolts(Data, ChInfo, Unit):
    if Unit.lower() == 'uv': U = 1
    elif Unit.lower() == 'mv': U = 10**-3

    for R in Data.keys():
        for C, Ch in enumerate(sorted(ChInfo.keys(), key=lambda x: int(x))):
            # print(ChInfo[Ch]['name'])
            Data[R][:,C] = Data[R][:,C] * float(ChInfo[Ch]['gain']) * U
            if 'ADC' in ChInfo[Ch]['name']: Data[R][:,C] *= 10**6


    return(Data)


def ChooseProcs(XMLFile, Procs):
    ProcList = SettingsXML.GetRecChs(XMLFile)[1]
    ProcList = {Id: Name for Id, Name in ProcList.items() if Id in Procs}

    print(Txt.Print(ProcList))
    Procs = input('Which Procs should be kept (comma separated) ? ')
    Procs = [_ for _ in Procs.split(',')]

    return(Procs)


def DataTouV(Data, RecChs, Unit):
    print('Converting to uV... ', end='')
    Data = {R: Rec.astype('float32') for R, Rec in Data.items()}
    Data = BitsToVolts(Data, RecChs, Unit)

    return(Data)


def EventsLoad(Folder):
    Files = sorted(glob(Folder+'/*.events'))
    if len(Files) > 1: print('Multiple sessions not supported yet.'); return(None)
#    for File in Files:
#        Session = File.split('.')[0].split('_')[-1]

    EventsDict = OpenEphys.loadEvents(Folder+'/'+Files[0])
    return(EventsDict)


def GetChNoAndProcs(File):
    ChNo, Procs = SettingsXML.GetRecChs(File)
    if len(ChNo) > 1:
        Proc = [K for K,V in Procs.items() if 'FPGA'in V][0]
    else:
        Proc = list(ChNo.keys())[0]
    ChNo = len(ChNo[Proc])

    return(ChNo, Proc)


def GetResistance(ImpedanceFile):
    Impedance = SettingsXML.XML2Dict(ImpedanceFile)
    Impedance = {C: Ch for C,Ch in Impedance['CHANNEL'].items()}
    Chs = sorted(Impedance.keys(), key=lambda x: int(x[2:]))

    ROhms = [
        abs(
            np.cos(float(Impedance[Ch]['phase'])) *
            float(Impedance[Ch]['magnitude'])
        )
        for C, Ch in enumerate(Chs)
    ]

    return(ROhms)


def VoltageToCurrent(Data, ImpedanceFile):
    print('Normalizing based on resistance of each channel... ', end='')
    Impedance = SettingsXML.XML2Dict(ImpedanceFile)
    Impedance = {C: Ch for C,Ch in Impedance['CHANNEL'].items()}

    for R in Data.keys():
        for C, Ch in enumerate(sorted(Impedance.keys(), key=lambda x: int(x[2:]))):
            ROhms = abs(np.cos(float(Impedance[Ch]['phase'])) * float(Impedance[Ch]['magnitude']))
            Data[R][:,C] /= ROhms

    return(Data)


## Level 1
def DatLoadOld(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None):
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

        if ChannelMap: Data[Proc] = ApplyChannelMap(Data[Proc], ChannelMap)
        if len(np.unique(Rate[Proc])) == 1: Rate[Proc] = Rate[Proc][0]

    return(Data, Rate)


def DatLoad(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None):
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

        if ChannelMap: Data[Proc] = ApplyChannelMap(Data[Proc], ChannelMap)
        if len(np.unique(Rate[Proc])) == 1: Rate[Proc] = Rate[Proc][0]

    return(Data, Rate)


def KwikLoad(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None):
    Kwds = sorted(glob(Folder+'/*.kwd'))
    if Unit.lower() == 'uv':
        XMLFile = sorted(glob(Folder+'/setting*.xml'))[0]
        RecChs = SettingsXML.GetRecChs(XMLFile)[0]

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Data = {}; Rate = {}
    for Kwd in Kwds:
        Exp, Proc = Kwd.split('/')[-1].split('_')[0][10:], Kwd.split('/')[-1].split('_')[1].split('.')[0]

        if Experiment:
            if Exp != Experiment: continue

        if Processor:
            if Proc != Processor: continue

        Data[Proc], Attrs = Hdf5.Load('/recordings', Kwd)

        if Recording:
            Data[Proc] = {R: Rec['data'] for R, Rec in Data[Proc].items() if R == Recording}
            Rate[Proc] = [np.array(int(Rec['sample_rate'])) for R,Rec in Attrs.items()  if R == Recording]
        else:
            Data[Proc] = {R: Rec['data'] for R, Rec in Data[Proc].items()}
            Rate[Proc] = [np.array(int(Rec['sample_rate'])) for Rec in Attrs.values()]

        if len(np.unique(Rate[Proc])) == 1: Rate[Proc] = Rate[Proc][0]

        try:
            if Unit.lower() == 'uv':
                Data[Proc] = DataTouV(Data[Proc], RecChs[Proc], Unit)
                if ImpedanceFile:
                    Data[Proc] = VoltageToCurrent(Data[Proc], ImpedanceFile)

        except KeyError:
            print('No gain info on file, units are in bits.')

        if ChannelMap: Data[Proc] = ApplyChannelMap(Data[Proc], ChannelMap)

    print('Done.')
    return(Data, Rate)


def OELoad(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Processor=None, Recording=None):
    OEs = glob(Folder+'/*continuous')

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Chs = [_.split('/')[-1] for _ in OEs]
    Procs = Analysis.UniqueStr([_[:3] for _ in Chs])

    Data = {_: {} for _ in Procs}; Rate = {_: {} for _ in Procs}
    Chs = {Proc: [_ for _ in Chs if _[:3] == Proc] for Proc in Procs}

    for P, Proc in Chs.items():
        Type = Chs[P][0].split('_')[-1].split('.')[0][:-1]
        print(Type)
        Chs[P] = sorted(Proc, key=lambda x: int(x.split('_'+Type)[1].split('_')[0].split('.')[0]))

    for Proc in Data.keys():
        if Processor:
            if Proc != Processor: continue

        ACh = Chs[Proc][0].split('.')[0]
        OEData = OpenEphys.loadFolder(Folder, source=Proc)
        Rate[Proc] = int(OEData[ACh]['header']['sampleRate'])

        Recs = np.unique(OEData[ACh]['recordingNumber'])
        BlockSize = int(OEData[ACh]['header']['blockLength'])
        for Rec in Recs:
            R = str(int(Rec))

            if Recording:
                if R != Recording: continue

            RecInd = np.where(OEData[ACh]['recordingNumber'].repeat(BlockSize) == Rec)
            Data[Proc][R] = [OEData[_.split('.')[0]]['data'][RecInd] for _ in Chs[Proc]]
            Data[Proc][R] = np.array(Data[Proc][R]).T

        if Unit.lower() == 'uv':
            ChsInfo = [OEData[_.split('.')[0]]['header']['bitVolts'] for _ in Chs[Proc]]
            ChsInfo = {str(Ch): {'gain': BitVolt} for Ch, BitVolt in enumerate(ChsInfo)}
            Data[Proc] = DataTouV(Data[Proc], ChsInfo)

            if ImpedanceFile:
                Data[Proc] = VoltageToCurrent(Data[Proc], ImpedanceFile)

        if ChannelMap: Data[Proc] = ApplyChannelMap(Data[Proc], ChannelMap)

    return(Data, Rate)


## Level 2
def GetRecs(Folder):
    FilesExt = [F[-3:] for F in glob(Folder+'/*.*')]

    if 'kwd' in FilesExt:
        Kwds = glob(Folder+'/*.kwd')

        for Kwd in Kwds:
            Proc = Kwd[-11:-8]

            Recs = {}
            Recs[Proc] = Hdf5.Load('/recordings', Kwd)[0]
            Recs[Proc] = [R for R in Recs[Proc].keys()]

    elif 'dat' in FilesExt:
        Files = glob(Folder+'/*.dat'); Files.sort()
        RecChs = SettingsXML.GetRecChs(Folder+'/settings.xml')[0]

        Recs = {Proc: [] for Proc in RecChs.keys()}

        for File in Files:
            _, Proc, Rec = File.split('/')[-1][10:-4].split('_')
            Recs[Proc].append(Rec)

    elif 'ous' in FilesExt:
        OEs = glob(Folder+'/*continuous')
        Chs = [_.split('/')[-1] for _ in OEs]
        Procs = Analysis.UniqueStr([_[:3] for _ in Chs])
        Recs = {}

        for Proc in Procs:
            ACh = Chs[Proc][0].split('.')[0]
            OEData = OpenEphys.loadFolder(Folder, source=Proc)
            R = np.unique(OEData[ACh]['recordingNumber'])
            Recs[Proc] = str(int(R))

    return(Recs)


def KwikToBin(Folders, Verbose=False):
    for Folder in Folders:
        Data, Rate = IO.DataLoader(Folder, 'bits')

        for P,Proc in Data.items():
            for R,Rec in Proc.items():
                File = 'experiment1_'+P+'_'+R+'.dat'
                File = Folder+'_Bin/'+File

                if Verbose:
                    print(Rec.dtype)
                    print(R)
                    print(File)
                    print()

                Bin.Write(Rec, File)

