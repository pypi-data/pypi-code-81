#!/usr/bin/ python
#coding:utf-8

"""
软件名称:星门数据库(stargateDB)
描述：星门数据库是一款微型电脑数据库
官方首页：http://www.stargatedb.com/
文档教程：http://www.stargatedb.com/index.php/wendangjiaocheng.html
申请账号：http://www.stargatedb.com/index.php/page/user.html
作者：重庆羊排信息技术有限公司
发布日期：2021年4月1日
"""

import requests
import os

#---中英文字符存储
def Add(username,password,key,value,database,life_time=0):
    request_url = "http://api.stargatedb.com:8002/add?username="+username+"&password="+password+"&key=" + str(key)+"&value="+str(value)+"&database="+str(database)+"&life_time="+str(life_time)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url,headers=headers)
    result_str = response.text
    return eval(result_str)

def Delete(username,password,key,database):
    request_url = "http://api.stargatedb.com:8002/delete?username="+username+"&password="+password+"&key=" + str( key ) + "&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

def Change(username,password,key,value,database,life_time=-1):
    request_url = "http://api.stargatedb.com:8002/change?username="+username+"&password="+password+"&key=" + str(key)+"&value="+str(value)+"&database="+str(database)+"&life_time="+str(life_time)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    try:
        result=eval(result_str)
        return result
    except:
        return result_str

def Find(username,password,key,database):
    request_url = "http://api.stargatedb.com:8002/find?username="+username+"&password="+password+"&key="+ str(key) +"&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    try:
        result=eval(result_str)
        return result
    except:
        return result_str

def AllFind(username,password,database):
    request_url = "http://api.stargatedb.com:8002/allfind?username="+username+"&password="+password+"&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

#---图片存储
"""
图片类型
• jpg  –  image/jpeg 
• png  –  image/png 
• gif  –  image/gif 
• webp  –  image/webp 
• cr2  –  image/x-canon-cr2 
• tif  –  image/tiff 
• bmp  –  image/bmp 
• jxr  –  image/vnd.ms-photo 
• psd  –  image/vnd.adobe.photoshop 
• ico  –  image/x-icon
"""
def AddImage(username,password,image,database,dir_path):
    img_src= dir_path+image
    try:
        files = {'file': (image, open( img_src, 'rb' ), {'Expires': '0'})}
    except:
        return {"state":404,"message":"no find image"}
    request_url = "http://api.stargatedb.com:8002/addimage?username="+username+"&password="+password+"&database=" + str(database)
    response = requests.post( request_url,files = files)
    result_str = response.text
    return eval(result_str)

def DeleteImage(username,password,image,database):
    request_url = "http://api.stargatedb.com:8002/deleteimage?username="+username+"&password="+password+"&image=" + str( image ) + "&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

def FindImage(username,password,image,database,save_dir):
    request_url = "http://api.stargatedb.com:8002/findimage?username="+username+"&password="+password+"&database=" + str( database ) + "&image=" + str( image )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    if not os.path.exists( save_dir ):
        os.mkdir( save_dir )
    img_path=save_dir+"/"+image
    try:
        result_str=eval( result_str )
        if result_str['state'] == 415:
            return {"state": 415, "message": "Unsupported image type"}
        if result_str['state']==404:
            return result_str
    except:
        with open(img_path,'wb') as f:
            f.write(response.content)
        return {"state":200,"message":"find image success"}

#----音频存储
"""
音频类型
• mid  –  audio/midi 
• mp3  –  audio/mpeg 
• m4a  –  audio/m4a 
• ogg  –  audio/ogg 
• flac  –  audio/x-flac 
• wav  –  audio/x-wav
• amr  –  audio/amr
"""
def AddAudio(username,password,audio,database,dir_path):
    audio_src= dir_path+audio
    try:
        files = {'file': (audio, open( audio_src, 'rb' ), {'Expires': '0'})}
    except:
        return {"state":404,"message":"no find audio"}
    request_url = "http://api.stargatedb.com:8002/addaudio?username="+username+"&password="+password+"&database=" + str(database)
    response = requests.post( request_url,files = files)
    result_str = response.text
    return eval(result_str)

def DeleteAudio(username,password,audio,database):
    request_url = "http://api.stargatedb.com:8002/deleteaudio?username="+username+"&password="+password+"&audio=" + str( audio ) + "&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

def FindAudio(username,password,audio,database,save_dir):
    request_url = "http://api.stargatedb.com:8002/findaudio?username="+username+"&password="+password+"&database=" + str( database ) + "&audio=" + str( audio )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    if not os.path.exists( save_dir ):
        os.mkdir( save_dir )
    audio_path=save_dir+"/"+audio
    try:
        result_str=eval( result_str )
        if result_str['state'] == 415:
            return {"state": 415, "message": "Unsupported audio type"}
        if result_str['state']==404:
            return result_str
    except:
        with open(audio_path,'wb') as f:
            f.write(response.content)
        return {"state":200,"message":"find audio success"}

#----视频存储
"""
视频类型
• mp4  –  video/mp4 
• m4v  –  video/x-m4v 
• mkv  –  video/x-matroska 
• webm  –  video/webm 
• mov  –  video/quicktime 
• avi  –  video/x-msvideo 
• wmv  –  video/x-ms-wmv 
• mpg  –  video/mpeg 
• flv  –  video/x-flv
"""
def AddVideo(username,password,video,database,dir_path):
    video_src= dir_path+video
    try:
        files = {'file': (video, open( video_src, 'rb' ), {'Expires': '0'})}
    except:
        return {"state":404,"message":"no find video"}
    request_url = "http://api.stargatedb.com:8002/addvideo?username="+username+"&password="+password+"&database=" + str(database)
    response = requests.post( request_url,files = files)
    result_str = response.text
    return eval(result_str)

def DeleteVideo(username,password,video,database):
    request_url = "http://api.stargatedb.com:8002/deletevideo?username="+username+"&password="+password+"video=" + str( video ) + "&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

def FindVideo(username,password,video,database,save_dir):
    request_url = "http://api.stargatedb.com:8002/findvideo?username="+username+"&password="+password+"&database=" + str( database ) + "&video=" + str( video )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    if not os.path.exists( save_dir ):
        os.mkdir( save_dir )
    video_path=save_dir+"/"+video
    try:
        result_str=eval( result_str )
        if result_str['state'] == 415:
            return {"state": 415, "message": "Unsupported video type"}
        if result_str['state']==404:
            return result_str
    except:
        with open(video_path,'wb') as f:
            f.write(response.content)
        return {"state":200,"message":"find video success"}

#----附件存储
"""
附件类型
• epub  –  application/epub+zip
• zip  –  application/zip
• tar  –  application/x-tar
• rar  –  application/x-rar-compressed
• gz  –  application/gzip 
• bz2  –  application/x-bzip2 
• 7z  –  application/x-7z-compressed 
• xz  –  application/x-xz 
• pdf  –  application/pdf 
• exe  –  application/x-msdownload 
• swf  –  application/x-shockwave-flash 
• rtf  –  application/rtf 
• eot  –  application/octet-stream 
• ps  –  application/postscript 
• sqlite  –  application/x-sqlite3 
• nes  –  application/x-nintendo-nes-rom 
• crx  –  application/x-google-chrome-extension 
• cab  –  application/vnd.ms-cab-compressed 
• deb  –  application/x-deb 
• ar  –  application/x-unix-archive 
• Z  –  application/x-compress 
• lz  –  application/x-lzip
"""
def AddResour(username,password,resour,database,dir_path):
    resour_src= dir_path+resour
    try:
        files = {'file': (resour, open( resour_src, 'rb' ), {'Expires': '0'})}
    except:
        return {"state":404,"message":"no find resour"}
    request_url = "http://api.stargatedb.com:8002/addresour?username="+username+"&password="+password+"&database=" + str(database)
    response = requests.post( request_url,files = files)
    result_str = response.text
    return eval(result_str)

def DeleteResour(username,password,resour,database):
    request_url = "http://api.stargatedb.com:8002/deleteresour?username="+username+"&password="+password+"&resour=" + str( resour ) + "&database=" + str(database)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    return eval(result_str)

def FindResour(username,password,resour,database,save_dir):
    request_url = "http://api.stargatedb.com:8002/findresour?username="+username+"&password="+password+"&database=" + str( database ) + "&resour=" + str( resour )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url, headers=headers )
    result_str = response.text
    if not os.path.exists( save_dir ):
        os.mkdir( save_dir )
    video_path=save_dir+"/"+resour
    try:
        result_str=eval( result_str )
        if result_str['state'] == 415:
            return {"state": 415, "message": "Unsupported resour type"}
        if result_str['state']==404:
            return result_str
    except:
        with open(video_path,'wb') as f:
            f.write(response.content)
        return {"state":200,"message":"find resour success"}

#-----示列代码-----
# res=AddAudio("xxxxx","xxxxx","1.mp3","new","./new/")
# print(res)

# res=FindAudio("xxxxx","xxxxx","1.mp3","new","./test/")
# print(res)

# res=DeleteAudio("xxxxx","xxxxx","1.mp3","new")
# print(res)

# res=Add("wumeng","xxxxx","xxxxx","无梦","new",30)
# print(res)

# res=Change("xxxxx","xxxxx","new",10)
# print(res)

# res=Delete("xxxxx","xxxxx")
# print(res)

# res=AllFind("xxxxx","xxxxx","new")
# for i in res:
#     print(res[i]['value'])
