#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui
_autogui=autogui.Autogui()

#----输入字符串和数字
def SayString(char,interval=0.0):
    _autogui.AutoguiSayString(char,interval)