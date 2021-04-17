#!/usr/bin/env python
# -*- coding:utf-8
import sys
import os
import requests
import json
from .. import config

IS_PY3 = sys.version_info.major
if IS_PY3 == 3:
    from urllib.parse import quote_plus
elif IS_PY3 == 2:
    from urllib import quote_plus


class Ai():
    def __init__(self):
        # 钥匙账号
        self._username = "test"
        # 钥匙密码
        self._password = "123456"

        # 主目录
        self._words_path = config._words_path
        self._speech_path = config._speech_path
        self._image_path = config._image_path


    def Ocr(self,image,e="low"):
        e=quote_plus(e)
        img_src= self._words_path+image
        files = {'file': (image, open( img_src, 'rb' ), 'image/bmp', {'Expires': '0'})}
        request_url = "http://api.pystargate.com:8000/ocr?e="+e+"&username=" + self._username + "&password="+self._password
        response = requests.post( request_url,files = files)
        result_str = response.text
        return result_str


    def SpeechSynthesis(self,say,save_file="SpeechSynthesis.mp3"):
        _say = say
        _save_file = save_file
        data = quote_plus( _say )
        request_url = "http://api.pystargate.com:8000/speech?say=" + str( data )+"&username=" + self._username + "&password="+self._password
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.get( request_url, headers=headers )
        result_str = response.content

        with open( self._speech_path + _save_file, 'wb+' ) as of:
            of.write( result_str )
            of.close()

        file = self._speech_path + _save_file
        os.system( file )
        return result_str


    def ImageSynthesis(self,image):
        img_src= self._image_path+image
        try:
            files = {'file': (image, open( img_src, 'rb' ), 'image/bmp', {'Expires': '0'})}
        except:
            return "未发现文件"
        request_url = "http://api.pystargate.com:8000/image?"+"username=" + self._username + "&password="+self._password
        response = requests.post( request_url,files = files)
        result_str = response.text
        keyword_arr=[]
        for i in range(0,len(json.loads( result_str )['result'])):
            keyword = json.loads( result_str )['result'][i]['keyword']
            keyword_arr.append(keyword)
            i = i + 1
        return keyword_arr
