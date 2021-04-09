#!/usr/bin/env python3

import os
import sys
import get
# import time, argparse
from optparse import OptionParser
# from typing import Dict

switch = {
    '1': "xhs",
    '2': "weibo",
    '3': "tiktokLive",
}


# 这里应该是获取到一个地址
# 判断地址是pdb文件 还是 directory 地址即可
def task(args):
    mode = 0
    # 1为单个 2为多个  3为批量
    count = 0
    for x in args:
        if str(x).endswith('.pdb'):
            mode = 1
            count += 1
    if count > 1 :
        mode = 2
    if mode == 0:
        if str(args[0]).__contains__("/"):
             mode = 3  #如果方法都没有匹配，那么就是文件夹批量上传
    # 如果模式还是0 那么就是出问题了
    if mode == 0:
        print("输入的参数有误，请检查")
        return
    print("欢迎使用flexpepdock批量下载工具 @Author -nonobel")
    print("任务开始...")
    if mode == 1:
        get.atom_task(args[0])
    elif mode == 2:
        for x in args:
            get.atom_task(x)
    elif mode == 3:
        dir_url = args[0]
        files = os.listdir(dir_url)
        for x in files:
            if x.endswith(".pdb"):
                get.atom_task(dir_url+x)


    #     读取文件目录，找出所有pdb
    print("任务完毕")


def usage(type):
    if type == "showOption":
        print(''' \033[92m	
               欢迎使用flexpepdock批量下载工具 @Author -nonobel 
               	usage : 
                    (1)单个上传 ：batchUpload + 1.pdb
                    (2)多个上传 ：batchUpload + 1.pdb  2.pdb  3.pdb (空格分开即可）
                    (2)批量上传 ：batchUpload + pdb文件所在的目录地址  (会将目录底下的pdb全部上传分析)
                result: 输出的是 网站获取结果的链接，请自行复制保存查看
                支持相对路径表达方式
               	\033[0m''')

        result = ""
        # while not result.isdigit():
        #     result = input()
        # task(str(switch.get(result)))

    elif type == "help":
        print(''' \033[92m	
        欢迎使用flexpepdock批量下载工具 @Author -nobel 
        	usage : 
        	    没有help咯，help就如开头所示
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


# 如何处理相对路径和绝对路径，就是在执行的目录呢，是不是默认支持
if __name__ == '__main__':
    get_parameters()