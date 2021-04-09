#!/usr/bin/env python
# -*- coding:utf-8
from .libs import extend,ai,common
_extend=extend.Extend()
_ai=ai.Ai()
_common=common

def Ocr(image,e="low"):
    return _ai.Ocr(image,e)

def OcrFindWords(image, cn, f=0, e="high"):
    return _extend.OcrFindWords(image,cn,f,e)

def OcrCaptureFindWords(x1,y1,x2,y2,fileName,words,f=0,e="high",t=0):
    return _extend.OcrCaptureFindWords(x1,y1,x2,y2,fileName,words,f,e,t)

def FindStr(find_str,all_str,f=0):
    return _common.FindStr(find_str,all_str,f)

def FindCnStr(find_str,all_str):
    return _common.FindCnStr(find_str,all_str)
