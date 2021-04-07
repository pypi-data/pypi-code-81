# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       setup
   Description :
   Author:          jiangfb
   date:            2021-03-12
-------------------------------------------------
   Change Activity:
                    2021-03-12:
-------------------------------------------------
"""
__author__ = 'jiangfb'

from setuptools import setup, find_packages     # 这个包没有可以pip一下

setup(
    name = "JFB",      # 这个是pip项目发布的名称
    version = "21.4.7.2",      # 版本号，pip默认安装最新版
    keywords = ("pip", "utils", "JFB"),
    description = "一些utils方法",
    long_description = "",
    license = "MIT Licence",
    url = "https://github.com/jiangfubang/jfb",       # 项目相关文件地址，一般是github，有没有都行吧
    author = "JiangFubang",
    author_email = "luckybang@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []        # 该模块需要的第三方库
)