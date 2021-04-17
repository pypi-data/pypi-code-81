#!/usr/bin/env python
# -*- coding:utf-8
import os, sys, shutil
import re
import cv2
import time
import pyscreenshot as ImageGrab
import pyautogui
from .. import config


def sleep(t=0):
    time.sleep(t)


def FindCnStr(find_str, all_str):

    if re.search( find_str, all_str, flags=re.I | re.M ) == None:
        return 0
    else:
        return 1


def FindStr(find_str, all_str, f=0):

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


'''in_dir代表图片原始目录，out_dir代表压缩后的存放目录'''
def ImgCompress(in_dir, out_dir,width,high,num=1):
    dir = config._image_path
    in_dir_path = dir + in_dir
    out_dir_path = dir + out_dir

    for i in range(0,num):
        image=cv2.imread(in_dir_path+ str(i) + ".jpg")

        res = cv2.resize(image, (width,high), interpolation=cv2.INTER_AREA)

        cv2.imwrite(out_dir_path+ str(i) + ".jpg",res)


def FindFiles(dir):
    flist=[]
    for root,dirs,files in os.walk(config._files_path+dir):
        for file in files:
            flist.append(os.path.basename(os.path.join(root,file)))
    if flist==[]:
        return 0
    else:
        return flist


def OpenFiles(files_name):
    os.startfile(config._files_path+files_name)


def CopyFiles(src,dst):
    try:
        if shutil.copy(config._files_path+src,config._files_path+dst):
            return 1
    except:
        return 0


def BatchCopyFiles(src,dst,t=0):
    res=FindFiles( src )
    if res!=[]:
        for files_name in res:
            CopyFiles( src+"/"+files_name, dst )
            sleep( t )
        return 1
    else:
        return 0


def MoveFiles(src,dst):
    try:
        if shutil.move(config._files_path+src,config._files_path+dst):
            return 1
    except:
        return 0


def BatchMoveFiles(src,dst,t=0):
    res=FindFiles( src )
    if res!=[]:
        for files_name in res:
            MoveFiles( src+"/"+files_name, dst )
            sleep( t )
        return 1
    else:
        return 0


def stop(t=0):
    time.sleep(t)
    sys.exit( 0 )


def CommonImageCapture(x=None, y=None, x1=None, y1=None,image="ImageCapture.bmp" ,mod=1,t1=0,t2=0):
    time.sleep( t1 )
    if mod==1:
        img = ImageGrab.grab( bbox=(x, y, x1, y1) )
        img.save( config._image_path + image )
        return 1

    elif mod==2:
        print( "鼠标放在左上角" )
        x,y=pyautogui.position()
        time.sleep( t2 )
        print( "鼠标放在右下角" )
        time.sleep( t2 )
        x1,y1 = pyautogui.position()
        img = ImageGrab.grab( bbox=(x, y, x1, y1) )
        img.save( config._image_path + image )
        return 1


def CommonWordsCapture(x=None, y=None, x1=None, y1=None,image="WordsCapture.bmp",mod=1,t1=0,t2=0):
    time.sleep( t1 )
    if mod==1:
        img = ImageGrab.grab( bbox=(x, y, x1, y1) )
        img.save( config._words_path + image)
        return 1

    elif mod==2:
        print( "鼠标放在左上角" )
        x,y=pyautogui.position()
        time.sleep( t2 )
        print( "鼠标放在右下角" )
        time.sleep( t2 )
        x1,y1 = pyautogui.position()
        img = ImageGrab.grab( bbox=(x, y, x1, y1) )
        img.save( config._words_path + image )
        return 1