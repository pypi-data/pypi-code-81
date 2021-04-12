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
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
import wx.lib.newevent

from open_spex import histPlotBox as hp

PickPointEvent, EVT_POINT_PICKED = wx.lib.newevent.NewEvent()

class plotPanel(wx.Panel):
    """
    A panel with a figure. 
    It also shows the coordinates for the mouse.
    """
    def __init__(self, parent, figure,  
                 hglist = None, hblist = None, pickPoints = False, 
                 evtReciever = False, useCountrate = False, useLegend=False):
        wx.Panel.__init__(self, parent)
        if figure == None:
            print("Warning: no figure to display.")
            return
        self.evtReciever = evtReciever
        self.figure = figure
        self.axes = self.figure.axes
        self.useCountrate = useCountrate
        self.useLegend = useLegend
        self.hglist = hglist
        self.hblist = hblist
        for ax in self.axes:
            ax.format_coord = lambda x,y: ""  #This is to disable the coordinates to be shown in the toolbar
            if not pickPoints: 
                ax.set_picker(True)
            else:
                for line in ax.lines:
                    line.set_picker(5)
        self.nLines = len(self.axes[0].lines) #all plots must have the same nrb of lines
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.Text = wx.StaticText( self, wx.ID_ANY, u"  Available Channels  ",
                                  wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Text.Wrap( -1 )
        self.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        if self.hglist != None:
            self.hgbox = hp.histPlotBox(self,self.canvas, self.axes[0], hglist, 
                                        self.useCountrate, self.useLegend)
            sizer2.Add(self.hgbox, 1, wx.LEFT)
        else:
            self.hgbox = None
        if self.hblist != None:
            self.hbbox = hp.histPlotBox(self,self.canvas, self.axes[1], hblist, 
                                        self.useCountrate, self.useLegend)
            sizer2.Add(self.hbbox, 1, wx.LEFT, border = 20)
        else:
            self.hbbox = None
        self.sizer.Add(sizer2, 1)
        self.canvas.SetMinSize((5,5))    #Solved problem that panels doesn't resize properly on Windows 10. 
        self.sizer.Add(self.canvas, 8, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
        self.add_toolbar()
        self.sizer.Add(self.Text,0, wx.LEFT | wx.EXPAND)
        if pickPoints:
            self.pickPointId = self.canvas.mpl_connect('pick_event', self.OnPickPoint)

    def OnPickPoint(self,event):
         N = len(event.ind)
         if not N: 
             return True
         line = event.artist
         line_ind = line.get_gid()
         if line_ind < 99:
             return True
         evt = PickPointEvent(attr1=event.ind[0], attr2 = self.figure, attr3 =line_ind)
         wx.PostEvent(self.evtReciever, evt)
         
    def add_toolbar(self):
        """ Add a toolbar """
        self.toolbar = NavigationToolbar2WxAgg(self.canvas)
        self.toolbar.Realize()
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
        
    def onMotion(self, evt):
        """Getthe x,y coordinates of the mouse pointer"""
        self.xdata = evt.xdata
        self.ydata = evt.ydata
        try:
            x = round(self.xdata,4)
            y = round(self.ydata,4)
        except:
            x = ""
            y = ""
        self.Text.SetLabelText("%s, %s" % (x,y))