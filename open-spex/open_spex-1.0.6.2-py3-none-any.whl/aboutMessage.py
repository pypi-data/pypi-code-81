#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 09:03:19 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import wx
import wx.lib.agw.hyperlink as hl

class about( wx.Dialog):

    def __init__(self, parent, info, linkText= '', url = None):
            vbox = wx.BoxSizer(wx.VERTICAL)
            #wx.Dialog.__init__(self, parent, -1, wx.STR_REFRESH_BALANCE, style=style)
            wx.Dialog.__init__(self, parent, -1)
            self.info = wx.StaticText(self, label=info)
            if url != None:
                self.url = hl.HyperLinkCtrl(self, -1, linkText, URL= url)
            else:
                self.url = wx.StaticText(self, label='')
            buttons = self.CreateButtonSizer(wx.OK)
    
            vbox.AddMany([
                (self.info, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10),
                (self.url, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10),
                (buttons, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
            ])
            self.SetSizerAndFit(vbox)