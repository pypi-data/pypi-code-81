#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/25 11:00
# @Author : 詹荣瑞
# @File : sequence.py
# @desc : 本代码未经授权禁止商用
from . import Environment
from bonetex.generator.content.content import ContentList, ContentBase
from bonetex.generator.content.command import Command
from typing import Union

commandline_item = Command("item")()


class Sequence(Environment):

    def __init__(self, *contents: Union[str, ContentBase], order=True):
        if order:
            name = "enumerate"
        else:
            name = "itemize"

        item = commandline_item.latex(" ") + "\n"
        super(Sequence, self).__init__(
            name,
            ContentList(*contents, start=item, separator=item)
        )

    def latex(self, indent=""):
        next_indent = indent + "  "

        out = self.begin.latex(indent)
        out += self.contents.latex(next_indent)
        out += self.end.latex(indent)
        return out
