#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import os
import oss2
from bs4 import BeautifulSoup
import urllib

def write(filename,text,typename='w',encoding='utf8'):
    dirname = os.path.dirname(filename)
    print(dirname)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename,typename,encoding=encoding) as f:
        f.write(text)

def read(filename,typename='r',encoding='utf8'):
    with open(filename,typename,encoding=encoding) as f:
        return f.read()
    return ''

def getHtml(url,retry_count = 5):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    while retry_count > 0:
        try:
            res = requests.get(url, headers=headers,timeout=10)
            if res.apparent_encoding.lower()=='gb2312':
                return res.text.encode("latin1").decode("gbk")
            else:
                res.encoding = res.apparent_encoding
                return res.text
        except Exception as e:
            print(e)
            retry_count -= 1
    return None

def existsWebFile(srcUrl):
    result = False
    with requests.get(srcUrl, stream=True) as r:
        result = r.ok
    return result

def ossAuthBucket(key,secret,endpoint,bucket):
    auth = oss2.Auth(key, secret)
    bucket = oss2.Bucket(auth, endpoint, bucket)
    return bucket

def ossUploadFile(bucket,localFile,targetFile):
    auth = oss2.Auth(key, secret)
    bucket = oss2.Bucket(auth, endpoint, bucket)    
    return bucket.put_object_from_file(targetFile, localFile)

def getLinks(url,html,allows='*'):
    links = []
    soup = BeautifulSoup(html,"html.parser")
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or href.startswith('javascript:'):
            continue
        new_full_url = urllib.parse.unquote(urllib.parse.urljoin(url, href))
        text = link.text.strip()
        classname = link.get('class')
        item = {'link':new_full_url,'text':text,'class':classname}
        if allows=='*':
            if item not in links:
                links.append(item)
        else:
            for allow in allows:
                if new_full_url and type(allow).__name__=='str' and new_full_url.startswith(allow) and item not in links:
                    links.append(item)
    return links

def handleURL(uri):
    result = urllib.parse.urlparse(uri)
    url = result.scheme + '://' + result.netloc + result.path
    return url