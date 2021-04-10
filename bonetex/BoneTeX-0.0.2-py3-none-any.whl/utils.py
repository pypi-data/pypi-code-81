#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/19 17:13
# @Author : 詹荣瑞
# @File : utils.py
# @desc : 本代码未经授权禁止商用
from chevron import render


def bone_template_render(code_string: str, words_dict: dict):
    for key, value in words_dict.items():
        code_string = code_string.replace("{{"+key+"}}", str(value))
    return code_string


def mustache_render(code_string: str, words_dict: dict):
    return render(code_string, words_dict)
