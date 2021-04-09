#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui,common
_autogui=autogui.Autogui()
_common=common

def GetMousePositon(t=0):
    return _autogui.AutoguiGetMousePositon(t)

def MoveTo(x,y,duration=0):
    _autogui.AutoguiMoveTo(x,y,duration)

def MoveRel(left_right=0, up_down=0, duration=0):
    _autogui.AutoguiMoveRel(left_right, up_down, duration)

def Click(x=0,y=0,click_number=1,interval=0.0,button='left'):
    _autogui.AutoguiClick(x,y,click_number,interval,button)

def Scroll(number,x=None,y=None):
    _autogui.AutoguiScroll(number,x,y)