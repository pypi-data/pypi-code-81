#!/usr/bin/env python
# -*- coding:utf-8
import time
import pyautogui

class Autogui():

    #----获取鼠标位置
    def AutoguiGetMousePositon(self,t=0):
        time.sleep( t )
        x,y = pyautogui.position()
        return x,y

    #----屏幕的宽和高
    def AutoguiWindowSize(self):
        width, height = pyautogui.size() # 屏幕的宽度和高度
        return width,height

    #----鼠标移动
    def AutoguiMoveTo(self,x,y,duration=0):
        pyautogui.moveTo( x, y, duration )

    #----鼠标位移
    def AutoguiMoveRel(self,left_right=0, up_down=0, duration=0):
        pyautogui.moveRel( left_right, up_down, duration )

    #----鼠标移动点击
    def AutoguiClick(self,x=0,y=0,click_number=1,interval=0.0,button='left'):
        pyautogui.click(x, y, click_number,interval, button)

    #----鼠标滚动
    def AutoguiScroll(self,number,x=None,y=None):
        pyautogui.scroll(number, x, y)

    #----输入字符串和数字
    def AutoguiSayString(self,char,interval=0.0):
        pyautogui.typewrite( char,interval )

    # ----热键组合
    def AutoguiHotKey(self,one,two):
        pyautogui.hotkey( one, two )