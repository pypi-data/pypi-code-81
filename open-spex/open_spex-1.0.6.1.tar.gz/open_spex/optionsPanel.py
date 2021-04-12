#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:29:46 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import wx
import wx.lib.newevent
from pathlib import Path
from os import path
import os

SaveEvent, EVT_OPTIONS_SAVED = wx.lib.newevent.NewEvent()

class options():
    """Options for the GUI 'openSpex'"""
    def __init__(self):
        self.ignoreFiletype = False
        self.histScaleCountrate = True
        self.verbose = False
        self.useMarkers = True
        self.loadMarkedSample = True
        self.hideMarked = False
        self.fileStationType = 'SAUNA'
        self.analysisUseGB = False
        self.combine = True
        self.originalBGM = False
        self.ingrowthCorr = True
        self.tweakParameters = [False,0,False,1,False,0,False,1]
        self.mSetPlot = ['AC', 'E', 'G']
        self.mSetPlotIso = ['Xe-133', 'Xe-131m', 'Xe-133m','Xe-135']
        self.writeResultFiles = True
        self.moveDataFiles = False
        self.spexFHome = path.join(Path.home(),".openSpex")
        if not path.exists(self.spexFHome):
            os.mkdir(self.spexFHome)
        self.pathFile = path.join(self.spexFHome,"DataPaths")
        try:
            with open(self.pathFile, 'r') as file:
                lines = file.read().splitlines()
                self.dataPath = lines[0]
                self.detbkPath = lines[1]
                self.resultPath = lines[2]
        except IOError:
            self.dataPath = str(os.getcwd())
            self.detbkPath = str(os.getcwd())
            self.resultPath = str(os.getcwd())
            
class optionsPanel(wx.Frame):
    """Options window for the GUI 'openSpex' """
    def __init__(self, parent, title, options):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(600,600), pos = (100,50))
        self.parent = parent
        self.options = options
        vbox = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer()
        self.nb = wx.Notebook(self)
        #General options
        self.tab_general = wx.Panel(self.nb)
        self.cb_ignoreType = wx.CheckBox(self.tab_general,
                        label = "Ignore PHD datatype", pos = (10,20))
        self.cb_verbose = wx.CheckBox(self.tab_general, label = "Verbose", pos = (10,40))
        self.cb_useMarkers = wx.CheckBox(self.tab_general, label = "Use markers", pos = (10,60))
        self.cb_loadMarkedSample = wx.CheckBox(self.tab_general, label = "Load marked sample", pos = (10,80))
        self.cb_hideMarkedSample = wx.CheckBox(self.tab_general, label = "Hide marked samples", pos = (10,100))
        
        lb = ["Counts/bin", "Counts/bin/s"]
        self.rb_hist = wx.RadioBox(self.tab_general, label= "1D Histogram scale", 
                                   pos = (10,130), 
                                   choices= lb, majorDimension = 1, 
                                   style = wx.RA_SPECIFY_ROWS)
        wx.StaticText(self.tab_general, label="Data path:        ", pos = (10,200))
        self.dpathPicker = wx.DirPickerCtrl(self.tab_general, wx.DIRP_DIR_MUST_EXIST, 
                            path = str(Path.home()), pos=(100,200), size=(300,28))
        self.cb_moveData = wx.CheckBox(self.tab_general, label = "Move", pos = (420,200))
        wx.StaticText(self.tab_general, label="Detbk path:        ", pos = (10,240))
        self.dbkpathPicker = wx.DirPickerCtrl(self.tab_general, wx.DIRP_DIR_MUST_EXIST, 
                            path = str(Path.home()), pos=(100,240), size=(300,28))
        wx.StaticText(self.tab_general, label="Result path:        ", pos = (10,280))
        self.resultpathPicker = wx.DirPickerCtrl(self.tab_general, wx.DIRP_DIR_MUST_EXIST, 
                            path = str(Path.home()), pos=(100,280), size=(300,28))
        self.cb_writeResults = wx.CheckBox(self.tab_general, label = "Save", pos = (420,280))
        
        #analysis options
        self.tab_analysis = wx.Panel(self.nb)
        self.cb_useGB = wx.CheckBox(self.tab_analysis, label = "Use gas background", pos = (10,20))
        lb3 = ["Use ROI 7-10", "Original"]
        self.rb_nrois = wx.RadioBox(self.tab_analysis, label= "Method:", 
                                    pos = (10,70), 
                                    choices= lb3, majorDimension = 1, 
                                    style = wx.RA_SPECIFY_ROWS)
        self.cb_ingrCorr = wx.CheckBox(self.tab_analysis, label = "Correct for Xe-133m ingrowth", pos = (10,140))
        self.cb_offsetBeta = wx.CheckBox(self.tab_analysis,label = "Beta offset (chan)", pos = (10,190))
        self.sc_offsetBeta = wx.SpinCtrlDouble(self.tab_analysis, pos = (10,210), min = 0., max = 256, inc = 1.)
        self.cb_tweakBeta = wx.CheckBox(self.tab_analysis,label = "Beta tweak", pos = (10,240))
        self.sc_tweakBeta = wx.SpinCtrlDouble(self.tab_analysis, pos = (10,260), min = 0., max = 2., inc = 0.01)
        self.cb_offsetGamma = wx.CheckBox(self.tab_analysis,label = "Gamma offset (chan)", pos = (10,290))
        self.sc_offsetGamma = wx.SpinCtrlDouble(self.tab_analysis, pos = (10,310), min = 0., max = 256, inc = 1.)
        self.cb_tweakGamma = wx.CheckBox(self.tab_analysis,label = "Gamma tweak", pos = (10,340))
        self.sc_tweakGamma = wx.SpinCtrlDouble(self.tab_analysis, pos = (10,360), min = 0., max = 2., inc = 0.01)
        
        
        #Measurementset plot options
        self.tab_mset = wx.Panel(self.nb)
        self.cb_AC = wx.CheckBox(self.tab_mset,
                        label = "Activity Concentration (AC)", pos = (10,20))
        self.cb_LC = wx.CheckBox(self.tab_mset,
                        label = "Activity Concentration Critical Limit (LC)", pos = (10,40))
        self.cb_MDC = wx.CheckBox(self.tab_mset,
                        label = "MDC", pos = (10,60))
        self.cb_A = wx.CheckBox(self.tab_mset,
                        label = "Activity (A)", pos = (10,80))
        self.cb_LCA = wx.CheckBox(self.tab_mset,
                        label = "Activity Critical Limit (LCA)", pos = (10,100))
        self.cb_MDA = wx.CheckBox(self.tab_mset,
                        label = "MDA", pos = (10,120))
        self.cb_err = wx.CheckBox(self.tab_mset,
                        label = "Error bars", pos = (10,150))
        self.cb_line = wx.CheckBox(self.tab_mset,
                        label = "AC and A as line", pos = (10,170))
        self.cb_dots = wx.CheckBox(self.tab_mset,
                        label = "LC, MDC, LCA, and MDA as dots", pos = (10,190))
        self.cb_legend = wx.CheckBox(self.tab_mset,
                        label = "show legend", pos = (10,210))
        self.cb_xe133 = wx.CheckBox(self.tab_mset,
                        label = "Xe-133", pos = (10,240))
        self.cb_xe131m = wx.CheckBox(self.tab_mset,
                        label = "Xe-131m", pos = (10,260))
        self.cb_xe133m = wx.CheckBox(self.tab_mset,
                        label = "Xe-133m", pos = (10,280))
        self.cb_xe135 = wx.CheckBox(self.tab_mset,
                        label = "Xe-135", pos = (10,300))
        self.cb_rn222 = wx.CheckBox(self.tab_mset,
                        label = "Rn-222", pos = (10,320))
        
    
        self.nb.AddPage(self.tab_general, "General")
        self.nb.AddPage(self.tab_analysis, "BGM Analysis")
        self.nb.AddPage(self.tab_mset, "Measurementset plot")
        box1.Add(self.nb,1, wx.EXPAND)
        vbox.Add(box1, 6, flag = wx.EXPAND )
        vbox.Add((-1,10))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.b_save = wx.Button(self,label="Save", size = (70,30))
        self.b_save.Bind(wx.EVT_BUTTON, self.OnSave)
        hbox2.Add(self.b_save)
        self.b_close = wx.Button(self,label="Close", size= (70,30))
        self.b_close.Bind(wx.EVT_BUTTON, self.OnClose)
        hbox2.Add(self.b_close, flag = wx.LEFT |wx.BOTTOM, border = 5)
        vbox.Add(hbox2, 1, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, border = 10)
        self.SetSizer(vbox)
        self.setOptions()
        self.change = False
    
    def setOptions(self):
        """Set stored options in panel"""
        self.cb_ignoreType.SetValue(self.options.ignoreFiletype)
        self.cb_verbose.SetValue(self.options.verbose)
        self.cb_useGB.SetValue(self.options.analysisUseGB)
        self.cb_ingrCorr.SetValue(self.options.ingrowthCorr)
        self.dpathPicker.SetPath(self.options.dataPath)
        self.dbkpathPicker.SetPath(self.options.detbkPath)
        self.resultpathPicker.SetPath(self.options.resultPath)
        self.cb_writeResults.SetValue(self.options.writeResultFiles)
        self.cb_moveData.SetValue(self.options.moveDataFiles)
        
        self.cb_offsetBeta.SetValue(self.options.tweakParameters[0])
        self.sc_offsetBeta.SetValue(self.options.tweakParameters[1])
        self.cb_tweakBeta.SetValue(self.options.tweakParameters[2])
        self.sc_tweakBeta.SetValue(self.options.tweakParameters[3])
        self.cb_offsetGamma.SetValue(self.options.tweakParameters[4])
        self.sc_offsetGamma.SetValue(self.options.tweakParameters[5])
        self.cb_tweakGamma.SetValue(self.options.tweakParameters[6])
        self.sc_tweakGamma.SetValue(self.options.tweakParameters[7])
        
        self.cb_useMarkers.SetValue(self.options.useMarkers)
        self.cb_loadMarkedSample.SetValue(self.options.loadMarkedSample)
        self.cb_hideMarkedSample.SetValue(self.options.hideMarked)

        
        if self.options.histScaleCountrate:
            self.rb_hist.SetSelection(1)
        else:
            self.rb_hist.SetSelection(0)
            
        if self.options.combine and not self.options.originalBGM:
            self.rb_nrois.SetSelection(0)
        if self.options.originalBGM and not self.options.combine:
            self.rb_nrois.SetSelection(1)
        if 'AC' in self.options.mSetPlot:
            self.cb_AC.SetValue(True)
        else:
            self.cb_AC.SetValue(False)
        if 'LC' in self.options.mSetPlot:
            self.cb_LC.SetValue(True)
        else:
            self.cb_LC.SetValue(False)
        if 'MDC' in self.options.mSetPlot:
            self.cb_MDC.SetValue(True)
        else:
            self.cb_MDC.SetValue(False)
        if 'A' in self.options.mSetPlot:
            self.cb_A.SetValue(True)
        else:
            self.cb_A.SetValue(False)
        if 'LCA' in self.options.mSetPlot:
            self.cb_LCA.SetValue(True)
        else:
            self.cb_LCA.SetValue(False)
        if 'MDA' in self.options.mSetPlot:
            self.cb_MDA.SetValue(True)
        else:
            self.cb_MDA.SetValue(False)
        if 'E' in self.options.mSetPlot:
            self.cb_err.SetValue(True)
        else:
            self.cb_err.SetValue(False)
        if 'L' in self.options.mSetPlot:
            self.cb_line.SetValue(True)
        else:
            self.cb_line.SetValue(False)
        if 'P' in self.options.mSetPlot:
            self.cb_dots.SetValue(True)
        else:
            self.cb_dots.SetValue(False)
        if 'G' in self.options.mSetPlot:
            self.cb_legend.SetValue(True)
        else:
            self.cb_legend.SetValue(False)
            
        if 'Xe-133' in self.options.mSetPlotIso:
            self.cb_xe133.SetValue(True)
        else:
            self.cb_xe133.SetValue(False)
        if 'Xe-131m' in self.options.mSetPlotIso:
            self.cb_xe131m.SetValue(True)
        else:
            self.cb_xe131m.SetValue(False)
        if 'Xe-133m' in self.options.mSetPlotIso:
            self.cb_xe133m.SetValue(True)
        else:
            self.cb_xe133m.SetValue(False)
        if 'Xe-135' in self.options.mSetPlotIso:
            self.cb_xe135.SetValue(True)
        else:
            self.cb_xe135.SetValue(False) 
        if 'Rn-222' in self.options.mSetPlotIso:
            self.cb_rn222.SetValue(True)
        else:
            self.cb_rn222.SetValue(False)      
        self.Layout()
        
    def OnSave(self,event):
        """Store selected options"""
        self.change = False
        self.options.ignoreFiletype = self.cb_ignoreType.GetValue()
        self.options.verbose = self.cb_verbose.GetValue()
        self.options.analysisUseGB = self.cb_useGB.GetValue()
        self.options.ingrowthCorr =  self.cb_ingrCorr.GetValue()
        self.options.useMarkers = self.cb_useMarkers.GetValue()
        self.options.loadMarkedSample = self.cb_loadMarkedSample.GetValue()
        self.options.hideMarked = self.cb_hideMarkedSample.GetValue()
        self.options.dataPath = self.dpathPicker.GetPath()
        self.options.detbkPath = self.dbkpathPicker.GetPath()
        self.options.resultPath = self.resultpathPicker.GetPath()
        self.options.writeResultFiles = self.cb_writeResults.GetValue()
        self.options.moveDataFiles = self.cb_moveData.GetValue()

        if self.rb_hist.GetSelection() ==0:
            self.options.histScaleCountrate = False
        else:
            self.options.histScaleCountrate = True
            
        if self.rb_nrois.GetSelection() ==0:
            self.options.combine = True
            self.options.originalBGM = False
        else:
            self.options.combine = False
            self.options.originalBGM = True
               
        self.options.tweakParameters[0] = self.cb_offsetBeta.GetValue()
        self.options.tweakParameters[1] = self.sc_offsetBeta.GetValue()
        self.options.tweakParameters[2] = self.cb_tweakBeta.GetValue()
        self.options.tweakParameters[3] = self.sc_tweakBeta.GetValue()
        self.options.tweakParameters[4] = self.cb_offsetGamma.GetValue()
        self.options.tweakParameters[5] = self.sc_offsetGamma.GetValue()
        self.options.tweakParameters[6] = self.cb_tweakGamma.GetValue()
        self.options.tweakParameters[7] = self.sc_tweakGamma.GetValue()
            
        self.options.mSetPlot = []
        ac = False
        a = False
        if self.cb_AC.GetValue():
            self.options.mSetPlot.append('AC')
            ac = True
        if self.cb_LC.GetValue():
            self.options.mSetPlot.append('LC')
            ac = True
        if self.cb_MDC.GetValue():
            self.options.mSetPlot.append('MDC')
            ac = True
        if self.cb_A.GetValue():
            self.options.mSetPlot.append('A')
            a = True
        if self.cb_LCA.GetValue():
            self.options.mSetPlot.append('LCA')
            a = True
        if self.cb_MDA.GetValue():
            self.options.mSetPlot.append('MDA')
            a = True
        if self.cb_err.GetValue():
            self.options.mSetPlot.append('E')
        if self.cb_line.GetValue():
            self.options.mSetPlot.append('L')
        if self.cb_dots.GetValue():
            self.options.mSetPlot.append('P')
        if self.cb_legend.GetValue():
            self.options.mSetPlot.append('G')
            
        if a and ac: 
            wx.MessageBox("You are plotting A and AC at the same time. Please change."
                                      ,"", wx.OK|wx.CENTRE)
            self.change = True
        self.options.mSetPlotIso = []
        if self.cb_xe133.GetValue():
            self.options.mSetPlotIso.append('Xe-133')
        if self.cb_xe131m.GetValue():
            self.options.mSetPlotIso.append('Xe-131m')
        if self.cb_xe133m.GetValue():
            self.options.mSetPlotIso.append('Xe-133m')
        if self.cb_xe135.GetValue():
            self.options.mSetPlotIso.append('Xe-135')
        if self.cb_rn222.GetValue():
            self.options.mSetPlotIso.append('Rn-222')

        try:
            with open(self.options.pathFile, 'w') as file:
                txt = [self.options.dataPath, self.options.detbkPath, self.options.resultPath]
                for line in txt:
                    file.write(line)
                    file.write("\n")
                file.close()
        except IOError:
            wx.LogError("Cannot write to pathFile %s. Data paths set to home directory.\n" %self.options.pathFile)
            self.dataPath = str(Path.home())
            self.detbkPath = str(Path.home())
            self.resultPath = str(Path.home())
        myEvent = SaveEvent()
        wx.PostEvent(self.parent, myEvent)
        event.Skip()
        
    def OnClose(self,event):
        """Perform some checks and then close the options panel"""
        if self.change:
              wx.MessageBox("You are plotting A and AC at the same time. Please change."
                                      ,"", wx.OK|wx.CENTRE)
              return
        if not path.exists(self.options.dataPath):
            wx.MessageBox("Data path does not exist. Please modify"
                                      ,"", wx.OK|wx.CENTRE)
            return
        if not path.exists(self.options.detbkPath):
            wx.MessageBox("Detector background path does not exist. Please modify"
                                      ,"", wx.OK|wx.CENTRE)
        if not path.exists(self.options.resultPath):
            wx.MessageBox("Result path does not exist. Please modify"
                                      ,"", wx.OK|wx.CENTRE)
            return
        self.Close()
        
"""
app = wx.App(False)
opt = options()
optionsPanel(None,"Options",opt).Show()
app.MainLoop()
del app
"""