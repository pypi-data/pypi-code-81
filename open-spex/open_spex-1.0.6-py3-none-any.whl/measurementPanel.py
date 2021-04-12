#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:03:01 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
import os

from open_spex import plotPanel as pp
from open_spex import bgm as bgm

font = 'Liberation Mono'
if os.name == 'nt':
    font = 'Courier New'

class measurementPanel(wx.Panel):
    """A window showing spectra and some data from a BGMeasurement"""
    def __init__(self, parent, options, mea=None, sample=None, extra = None):
        wx.Panel.__init__(self, parent)
        self.mea = mea
        self.sample = sample
        if options != None:
            self.useCountrate = options.histScaleCountrate
        else:
            self.options = None
        self.extra = extra
        self.drawSpectra()
      
    def drawSpectra(self):
        """Show loaded spectra in the measurement panel"""
        #Splitter and panels
        self.splitter = wx.SplitterWindow(self)
        #Upper panel
        self.figure1 = Figure()
        self.ax_text = self.figure1.add_subplot(121)
        self.ax_bg = self.figure1.add_subplot(122)
        self.ax_text.axis('off')
        if self.mea is not None and self.sample is None:
            self.mea.beta_gamma_hist.draw(self.figure1, self.ax_bg, self.mea.ROI_limits_chan)
            txt = self.mea.info
        if self.mea is not None and self.sample is not None:
            if hasattr(self.sample.bgmHandler,"roiBitPattern"):
                if not self.sample.bgmHandler.combined:
                    bp = bgm.kROI_3 + bgm.kROI_4
                else:
                    bp = self.sample.bgmHandler.roiBitPattern
                self.mea.beta_gamma_hist.draw(self.figure1, self.ax_bg, self.mea.ROI_limits_chan, bp)
            else:
                self.mea.beta_gamma_hist.draw(self.figure1, self.ax_bg, self.mea.ROI_limits_chan)
            txt = self.mea.info + "\n" + self.sample.analysisInfo
        if self.mea is not None:
            font_dict = {'family': font, 'color':'black', 'size':9}
            self.ax_text.text(0., 1.1, txt, va='top', fontdict = font_dict)
        self.upperPanel = pp.plotPanel(self.splitter, self.figure1)
        #Lower panel
        self.figure2 = Figure()
        self.ax_g = self.figure2.add_subplot(121)
        self.ax_b = self.figure2.add_subplot(122)
        if self.sample != None:
            hglist = self.sample.sample.get1DHistList('gamma')
            hblist = self.sample.sample.get1DHistList('beta')
            if self.sample.gasbk != None:
                hglist += self.sample.gasbk.get1DHistList('gamma')
                hblist += self.sample.gasbk.get1DHistList('beta') 
            if self.sample.detbk != None:
                hglist += self.sample.detbk.get1DHistList('gamma')
                hblist += self.sample.detbk.get1DHistList('beta') 
        elif self.mea != None and self.sample  == None:
            hglist = self.mea.get1DHistList('gamma')
            hblist = self.mea.get1DHistList('beta')
        else:
            hglist = None
            hblist = None
        self.lowerPanel = pp.plotPanel(self.splitter, self.figure2, 
                                       hglist = hglist, hblist = hblist,
                          useCountrate = self.useCountrate, useLegend=True)
        if self.lowerPanel.hgbox != None:
            self.lowerPanel.hgbox.SetCheckedItems([1])
            self.lowerPanel.hgbox.OnSelected(0)
        if self.lowerPanel.hbbox != None:
            self.lowerPanel.hbbox.SetCheckedItems([1])
            self.lowerPanel.hbbox.OnSelected(0)
        #Split screen --
        self.splitter.SplitHorizontally(self.upperPanel, self.lowerPanel)
        #self.splitter.SetMinimumPaneSize(100)
        split_sizer = wx.BoxSizer()
        split_sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(split_sizer)
        self.splitter.SetSashPosition(400)
        
    def loadData(self, mea, sample=None, useCountrate = None):
            """Load data into the measurement panel"""
            if mea is not None:
                if mea.errors:
                    print("Error in measurement. Could not load data into measurementPanel.")
                    return
            self.mea = mea
            self.sample = sample
            self.useCountrate = useCountrate
            self.splitter.Destroy()
            self.drawSpectra()
            self.Layout()
            
    def clearData(self):
        """Clear the measurement panel"""
        if self.mea != None:
            self.mea = None
        if self.sample != None:
                self.sample = None
        self.splitter.Destroy()
        self.drawSpectra()
        self.Layout()
