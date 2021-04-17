#!/usr/bin/env python
# -*- coding:utf-8
import time
import pyautogui

class Autogui():


    def AutoguiGetMousePositon(self,t=0):
        time.sleep( t )
        x,y = pyautogui.position()
        return x,y


    def AutoguiWindowSize(self):
        width, height = pyautogui.size() # 屏幕的宽度和高度
        return width,height


    def AutoguiMoveTo(self,x,y,duration=0):
        pyautogui.moveTo( x, y, duration )


    def AutoguiMoveRel(self,left_right=0, up_down=0, duration=0):
        pyautogui.moveRel( left_right, up_down, duration )


    def AutoguiClick(self,x=0,y=0,click_number=1,interval=0.0,button='left'):
        pyautogui.click(x, y, click_number,interval, button)


    def AutoguiScroll(self,number,x=None,y=None):
        pyautogui.scroll(number, x, y)


    def AutoguiSayString(self,char,interval=0.0):
        pyautogui.typewrite( char,interval )


    def AutoguiHotKey(self,one,two):
        pyautogui.hotkey( one, two )