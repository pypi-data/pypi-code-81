#!/usr/bin/env python
# -*- coding:utf-8
from .libs import tkinter as tkinker
_tkinker=tkinker.Tkinter()

def Button(_div,text,color1=None,color2=None,command=None,width=None,height=None,place=1):
    _tkinker.TkinterButton(_div,text,color1,color2,command,width,height,place)

def Label( _div,text, color=None, width=None, height=None,place=1):
    _tkinker.TkinterLabel( _div,text, color, width, height,place)

def Div():
    return _tkinker.TkinterDiv()

def ShowDiv(div):
    _tkinker.TkinterShowDiv(div)