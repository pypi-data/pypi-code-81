#!/usr/bin/env python
# -*- coding:utf-8
from .libs import autogui,common,ai,opencv
_opencv=opencv.Opencv()
_autogui=autogui.Autogui()
_ai=ai.Ai()
_common=common

def ImgCompress(in_dir, out_dir,width,high,num=1):
    _common.ImgCompress(in_dir,out_dir,width,high,num)

def Synthesis(image):
    return _ai.ImageSynthesis(image)

def FindPicture(target,template):
    return _opencv.OpencvFindPicture(target,template)

def ImageCapture(x=None, y=None, x1=None, y1=None,image="ImageCapture.bmp" ,mod=1,t1=1,t2=1):
    return _common.CommonImageCapture(x, y, x1, y1,image ,mod,t1,t2)

def WordsCapture(x=None, y=None, x1=None, y1=None,image="WordsCapture.bmp" ,mod=1,t1=0,t2=0):
    return _common.CommonWordsCapture(x, y, x1, y1,image ,mod,t1,t2)