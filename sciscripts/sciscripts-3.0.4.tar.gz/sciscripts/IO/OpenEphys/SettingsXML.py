#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170704

Loads info from the settings.xml file.

Examples:
    File = '/Path/To/Experiment/settings.xml

    # To get all info the xml file can provide:
    AllInfo = SettingsXML.XML2Dict(File)

    # AllInfo will be a dictionary following the same structure of the XML file.

    # To get the sampling rate used in recording:
    Rate = SettingsXML.GetSamplingRate(File)

    # To get info only about channels recorded:
    RecChs = SettingsXML.GetRecChs(File)[0]

    # To get also the processor names:
    RecChs, PluginNames = SettingsXML.GetRecChs(File)

    # RecChs will be a dictionary:
    #
    # RecChs
    #     ProcessorNodeId
    #         ChIndex
    #             'name'
    #             'number'
    #             'gain'
    #         'PluginName'

"""

from sciscripts.IO import XML


def FindRecProcs(Ch, Proc, RecChs):
    ChNo = Ch['number']
    Rec = Proc['CHANNEL'][ChNo]['SELECTIONSTATE']['record']

    if Rec == '1':
        if Proc['NodeId'] not in RecChs: RecChs[Proc['NodeId']] = {}
        RecChs[Proc['NodeId']][ChNo] = Ch

    return(RecChs)


def GetSamplingRate(File):
    Info = XML.Read(File)
    Error = 'Cannot parse sample rate. Check your settings.xml file at SIGNALCHAIN>PROCESSOR>Sources/Rhythm FPGA.'
    SignalChains = [_ for _ in Info.keys() if 'SIGNALCHAIN' in _]

    try:
        for SignalChain in SignalChains:
            if 'Sources/Rhythm FPGA' in Info[SignalChain]['PROCESSOR'].keys():
                if 'SampleRateString' in Info[SignalChain]['PROCESSOR']['Sources/Rhythm FPGA']['EDITOR']:
                    Rate = Info[SignalChain]['PROCESSOR']['Sources/Rhythm FPGA']['EDITOR']['SampleRateString']
                    Rate = float(Rate.split(' ')[0])*1000
                elif Info[SignalChain]['PROCESSOR']['Sources/Rhythm FPGA']['EDITOR']['SampleRate'] == '17':
                    Rate = 30000
                elif Info[SignalChain]['PROCESSOR']['Sources/Rhythm FPGA']['EDITOR']['SampleRate'] == '16':
                    Rate = 25000
                else:
                    Rate = None
            else:
                Rate = None

        if not Rate:
            print(Error); return(None)
        else:
            return(Rate)

    except Exception as Ex:
        print(Ex); print(Error); return(None)


def GetRecChs(File):
    Info = XML.Read(File)
    RecChs = {}; ProcNames = {}

    if len([k for k in Info if 'SIGNALCHAIN' in k]) > 1:
        for S in [k for k in Info if 'SIGNALCHAIN_' in k]:
            for P, Proc in Info[S]['PROCESSOR'].items():
                Info['SIGNALCHAIN']['PROCESSOR'][P+'_'+S[-1]] = Proc
            del(Info[S])

    for P, Proc in Info['SIGNALCHAIN']['PROCESSOR'].items():
        if 'isSource' in Proc:
            if Proc['isSource'] == '1': SourceProc = P[:]
        else:
            if Proc['name'].split('/')[0] == 'Sources': SourceProc = P[:]

        if 'CHANNEL_INFO' in Proc and Proc['CHANNEL_INFO']:
            for Ch in Proc['CHANNEL_INFO']['CHANNEL'].values():
                RecChs = FindRecProcs(Ch, Proc, RecChs)

        elif 'CHANNEL' in Proc:
            for Ch in Proc['CHANNEL'].values():
                RecChs = FindRecProcs(Ch, Proc, RecChs)

        else: continue

        if 'pluginName' in Proc:
            ProcNames[Proc['NodeId']] = Proc['pluginName']
        else:
            ProcNames[Proc['NodeId']] = Proc['name']

    if Info['SIGNALCHAIN']['PROCESSOR'][SourceProc]['CHANNEL_INFO']:
        SourceProc = Info['SIGNALCHAIN']['PROCESSOR'][SourceProc]['CHANNEL_INFO']['CHANNEL']
    else:
        SourceProc = Info['SIGNALCHAIN']['PROCESSOR'][SourceProc]['CHANNEL']

    for P, Proc in RecChs.items():
        for C, Ch in Proc.items():
            if 'gain' not in Ch:
                RecChs[P][C].update([c for c in SourceProc.values() if c['number'] == C][0])

    return(RecChs, ProcNames)

