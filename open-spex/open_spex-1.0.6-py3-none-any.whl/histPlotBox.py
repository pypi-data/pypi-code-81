#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:46:57 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import wx
import os


font = 'Liberation Mono'
if os.name == 'nt':
    font = 'Courier New'

class histPlotBox(wx.CheckListBox):
    """A listbox connected to an axis where selected histograms will 
    be plotted.
    """
    def __init__(self, parent, canvas, ax, histograms, useCountrate = False, useLegend = False):
        wx.CheckListBox.__init__(self, parent, style = wx.LB_MULTIPLE, size = [300,80])
        self.hist = histograms
        self.canvas = canvas
        self.ax = ax
        self.useCountrate = useCountrate
        self.useLegend = useLegend
        for h in self.hist:
            self.Append(h.title)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnSelected)
        self.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0,font))
    
    def OnSelected(self,evt):
       n = self.GetCount()
       self.ax.cla()
       for i in range(n):
           if self.IsChecked(i):
                   self.hist[i].draw(self.ax, useCountrate = self.useCountrate, 
                                     legend=self.hist[i].title, showLegend = self.useLegend)
       self.ax.set_title("")
       #self.ax.legend()
       self.canvas.draw()
       