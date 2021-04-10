#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/24 17:08
# @Author : 詹荣瑞
# @File : environment.py
# @desc : 本代码未经授权禁止商用
from bonetex.generator.content.content import ContentList, ContentBase
from bonetex.generator.content.command import Command
from typing import Tuple


class Environment(ContentBase):
    command_begin = Command("begin", end="\n")
    command_end = Command("end")

    def __init__(self, name, contents: ContentList = None, option: Tuple[list, dict] = None):
        if option is None:
            option = ((), {})
        self.name = name
        self.begin = self.command_begin(name, *option[0], **option[1])
        self.end = self.command_end(name)
        if contents is not None:
            self.contents = contents
        else:
            self.contents = ContentList()

    def __iter__(self):
        for out in self.contents:
            yield out

    def latex(self, indent=""):
        next_indent = indent + "  "
        out = self.begin.latex(indent)
        out += f"\n{self.contents.latex(next_indent)}\n"
        out += self.end.latex(indent)
        return out

    def latex3(self, indent=""):
        return self.latex(indent)


class FileEnvironment(Environment):

    def __init__(self, name, contents: ContentList = None, option: Tuple[list, dict] = None,
                 resources_folder=""):
        self.resources_folder = resources_folder
        super().__init__(name, contents, option)
