#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui
_autogui=autogui.Autogui()

def HotKey(one,two):
    _autogui.AutoguiHotKey( one, two )