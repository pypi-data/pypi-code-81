# -*- coding: utf-8 -*-

"""
do.py 实际工具集合Py模块
do 做什么 做它 do it.
@Date    : 2021-4-9 17:03:03
@Author  : LC
"""
import platform
import psutil
import requests

# 使用 utoolc.do 统一使用入口 当然其他入口也开放 自由发挥
# 将所有的工具函数和功能Python模块(Module)(模块能定义函数，类和变量，模块里也能包含可执行的代码)暴露出去
# 在do.py模块暴露出去之后 可以 utoolc.do 进行访问操作
# 写法一 推荐 使用绝对路径 更直观 手动导入 更可控 目前使用这个方案吧
from utoolc import get_random
from utoolc.easy import easy_say
from utoolc.utils import utils, print_msg_to_log_model, start_to_end_time_consuming


# # 写法二
# from . import get_random
# from .easy import easy_say
# from .utils import utils, print_msg_to_log_model, start_to_end_time_consuming
# # 写法三 这个写法 其他Py文件有新增功能代码,这里就能暴露出去 这里*的意思是导入所有 方法一和二还得do.py代码里 对应添加 但这个也是有利有弊 比如没有方法一 直观可控
# from utoolc import *  # 故 utils.print_a_line() 直接使用没有问题
# from utoolc.easy import *
# from utoolc.utils import *

# do => 格式的互转
# 将 input formats 输入格式 转换为 output formats 输出格式 - A格式与B格式的互转
# @param from_formats: {str} 输入的格式 【'rst''markdown'等】
# @param to_formats: {str} 输出的格式 【'rst''markdown'等】
# @param from_file: {str} 输入格式的文件的路径
# @param to_file: {str} 输出格式文件的路径
# -----------------------------------------------------------------------
# Docverter’s REST API 官网如下:
# Docverter - Use Docverter’s REST API to convert your documents, lickety split.
# https://www.docverter.com/
# Docverter | learn
# https://www.docverter.com/learn/
# 支持的输入输出格式如下-具体看上面官网链接:
# What formats does Docverter support?
# Docverter supports the following input formats:
#
# Markdown
# Textile
# reStructured Text
# HTML
# Docbook
# LaTeX
#
# And can convert to these output formats:
#
# PDF
# HTML
# Microsoft Docx
# OpenOffice ODT
# OpenDocument XML
# EPUB (for iBooks)
# MOBI (for Kindle)
# DocBook
# TexInfo
# Groff
# LaTeX/ConTeXt
# Markdown
# reStructured Text
# AsciiDoc
# MediaWiki
# Emacs Org-Mode
# Textile
# -----------------------------------------------------------------------
def do_cverter(from_formats, to_formats, from_file, to_file):
    utils.print_a_line()
    print('...do...do_cverter...from', from_file, from_formats, '格式...to...', to_file, to_formats, '格式')
    utils.print_a_line()
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'from': from_formats, 'to': to_formats},
        files={'input_files[]': open(from_file, 'rb')}
    )

    if response.ok:
        print('...do...do_cverter...success...')
        with open(to_file, "wb") as f:
            f.write(response.content)


# do => Py运行时工具类
# 获取当前操作系统名称
# mac -> Darwin
# win -> Windows
# linux -> Linux
def get_os():
    return platform.system()


# 获取当前系统的CPU核数量
# 使用 psutil 第三方模块
def get_num_cpu():
    return psutil.cpu_count()


# 是否是mac系统
def is_mac_os():
    return get_os() == 'Darwin'


# 是否是win系统
def is_win_os():
    return get_os() == 'Windows'


# 是否是linux系统
def is_linux_os():
    return get_os() == 'Linux'
