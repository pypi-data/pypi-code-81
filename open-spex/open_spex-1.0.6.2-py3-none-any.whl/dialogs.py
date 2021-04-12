#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 08:02:41 2020

@author: ringbom
This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import wx
import pickle
from os import path

def exportIMSFile(bgmeas,pathname):
    fn = path.join(pathname, bgmeas.phdFileName)
    try:
        with open(fn, 'w') as file:
            file.write(bgmeas.IMSFormat())      
    except IOError:
        wx.LogError("Cannot save current data in file '%s'." % fn)
    print("Exported data to file %s" %fn)
        
def ReadFile(parent,ext=[],descr=[]):
    """
    Dialogue for opening and reading a file.
    Parameters:
    ----------
    ext:      List of extension strings [ext1,ext2,...]
    descr     List of corresponding description strings [descr1,descr2, ...]
    
    Returns pathname, data
    Returns 'None', 'None' if cancelled.
    Returns pathname, 'None' if file could not be opened. 
    """
    wildc = ""
    i = 0
    for ex in ext:
        if i > 0:
            wildc += "|"
        wildc +=descr[i] + " (*." + ex +")|*." + ex
        i +=1
    
    with wx.FileDialog(parent, "Open file", 
                       wildcard = wildc,
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return None, None          
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'r') as file:
                print("Reading file %s" % pathname)
                data = file.read()
        except IOError:
            wx.LogError("Cannot open file %s\n" %pathname)
            data = None
    return pathname, data

def SaveFile(parent,buf,ext=[],descr=[]):
    """ 
    Dialog saving content in string 'buf' as file
    Parameters:
    ----------
    buf       Data string
    ext:      List of extension strings [ext1,ext2,...]
    descr     List of corresponding description strings [descr1,descr2, ...]
    """
    wildc = ""
    i = 0
    for ex in ext:
        if i > 0:
            wildc += "|"
        wildc +=descr[i] + " (*." + ex +")|*." + ex
        i +=1
    with wx.FileDialog(parent, "Save file", wildcard=wildc,
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'w') as file:
              file.write(buf)      
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)
            
    
def SavePickleFile(parent, obj):
    """
    Dialogue for saving an object to a pickle file.
    Returns 'True' if file was saved; 'False' otherwize.
    """
    with wx.FileDialog(parent, "Save pkl-file", 
                       wildcard="pkl files (*.pkl)|*.pkl",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return False
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'wb') as file:
               pickle.dump(obj, file)
        except IOError:
            wx.LogError("Cannot save current data in file %s\n" %pathname)
            return False
        return True
            

def ReadPickleFile(parent):
    """
    Dialogue for opening and reading an object from a pickle file. 
    Returns pathname, object. 
    Returns 'None', 'None' if cancelled.
    Returns pathname, 'None' if file could not be opened. 
    """
    with wx.FileDialog(parent, "Open pkl file", 
                       wildcard="pkl files (*.pkl)|*.pkl",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return None, None   
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'rb') as file:
                print("Reading file %s" % pathname)
                obj = pickle.load(file)
        except IOError:
            wx.LogError("Cannot open file %s\n" %pathname)
            obj = None
    return pathname, obj