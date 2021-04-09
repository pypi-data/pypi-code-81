#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui,tkinter
_autogui=autogui.Autogui()
_tkinter=tkinter.Tkinter()

def WindowSize():
    return _autogui.AutoguiWindowSize()