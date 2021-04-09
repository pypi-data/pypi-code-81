# -*- coding: utf-8 -*-

"""
do.py 实际工具集合Py模块
do 做什么 做它 do it.
@Date    : 2021-4-9 17:03:03
@Author  : LC
"""

import requests
from utoolc.utils import utils


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
