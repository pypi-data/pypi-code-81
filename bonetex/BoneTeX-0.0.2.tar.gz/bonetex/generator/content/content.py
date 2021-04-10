#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/12/3 18:43
# @Author : 詹荣瑞
# @File : content.py
# @desc : 本代码未经授权禁止商用
from typing import Union


class ContentBase(object):

    def latex(self, indent=""):
        """

        :param indent: 缩进
        :return: LaTeX2e代码
        """
        return ""

    def latex3(self, indent=""):
        return self.latex(indent)


class Content(ContentBase):

    def __init__(self, text: str, mode: str = "paragraph"):
        escape = r"\{}%"
        for e in escape:
            text = text.replace(e, "\\" + e)

        self.text = text
        self.mode = mode

    def latex(self, indent=""):
        if self.mode == "paragraph":
            out = ""
            for t in self.text.split("\n"):
                out += f"{indent}{t}\n"
            return out
        else:
            return self.text


class ContentList(ContentBase):

    def __init__(self, *contents: Union[str, ContentBase], start="", separator="\n", end="\n"):
        self.start = start
        self.separator = separator
        self.end = end

        if contents:
            self.contents = list(contents)
        else:
            self.contents = []

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        for out in self.contents:
            yield out

    def __getitem__(self, item):
        return self.contents[item]

    def append(self, *obj):
        self.contents.extend(obj)

    def latex(self, indent=""):
        contents = []
        if "\n" in self.separator:
            new_indent = indent
        else:
            new_indent = ""
            self.start += indent
        for c in self.contents:
            if hasattr(c, "latex"):
                contents.append(c.latex(new_indent))
            else:
                contents.append(f"{new_indent}{str(c)}")
        contents = self.start + self.separator.join(contents) + self.end
        return contents


class Attribute(Content):

    def __init__(self):
        super().__init__()


class Element(Content):

    def __init__(self):
        super().__init__()
