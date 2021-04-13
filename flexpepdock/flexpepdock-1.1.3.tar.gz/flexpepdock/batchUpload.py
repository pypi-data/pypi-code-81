#!/usr/bin/env python3
import os
import sys
import requests
from optparse import OptionParser
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

file = ""

def post(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Referer":"http://flexpepdock.furmanlab.cs.huji.ac.il/index.php",
        "Host": "flexpepdock.furmanlab.cs.huji.ac.il",
        "Origin":"http://flexpepdock.furmanlab.cs.huji.ac.il",
        "Upgrade-Insecure-Requests":"1",
        "Proxy-Connection":"keep-alive",
    }
    # , verify = certifi.where()
    # result = requests.get(url, headers=headers, data={}, verify=certifi.where(),timeout=30)
    result = requests.post(url,  headers={"Content-Type":file.content_type},data=file)
    return result

# 从单个的开始做,然后再批量
def atom_task(pdb_url, eMail):
    global file
    file = MultipartEncoder(
        fields={
            # 'field0': 'value',
            # 'field1': 'value',
            'eMail':eMail,
            'upload': ('file', open(pdb_url, "rb"), 'application/file'),
            # 'filed3': ("aab.jpg", open("aab.jpg", 'rb'), "image/jpeg")
        })
    res = post('http://flexpepdock.furmanlab.cs.huji.ac.il/saveFile.php').text
    # 这里要把结果号爬出来

    if res.__contains__("You did not succeed in uploading the PDB file"):
        print("failed, may be the format of your pdb file is wrong")
    else:
        soup = BeautifulSoup(res, "lxml")
        for x in soup.find_all("td"):
            if x.get('id') is not None:
                if x.get('id') == 'content':
                    result_url = x.find_all('a')[1].get('href')
                    # print(x.find_all('a')[1].get('href'))
        print("success, the result url is " + result_url)


# 判断地址是pdb文件 还是 directory 地址即可
def task(args):
    mode = 0
    # 1为单个 2为多个  3为批量
    count = 0

    eMail = ""
    # 处理输入的所有参数
    for x in args:
        if str(x).endswith('.pdb'):
            mode = 1
            count += 1
        if str(x).__contains__('@') and (str(x).__contains__('com') or str(x).__contains__('cn')):
            eMail = str(x)

    if count > 1 :
        mode = 2
    if mode == 0:
        if str(args[0]).__contains__("/"):
             mode = 3  #如果方法都没有匹配，那么就是文件夹批量上传
    # 如果模式还是0 那么就是出问题了
    if mode == 0:
        print("The params were wronged, please check again!")
        return
    print("Welcome to use flexpepdock patchUpload @Author -nonobel")
    print("Task start...")
    if not eMail == "":
        print("Your result will be delivered to "+eMail)
    if mode == 1:
        atom_task(args[0],eMail)
    elif mode == 2:
        for x in args:
            if str(x).endswith('.pdb'):
                atom_task(x,eMail)
    elif mode == 3:
        dir_url = args[0]
        files = os.listdir(dir_url)
        for x in files:
            if x.endswith(".pdb"):
                atom_task(dir_url+x,eMail)


    #     读取文件目录，找出所有pdb
    print("Task completed !")


def usage(type):
    if type == "showOption":
        print(''' \033[92m	
               Welcome to use flexpepdock patchUpload @Author -nonobel
               	Usage : 
                    (1)single upload ：batchUpload + 1.pdb
                    (2)Multiple upload ：batchUpload + 1.pdb  2.pdb  3.pdb (seperate the file by space)
                    (2)batch upload ：batchUpload + the dir that pdb files exist in   (this will upload all pdb files in directory)
                Result: print the url that stores the analysis data.
                Ps: You can use absolute dir or relative dir 
               	\033[0m''')

        result = ""

    elif type == "help":
        print(''' \033[92m	
         Welcome to use flexpepdock patchUpload @Author -nonobel
        	    No more introduction.
        	\033[0m''')
    sys.exit()


def get_parameters():
    optp = OptionParser(add_help_option=False, epilog="Hammers")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
    optp.add_option("-o", "--option", dest="option", action='store_true', help="your option")
    deal_parameters(optp)


def deal_parameters(optp):
    global option
    # 变量和那个都保存在这optp里面
    opts, args = optp.parse_args()
    if opts.help:
        usage("help")
    # elif opts.option is not None:
    #     usage("showOption")
    #     option = opts.option
    elif len(args) == 0:
        usage("showOption")
    else:
        task(args)

def main():
    get_parameters()

# 如何处理相对路径和绝对路径，就是在执行的目录呢，是不是默认支持
if __name__ == '__main__':
    main()
