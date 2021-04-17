#!/usr/bin/env python
# -*- coding:utf-8
import re
from . import common,ai

class Extend():
    def __init__(self):
        self._common=common
        self._ai=ai
    def OcrFindWords(self, image, cn, f=0, e="high"):
        all_str = self._ai.Ai().Ocr( image, e ).encode( 'unicode-escape' ).decode( 'unicode_escape' )
        find_str = cn.encode( 'unicode-escape' ).decode( 'unicode_escape' )
        if f == 1:
            if re.search( find_str, all_str, flags=re.I | re.M ) == None:
                return 0
            else:
                return 1

        else:
            if re.search( find_str, all_str ) == None:
                return 0
            else:
                return 1


    def OcrCaptureFindWords(self,x1,y1,x2,y2,filename,words,f=0,e="high",mod=1,t1=1,t2=1):
        self._common.CommonWordsCapture( x1, y1, x2, y2, filename,mod,t1,t2)
        return self.OcrFindWords(filename, words,f,e )


    def FindOpenFiles(self,files_dir):
        files_name = common.FindFiles( files_dir )
        for i in files_name:
            common.OpenFiles( files_dir + "/" + i )
