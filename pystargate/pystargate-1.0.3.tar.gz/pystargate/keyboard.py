#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui
_autogui=autogui.Autogui()

#----热键组合
def HotKey(one,two):
    _autogui.AutoguiHotKey( one, two )