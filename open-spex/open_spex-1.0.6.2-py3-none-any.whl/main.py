#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:29:46 2020

@author: Anders Ringbom; Swedish Defence Research Agency (FOI)
         anders.ringbom@foi.se

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import sys
sys.path.append('/home/ringbom/Source_svn/Source/trunk/pyxe/spex/openSpex')

import wx
import os
import copy
import pickle
import locale
import webbrowser
import tempfile
from os import path

from open_spex import utils as ut
from open_spex import menu as menu
from open_spex import BGMeasurement as bg
from open_spex import BGSample as bgs
from open_spex import bgm as bgm
from open_spex import dialogs as di
from open_spex import measurementPanel as sp
from open_spex import helpOpenSpex as h
from open_spex import aboutMessage as ab
from open_spex import xenonSampleSet as xs
from open_spex import optionsPanel as op
from open_spex import plotPanel as pp
from open_spex import version

LICENSE = """
MIT License

Copyright (c) 2021 Swedish Defence Research Agency (FOI)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

VERSION = version.version

font = 'Liberation Mono'
if os.name == 'nt':
    font = 'Courier New'

class mainFrame(wx.Frame):
    """
    Main frame for the xenon analysis tool 'openSpex'
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(1500,900), pos = (100,50))
        locale.setlocale(locale.LC_ALL, '')
        self.version = VERSION
        self.options = op.options()
        self.bgsample = None
        self.sample = None
        self.gasbk = None
        self.detbk = None
        self.qc = None
        self.calib = None
        self.mset = None
        self.tweakedLastSample = False
        self.tweakedLastGasbk = False
        
        #Menu
        self.menu = menu.menu()
        self.SetMenuBar(self.menu)
        self.Bind(wx.EVT_MENU, self.OpenPHD, self.menu.openSample)
        self.Bind(wx.EVT_MENU, self.OpenPHD, self.menu.openGasbk)
        self.Bind(wx.EVT_MENU, self.OpenPHD, self.menu.openDetbk)
        self.Bind(wx.EVT_MENU, self.OpenPHD, self.menu.openQC)
        self.Bind(wx.EVT_MENU, self.OpenPHD, self.menu.openCalib)
        self.Bind(wx.EVT_MENU, self.PrintPHD, self.menu.printSample)
        self.Bind(wx.EVT_MENU, self.PrintPHD, self.menu.printGasbk)
        self.Bind(wx.EVT_MENU, self.PrintPHD, self.menu.printDetbk)
        self.Bind(wx.EVT_MENU, self.PrintPHD, self.menu.printQC)
        self.Bind(wx.EVT_MENU, self.PrintPHD, self.menu.printCalib)
        self.Bind(wx.EVT_MENU, self.OnReadObject, self.menu.openMeasurement)
        self.Bind(wx.EVT_MENU, self.OnReadObject, self.menu.openDataset)
        self.Bind(wx.EVT_MENU, self.OnClearLog, self.menu.clearLog)
        self.Bind(wx.EVT_MENU, self.OnQuit, self.menu.quit)
        self.Bind(wx.EVT_MENU, self.OnSavePHD, self.menu.saveSamplePHD)
        self.Bind(wx.EVT_MENU, self.OnSavePHD, self.menu.saveGasbkPHD)
        self.Bind(wx.EVT_MENU, self.OnSavePHD, self.menu.saveDetbkPHD)
        self.Bind(wx.EVT_MENU, self.OnSavePHD, self.menu.saveQCPHD)
        self.Bind(wx.EVT_MENU, self.OnSavePHD, self.menu.saveCalibPHD)
        self.Bind(wx.EVT_MENU, self.OnSaveReport, self.menu.saveMeasurementReport)
        self.Bind(wx.EVT_MENU, self.OnSaveReport, self.menu.saveMeasurementsetReport)
        self.Bind(wx.EVT_MENU, self.OnSaveObject, self.menu.saveMeasurement)
        self.Bind(wx.EVT_MENU, self.OnSaveObject, self.menu.saveDataset)
        self.Bind(wx.EVT_MENU, self.OnSaveMsetCSV, self.menu.saveDatasetCSV)
        self.Bind(wx.EVT_MENU, self.OnAnalyze, self.menu.analyze)
        self.Bind(wx.EVT_MENU, self.OnUnmarkMset, self.menu.unmarkMset)
        self.Bind(wx.EVT_MENU, self.OnClearMea, self.menu.clearMea)
        self.Bind(wx.EVT_MENU, self.OnCalcMset, self.menu.calcMsetFile)
        self.Bind(wx.EVT_MENU, self.OnReportMset, self.menu.reportMset)
        self.Bind(wx.EVT_MENU, self.OnPlotMset, self.menu.plotMset)
        self.Bind(wx.EVT_MENU, self.OnFreqMset, self.menu.freqMset)
        self.Bind(wx.EVT_MENU, self.OnAppendMset, self.menu.appendMset)
        self.Bind(wx.EVT_MENU, self.OnMircMset, self.menu.mirc3Mset)
        self.Bind(wx.EVT_MENU, self.OnMircMset, self.menu.mirc4Mset)
        self.Bind(wx.EVT_MENU, self.OnPlotParam, self.menu.plotXeVol)
        self.Bind(wx.EVT_MENU, self.OnPlotParam, self.menu.plotXeYield)
        self.Bind(wx.EVT_MENU, self.OnPlotParam, self.menu.plotAirVol)
        self.Bind(wx.EVT_MENU, self.OnPlotParam, self.menu.plotErrors)
        self.Bind(wx.EVT_MENU, self.OnClearMset, self.menu.clearMset)
        self.Bind(wx.EVT_MENU, self.OnOptions, self.menu.options)
        self.Bind(wx.EVT_MENU, self.OnHelp, self.menu.help)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.menu.about)

        #Splitter and panels
        splitter = wx.SplitterWindow(self)
        
        #Right panel
        rightP = wx.Panel(splitter)
        self.nb = wx.Notebook(rightP)
        self.tab_sample = sp.measurementPanel(self.nb, self.options)
        self.tab_gasbk = sp.measurementPanel(self.nb, self.options)
        self.tab_detbk = sp.measurementPanel(self.nb, self.options)
        self.tab_qc = sp.measurementPanel(self.nb, self.options)
        self.tab_calib = sp.measurementPanel(self.nb, self.options)
        self.tab_plot = wx.Panel(self.nb)
        self.nb.AddPage(self.tab_sample, "Sample")
        self.nb.AddPage(self.tab_gasbk, "Gasbk")
        self.nb.AddPage(self.tab_detbk, "Detbk")
        self.nb.AddPage(self.tab_qc, "QC")
        self.nb.AddPage(self.tab_calib, "Calib")
        self.nb.AddPage(self.tab_plot, "Plot")
        nb_sizer = wx.BoxSizer()
        nb_sizer.Add(self.nb, 1, wx.EXPAND)
        rightP.SetSizer(nb_sizer)
        
        #Left panel
        leftP = wx.Panel(splitter)
        self.nb2 = wx.Notebook(leftP)
        self.tab_log = wx.TextCtrl(self.nb2, style= wx.TE_MULTILINE)
        self.tab_log.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0,
font)) 
        self.nb2.AddPage(self.tab_log, "Log")
        nb2_sizer = wx.BoxSizer()
        nb2_sizer.Add(self.nb2, 1, wx.EXPAND | wx.LEFT, border = 10)
        leftP.SetSizer(nb2_sizer)
        sys.stdout = self.tab_log
        
        #Split screen
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(100)
        split_sizer = wx.BoxSizer(wx.VERTICAL)
        split_sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(split_sizer)
        splitter.SetSashPosition(550)
        
    def OnQuit(self, event):
        """Close the main frame"""
        self.Close(True)
        
    def OnClearLog(self, event):
        """Clear the log window"""
        self.tab_log.Clear()
        
    def OnHelp(self,event):
        """Show the help menu in default browser"""
        fh, path = tempfile.mkstemp(suffix='.html')
        url = 'file://' + path
        with open(path, 'w') as fp:
            fp.write(h.HELPTEXT)
        webbrowser.open(url, new = 2)
        
    def OnAbout(self,event):
        """Show 'about' information"""
        info = format('This is openSpexF version %s\n\nAuthor: Anders Ringbom, Swedish Defence Research Agency (FOI)\n' %self.version)
        info += LICENSE
        ab.about(self, info).Show()
        
    def OnOptions(self, event):
        """Create the options panel with current options"""
        optpan = op.optionsPanel(self,"Options",self.options)
        optpan.Show()
        self.Bind(op.EVT_OPTIONS_SAVED, self.OnSaveOptions)
        
    def OnSaveOptions(self,event):
        """Immediate actions when options are changed"""
        #Set histogram plot options in measurement panels
        if self.tab_sample.lowerPanel.hglist:
            self.tab_sample.lowerPanel.hgbox.useCountrate = self.options.histScaleCountrate
        if self.tab_sample.lowerPanel.hblist:
            self.tab_sample.lowerPanel.hbbox.useCountrate = self.options.histScaleCountrate
        if self.tab_gasbk.lowerPanel.hglist:
            self.tab_gasbk.lowerPanel.hgbox.useCountrate = self.options.histScaleCountrate
        if self.tab_gasbk.lowerPanel.hblist:
            self.tab_gasbk.lowerPanel.hbbox.useCountrate = self.options.histScaleCountrate
        if self.tab_detbk.lowerPanel.hglist:
            self.tab_detbk.lowerPanel.hgbox.useCountrate = self.options.histScaleCountrate
        if self.tab_detbk.lowerPanel.hblist:
            self.tab_detbk.lowerPanel.hbbox.useCountrate = self.options.histScaleCountrate
        if self.tab_qc.lowerPanel.hglist:
            self.tab_qc.lowerPanel.hgbox.useCountrate = self.options.histScaleCountrate
        if self.tab_qc.lowerPanel.hblist:
            self.tab_qc.lowerPanel.hbbox.useCountrate = self.options.histScaleCountrate
        if self.tab_calib.lowerPanel.hglist:
            self.tab_calib.lowerPanel.hgbox.useCountrate = self.options.histScaleCountrate
        if self.tab_calib.lowerPanel.hblist:
            self.tab_calib.lowerPanel.hbbox.useCountrate = self.options.histScaleCountrate
        event.Skip()   
        
    def OnSaveMsetCSV(self,event):
        """Save a measuremetn set as .csv"""
        if self.mset == None:
            wx.MessageBox("No measurement set exists.","", wx.OK|wx.CENTRE)
            return
        di.SaveFile(self,self.mset.csv(),['CSV','csv'],['CSV files','CSV files'])
        
    def OnSaveObject(self, event):
        """Save a measurement or a measurement set to a pickle file"""
        if event.GetId()==menu.SAVE_MEAS:
            if self.bgsample == None:
                 wx.MessageBox("No measurement exists. Check data and analysis."
                                      ,"", wx.OK|wx.CENTRE)
                 return
            di.SavePickleFile(self,self.bgsample)
        if event.GetId()==menu.SAVE_DATASET:
            if self.mset == None:
                 wx.MessageBox("No measurement set exists.","", wx.OK|wx.CENTRE)
                 return
            di.SavePickleFile(self,self.mset)
                
    def OnReadObject(self, event):
        """Read a measurement or a measurement set from a pickle file"""
        if event.GetId()==menu.OPEN_MEAS:
           if self.bgsample != None:
               dlg = wx.MessageDialog(self, "Loaded measurement will be deleted. OK?"
                                      ,"", wx.YES_NO|wx.ICON_WARNING|wx.CENTRE)
               result = dlg.ShowModal()
               if result == wx.ID_NO:
                   return
           path, obj = di.ReadPickleFile(self)
           if path == None and obj == None:
               return
           if isinstance(obj, bgs.BGSample):
               self.bgsample = obj
               self.sample = self.bgsample.sample
               self.gasbk = self.bgsample.gasbk
               self.detbk = self.bgsample.detbk
               self.qc = self.bgsample.qc
               print("Loading new measurement")
               self.loadMeasurement()
           else:
               wx.MessageBox("Could not read a sample from selected file."
                                      ,"", wx.OK|wx.CENTRE)
               return
        if event.GetId()==menu.OPEN_DATASET:
           if self.mset != None:
               dlg = wx.MessageDialog(self, "Loaded measurement set will be deleted. OK?"
                                      ,"", wx.YES_NO|wx.ICON_WARNING|wx.CENTRE)
               result = dlg.ShowModal()
               if result == wx.ID_NO:
                   return
           path, obj = di.ReadPickleFile(self)
           if path == None and obj == None:
               return
           if isinstance(obj, xs.xenonSampleSet):
               self.mset = obj
               print("Loading new measurement set")
               self.OnPlotMset(0)
           else:
               wx.MessageBox("Could not read a measurement set from selected file."
                                      ,"", wx.OK|wx.CENTRE)
    
    def OnSavePHD(self,event):
         """Save loaded measurement as PHD-file"""
         if event.GetId()==menu.SAVE_SAMPLE_PHD and self.sample == None:
             wx.MessageBox("No sample exists.","", wx.OK|wx.CENTRE)
             return
         if event.GetId()==menu.SAVE_GASBK_PHD and self.gasbk == None:
             wx.MessageBox("No gas background exists.","", wx.OK|wx.CENTRE)
             return
         if event.GetId()==menu.SAVE_DETBK_PHD and self.detbk == None:
             wx.MessageBox("No detbk exists.","", wx.OK|wx.CENTRE)
             return
         if event.GetId()==menu.SAVE_QC_PHD and self.qc == None:
             wx.MessageBox("No QC exists.","", wx.OK|wx.CENTRE)
             return
         if event.GetId()==menu.SAVE_CALIB_PHD and self.calib == None:
             wx.MessageBox("No calib exists.","", wx.OK|wx.CENTRE)
             return
         if event.GetId()==menu.SAVE_SAMPLE_PHD:
             di.SaveFile(self,self.sample.IMSFormat(),['PHD','phd'],['IMS2.0 files','IMS 2.0 files'])
         elif event.GetId()==menu.SAVE_GASBK_PHD:
             di.SaveFile(self,self.gasbk.IMSFormat(),['PHD','phd'],['IMS2.0 files','IMS 2.0 files'])
         elif event.GetId()==menu.SAVE_DETBK_PHD:
             di.SaveFile(self,self.detbk.IMSFormat(),['PHD','phd'],['IMS2.0 files','IMS 2.0 files'])
         elif event.GetId()==menu.SAVE_QC_PHD:
             di.SaveFile(self,self.qc.IMSFormat(),['PHD','phd'],['IMS2.0 files','IMS 2.0 files'])
         elif event.GetId()==menu.SAVE_CALIB_PHD:
             di.SaveFile(self,self.calib.IMSFormat(),['PHD','phd'],['IMS2.0 files','IMS 2.0 files'])
         else:
             print("Wrong event id when saving PHD file.")
             
    def OnSaveReport(self,event):
        """Save measurement or measurement set report"""
        if event.GetId()==menu.SAVE_MEAS_REPORT:
            if self.bgsample == None:
                 wx.MessageBox("No measurement exists. Check data and analysis."
                                      ,"", wx.OK|wx.CENTRE)
                 return
            di.SaveFile(self,self.bgsample.bgmHandler.report(),['TXT','txt'],['TXT files','TXT files'])
        if event.GetId()==menu.SAVE_MEASSET_REPORT:
            if self.mset == None:
                 wx.MessageBox("No measurement set  exists."
                                      ,"", wx.OK|wx.CENTRE)
                 return
            di.SaveFile(self,self.mset.report,['TXT','txt'],['TXT files','TXT files'])
           
    def OnClearMea(self, event):
        """Delete measurement data and clear all plots"""
        print("Deleting measurement data")
        self.bgsample = None
        self.sample = None
        self.gasbk = None
        self.detbk = None
        self.qc = None
        self.calib = None
        self.tab_sample.clearData()
        self.tab_gasbk.clearData()
        self.tab_detbk.clearData()
        self.tab_qc.clearData()
        self.tab_calib.clearData()
        
        
    def OnUnmarkMset(self,event):
        """Unmark all measurements in the measurement set"""
        if self.mset == None:
             wx.MessageBox("Not measurement set loaded.","", wx.OK|wx.CENTRE)
             return
        for s in self.mset.set:
            s.marked = False
        if self.nb.FindPage(self.tab_plot) != wx.NOT_FOUND:
            self.mset.drawMarkers(self.tab_plot.figure)
        
    def OnClearMset(self, event):
        """Delete the measurement set and clear plots"""
        if self.mset == None:
             wx.MessageBox("Not measurement set loaded.","", wx.OK|wx.CENTRE)
             return
        dlg = wx.MessageDialog(self, "Loaded measurement set will be deleted. OK?"
                                      ,"", wx.YES_NO|wx.ICON_WARNING|wx.CENTRE)
        result = dlg.ShowModal()
        if result == wx.ID_NO:
            return
        print("Deleting measurement set")
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        self.tab_plot = wx.Panel(self.nb)
        self.nb.AddPage(self.tab_plot, "Plot")
        self.mset = None

    def OnCalcMset(self, event):
        """Calculate a measurement set from files"""
        if self.mset != None:
            dlg = wx.MessageDialog(self, "Loaded measurement set will be deleted. OK?"
                                      ,"", wx.YES_NO|wx.ICON_WARNING|wx.CENTRE)
            result = dlg.ShowModal()
            if result == wx.ID_NO:
                return
        txt = ''
        if self.options.writeResultFiles:
            txt += "Sample .pkl files will be written to:\n"
            txt += path.join(self.options.resultPath,'results')
            txt += '\n'
        if self.options.moveDataFiles:
            txt += 'Analyzed data files will be moved to:\n'
            txt += path.join(self.options.resultPath,'data')
        txt += "\n OK?"
        if self.options.moveDataFiles or self.options.writeResultFiles:
            dlg = wx.MessageDialog(self, txt,"", wx.YES_NO|wx.ICON_WARNING|wx.CENTRE)
            result = dlg.ShowModal()
            if result == wx.ID_NO:
                return
        self.mset = xs.xenonSampleSet(self.options.dataPath,
                                                       self.options.detbkPath,
                                                       resultPath = self.options.resultPath,
                                                       prog = True,
                                                       combine = self.options.combine, 
                                                       use_gasbk = self.options.analysisUseGB,
                                                       verbose = self.options.verbose,
                                                       useIngrowth=self.options.ingrowthCorr,
                                                       writeResults = self.options.writeResultFiles,
                                                       moveDataFiles = self.options.moveDataFiles)
        if self.mset.getNSamples() == 0:
            wx.MessageBox(format("Measurement set empty. Check data in %s" %self.options.dataPath),
                          "", wx.OK|wx.CENTRE)
            self.mset = None
            return 
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        self.tab_plot = pp.plotPanel(self.nb,
                                     self.mset.plotACTimeSeries(
                                        self.options.mSetPlot, 
                                        iso = self.options.mSetPlotIso, 
                                        hideMarked = self.options.hideMarked), 
                                        pickPoints = True,
                                        evtReciever = self)
        self.Bind(pp.EVT_POINT_PICKED, self.OnPointClicked)
        self.nb.AddPage(self.tab_plot, "Measurement Set")
        self.nb.ChangeSelection(5)
        
    def OnReportMset(self,evt):
        """Print a measurement set report."""
        if self.mset == None:
             wx.MessageBox("Not measurement set to report.","", wx.OK|wx.CENTRE)
             return
        self.mset.makeReport()
        print(self.mset.report)
        
    def OnPointClicked(self,evt):
         """Perform actions if a datapoint is clicked"""
         if not self.options.useMarkers:
             return
         index = evt.attr1
         figure = evt.attr2
         line_index = evt.attr3
         sp = self.mset.getPlottedSample(index,line_index)
         if sp != None:
             removed = sp.marked
             sp.marked = not sp.marked
             if not removed:
                 print(sp.makeInfo())
             if sp.resultPath != None and self.options.loadMarkedSample and not removed:
                 self.loadFileSample(sp.resultPath)
         self.mset.drawMarkers(figure)
        
    def OnPlotMset(self, event):
        """Plot a timeseries in the plot tab"""
        if self.mset == None:
             wx.MessageBox("Not measurement set to plot.","", wx.OK|wx.CENTRE)
             return
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        self.tab_plot = pp.plotPanel(self.nb,
                                     self.mset.plotACTimeSeries
                                     (self.options.mSetPlot, 
                                      iso = self.options.mSetPlotIso,
                                      hideMarked = self.options.hideMarked),
                                      pickPoints = True,
                                      evtReciever = self)
        self.nb.AddPage(self.tab_plot, "Measurement Set")
        self.nb.ChangeSelection(5)
        self.Bind(pp.EVT_POINT_PICKED, self.OnPointClicked)
    
    def OnFreqMset(self, event):
        """Plot frequency histograms in the plot tab"""
        if self.mset == None:
             wx.MessageBox("Not measurement set to plot.","", wx.OK|wx.CENTRE)
             return
        plotOpt = copy.copy(self.options.mSetPlot)
        if 'E' in plotOpt:
            plotOpt.remove('E')
        if 'L' in plotOpt:
            plotOpt.remove('L')
        if 'G' in plotOpt:
            plotOpt.remove('G')
        if len(plotOpt) > 1:
            wx.MessageBox("Please select only one plot option in the options menu.\n (AC, LC, MDC, A, LCA or MDA)"
                                      ,"", wx.OK|wx.CENTRE)
            return
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        self.tab_plot = pp.plotPanel(self.nb,
                                     self.mset.frequencyDistr
                                     (self.options.mSetPlot, 
                                      self.options.mSetPlotIso))
        self.nb.AddPage(self.tab_plot, "Frequency")
        self.nb.ChangeSelection(5)
    
    def OnAppendMset(self, event):
        """Append a measurement set to the currently loaded set"""
        if self.mset == None:
             wx.MessageBox("Not measurement set to append to."
                                      ,"", wx.OK|wx.CENTRE)
             return
        path, mset = di.ReadPickleFile(self)
        if mset != None:
            print("Appending measurement set")
            self.mset.appendSet(mset)
            self.OnPlotMset(0)
    
    def OnPlotParam(self,event):
        if self.mset == None:
            wx.MessageBox("Not measurement set to plot.","", wx.OK|wx.CENTRE)
            return
        opt = []
        if self.menu.plotXeVol.IsChecked():
            opt.append('xeVol')
        if self.menu.plotXeYield.IsChecked():
            opt.append('xeYield')
        if self.menu.plotAirVol.IsChecked():
            opt.append('airVol')
        if self.menu.plotErrors.IsChecked():
            showErr = True
        else:
            showErr = False
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        self.tab_plot = pp.plotPanel(self.nb,self.mset.plotQuantity(opt, showErr))
        self.nb.AddPage(self.tab_plot, 'Parameters')
        self.nb.ChangeSelection(5)
        
    def OnMircMset(self,event):
        """Plot a MIRC plot in the plot tab"""
        if self.mset == None:
            wx.MessageBox("Not measurement set to plot.","", wx.OK|wx.CENTRE)
            return
        page =  self.nb.FindPage(self.tab_plot)
        self.nb.DeletePage(page)
        if event.GetId()==menu.MSET_MIRC3: opt = 3
        if event.GetId()==menu.MSET_MIRC4: opt = 4
        self.tab_plot = pp.plotPanel(self.nb,self.mset.MIRC(opt), 
                                     pickPoints = True, evtReciever = self)
        self.nb.AddPage(self.tab_plot, "MIRC" + str(opt))
        self.nb.ChangeSelection(5)
        self.Bind(pp.EVT_POINT_PICKED, self.OnPointClicked)
            
    def OnAnalyze(self, event):
        """
        Create a BGSample if enough data loaded. 
        Do a BGM- analysis if no input errors found.
        """
        self.bgsample = None
        bgmOK = False
        tweakParam = [0,1,0,1]
        if self.sample != None and self.detbk != None:
            tweak = False
            if self.options.tweakParameters[0]:
                tweakParam[0] = self.options.tweakParameters[1]
                tweak = True
            if self.options.tweakParameters[2]:
                tweakParam[1] = self.options.tweakParameters[3]
                tweak = True
            if self.options.tweakParameters[4]:
                tweakParam[2] = self.options.tweakParameters[5]
                tweak = True
            if self.options.tweakParameters[6]:
                tweakParam[3] = self.options.tweakParameters[7]
                tweak = True
            self.sample.resetROIs()
            if tweak:
                print("Tweaking sample using [beta offset, beta tweak, gamma offset, gamma tweak] = ", tweakParam)
                self.tweakedLastSample = True
                self.sample.calibrate(tweakParam)
            else:
                if self.tweakedLastSample:
                    print("Recalibrating sample since it was tweaked the last time")
                    self.sample.calibrate()
                    self.tweakedLastSample = False
            if not self.sample.errors and not self.detbk.errors:
                if self.options.analysisUseGB and self.gasbk != None:
                    if not self.gasbk.errors:
                        self.gasbk.resetROIs()
                        if tweak:
                            self.gasbk.calibrate(tweakParam)
                            self.tweakedLastGasbk = True
                        else:
                            if self.tweakedLastGasbk:
                                self.gasbk.calibrate()
                                self.tweakedLastGasbk = False
                        self.bgsample = bgs.BGSample(self.sample, self.detbk, self.gasbk, self.qc)
                        print("Created measurement with gas background.")
                        bgmOK = not ((self.bgsample.sample.status & bg.ZERO_GROSS) or\
                            (self.bgsample.gasbk.status & bg.ZERO_GROSS))
                if not self.options.analysisUseGB:
                    self.bgsample = bgs.BGSample(self.sample, self.detbk, qc = self.qc)
                    print("Created measurement without gas background.")
                    bgmOK = not (self.bgsample.sample.status & bg.ZERO_GROSS)
        if bgmOK:
                self.bgsample.bgmAnalysis(self.options.combine, self.options.verbose, self.options.ingrowthCorr)
                print(self.bgsample.bgmHandler.report())
                self.tab_sample.loadData(self.sample, self.bgsample, useCountrate = self.options.histScaleCountrate)
                self.tab_gasbk.loadData(self.gasbk, useCountrate = self.options.histScaleCountrate)
                self.nb.ChangeSelection(0)
        else:
            wx.MessageBox("Data error. Check data and analysis options."
                                      ,"", wx.OK|wx.CENTRE)         
            
    def OpenPHD(self,event):
        """Open a PHD-file and load data into a measurementPanel"""
        pathname, data = di.ReadFile(self,['PHD','phd'],['IMS2.0 files','IMS2.0 files'])
        if data is None:
            return
        else:
            if event.GetId()==menu.OPEN_SAMPLE:
                if (ut.getDataType(pathname) == 'SAMPLEPHD' and not
                    self.options.ignoreFiletype) or self.options.ignoreFiletype:
                    self.sample = bg.BGMeasurement(self.options.fileStationType, pathname)
                    self.tab_sample.loadData(self.sample, useCountrate = self.options.histScaleCountrate)
                    self.nb.ChangeSelection(0)
                else:
                     wx.MessageBox("File is not SAMPLEPHD. This can be overrun by selecting the \"Ignore PHD filetype\" option."
                                      ,"", wx.OK|wx.CENTRE) 
            if event.GetId()==menu.OPEN_GASBK:
                if (ut.getDataType(pathname) == 'GASBKPHD' and not
                    self.options.ignoreFiletype) or self.options.ignoreFiletype:
                        self.gasbk = bg.BGMeasurement(self.options.fileStationType, pathname)
                        self.tab_gasbk.loadData(self.gasbk, useCountrate = self.options.histScaleCountrate)
                        self.nb.ChangeSelection(1)
                else:
                      wx.MessageBox("File is not GASBKPHD. This can be overrun by selecting the \"Ignore PHD filetype\" option."
                                      ,"", wx.OK|wx.CENTRE) 
            if event.GetId()==menu.OPEN_DETBK:
                if (ut.getDataType(pathname) == 'DETBKPHD' and not
                    self.options.ignoreFiletype) or self.options.ignoreFiletype:
                        self.detbk = bg.BGMeasurement(self.options.fileStationType, pathname)
                        self.tab_detbk.loadData(self.detbk, useCountrate = self.options.histScaleCountrate)
                        self.nb.ChangeSelection(2)
                else:
                    print("Wrong filetype")
            if event.GetId()==menu.OPEN_QC:
                if (ut.getDataType(pathname) == 'QCPHD' and not
                    self.options.ignoreFiletype) or self.options.ignoreFiletype:
                        self.qc = bg.BGMeasurement(self.options.fileStationType, pathname)
                        self.tab_qc.loadData(self.qc, useCountrate = self.options.histScaleCountrate)
                        self.nb.ChangeSelection(3)
                else:
                     wx.MessageBox("File is not QCPHD. This can be overrun by selecting the \"Ignore PHD filetype\" option."
                                      ,"", wx.OK|wx.CENTRE) 
            if event.GetId()==menu.OPEN_CALIB:
                if (ut.getDataType(pathname) == 'CALIBPHD' and not
                    self.options.ignoreFiletype) or self.options.ignoreFiletype:
                        self.calib = bg.BGMeasurement(self.options.fileStationType, pathname)
                        self.tab_calib.loadData(self.calib, useCountrate = self.options.histScaleCountrate)
                        self.nb.ChangeSelection(4)
                else:
                     wx.MessageBox("File is not CALILBPHD. This can be overrun by selecting the \"Ignore PHD filetype\" option."
                                      ,"", wx.OK|wx.CENTRE) 
                    
    def PrintPHD(self,event):
        """Print loaded data on IMS -format"""
        if event.GetId()==menu.PRINT_SAMPLE:
            if self.sample == None:
                wx.MessageBox("No Sample loaded","", wx.OK|wx.CENTRE)
            else:
                print(self.sample.IMSFormat())
        if event.GetId()==menu.PRINT_GASBK:
            if self.gasbk == None:
                wx.MessageBox("No Gasbk loaded","", wx.OK|wx.CENTRE)
            else:
                print(self.gasbk.IMSFormat())
        if event.GetId()==menu.PRINT_DETBK:
            if self.detbk == None:
                wx.MessageBox("No Detbk loaded","", wx.OK|wx.CENTRE)
            else:
                print(self.detbk.IMSFormat())
        if event.GetId()==menu.PRINT_QC:
            if self.qc == None:
                wx.MessageBox("No QC loaded","", wx.OK|wx.CENTRE)
            else:
                print(self.qc.IMSFormat())
        if event.GetId()==menu.PRINT_CALIB:
            if self.calib == None:
                wx.MessageBox("No Calib loaded","", wx.OK|wx.CENTRE)
            else:
                print(self.calib.IMSFormat())     
                    
    def loadMeasurement(self):
        """Load measurement data into the various tabs"""
        if self.bgsample != None:
            self.tab_sample.loadData(self.bgsample.sample, self.bgsample, useCountrate = self.options.histScaleCountrate)
            self.tab_gasbk.loadData(self.bgsample.gasbk, useCountrate = self.options.histScaleCountrate)
            self.tab_detbk.loadData(self.bgsample.detbk, useCountrate = self.options.histScaleCountrate)
            self.tab_qc.loadData(self.bgsample.qc, useCountrate = self.options.histScaleCountrate)
            self.nb.ChangeSelection(0)
    
    def loadFileSample(self,filePath):
       wait =  wx.BusyCursor()
       try:
           with open(filePath, 'rb') as file:
               print("Reading file %s" % filePath)
               obj = pickle.load(file)
       except IOError:
            print("Cannot open file %s\n" %filePath)
            obj = None
            del wait
            return
       self.bgsample = obj
       self.sample = self.bgsample.sample
       self.gasbk = self.bgsample.gasbk
       self.detbk = self.bgsample.detbk
       self.qc = self.bgsample.qc
       self.loadMeasurement()
       self.nb.ChangeSelection(0)
       del wait
                    
    def clearMeasurementPanels(self):
        """Clear all measurement tabs"""
        self.tab_sample.clearData()
        self.tab_gasbk.clearData()
        self.tab_detbk.clearData()
        self.tab_qc.clearData()
        self.tab_calib.clearData()


app = wx.App(False)
mainFrame(None,"openSpex " + VERSION + " BGM " + bgm.VERSION).Show()
app.MainLoop()
del app