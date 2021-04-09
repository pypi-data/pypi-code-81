#!/usr/bin/env python
# -*- coding:utf-8
import re
from . import common,ai

class Extend():
    def __init__(self):
        self._common=common
        self._ai=ai

    # ----Ocr查字（支持中文、英文、数字）
    def OcrFindWords(self, image, cn, f=0, e="high"):
        '''
        python2.7版本中，被查找的字符前必须加u ，例如：Orc_FindCnStr("1.bmp",u'摘要',f=0),f=1代表不区分大小写,
        返回1代表查找成功，返回0代表查找失败，e="low"代表普通版，e="high"代表高精版
        '''
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

    # ----Ocr抓图识别查字（支持中文、英文、数字）
    def OcrCaptureFindWords(self,x1,y1,x2,y2,fileName,words,f=0,e="high",t=0):
        '''
        参数
        x1,x1：左上角坐标
        x2,y2：右下角坐标
        fileName：抓图保存图片名
        words：要查找的字
        f：对大小写是否敏感 ，1 不敏感，0 敏感
        e：识别的精度，low 普通精度，high 高精度
        t：开始抓图延时

        返回值
        1：找到字
        0：未找到字
        '''

        self._common.CommonWordsCapture( x1, y1, x2, y2, fileName,t)
        return self.OcrFindWords(fileName, words,f,e )

    #----遍历并打开指定目录下的所有文件
    def FindOpenFiles(self,files_dir):
        files_name = common.FindFiles( files_dir )
        for i in files_name:
            common.OpenFiles( files_dir + "/" + i )
