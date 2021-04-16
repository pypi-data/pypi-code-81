#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : setup
# @Author   : LiuYan
# @Time     : 2021/4/16 10:07

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='xiaoxiong',
    version='0.0.1',
    author='ygg',
    author_email='ygg@zut.edu.cn',
    description='Oh Bear !',
    long_description=long_description,
    url='https://gitee.com/ly_love_ly/xiaoxiong',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
