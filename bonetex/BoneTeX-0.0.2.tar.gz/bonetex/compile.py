#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/12/3 18:29
# @Author : 詹荣瑞
# @File : compile.py
# @desc : 本代码未经授权禁止商用
import os
import re
from typing import Tuple, Union


class Compiler(object):

    def __init__(self, doc, path, compilers: Union[Tuple, str] = "xelatex"):
        re_path_name = re.compile(r"(.+)[\\/](.+)")
        self.doc = doc
        self.path, self.name = re_path_name.search(path).groups()
        if isinstance(compilers, str):
            self.compilers = (compilers,)
        else:
            self.compilers = compilers

    def generate_tex(self):
        path, name = self.path, self.name
        latex_code = self.doc.latex()
        with open(f"{os.path.join(path, name)}.tex", "w", encoding="utf-8") as file:
            file.write(latex_code)
        return latex_code

    def generate_pdf(self, generate_tex=True):
        if generate_tex:
            self.generate_tex()
        original_cwd = os.getcwd()
        path, name = self.path, self.name
        os.chdir(os.path.join(os.getcwd(), path))
        for compiler in self.compilers:
            os.system(f"{compiler} ./{name}.tex")
        os.chdir(original_cwd)


def latex_compile(doc, path, compiler="xelatex"):
    original_cwd = os.getcwd()
    re_path_name = re.compile(r"(.+)[\\/](.+)")
    path, name = re_path_name.search(path).groups()
    os.chdir(os.path.join(os.getcwd(), path))
    latex_code = doc.latex()
    with open(f"./{name}.tex", "w", encoding="utf-8") as file:
        file.write(latex_code)
    os.system(f"{compiler} ./{name}.tex")
    os.chdir(original_cwd)
    return latex_code
