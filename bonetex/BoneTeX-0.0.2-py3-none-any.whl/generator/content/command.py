#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/30 22:10
# @Author : 詹荣瑞
# @File : command.py
# @desc : 本代码未经授权禁止商用
from .content import ContentBase


class CommandLine(ContentBase):

    def __init__(self, command, op_para=(), re_para=(), end=" "):
        self.command = command
        self.para = (op_para, re_para)
        self.end = end

    def latex(self, indent=""):
        op_para, re_para = self.para
        re_para = "".join(map(lambda p: f"{{{p}}}", re_para))
        op_para = ', '.join(op_para)
        if op_para != "":
            op_para = f"[{op_para}]"
        out = f"{indent}\\{self.command}{re_para}{op_para}{self.end}"
        return out

    def latex3(self, indent=""):
        return self.latex(indent)


class Command(object):

    def __init__(self, name, end=" "):
        self.name = name
        self.end = end

    def __call__(self, *args, **kwargs):
        """

        :param args: 命令选项，被大括号包裹。
        :param kwargs: 可选命令选项，被中括号包裹，n_开头的表示不需要指定命令名称。
        :return:
        """
        kwargs = [f"{str(v)}" if k[:2] == "n_" else f"{k} = {str(v)}" for k, v in kwargs.items()]
        return CommandLine(self.name, kwargs, args, end=self.end)

