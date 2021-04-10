#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/28 0:04
# @Author : 詹荣瑞
# @File : document.py
# @desc : 本代码未经授权禁止商用
from bonetex.generator.content.content import ContentList
from bonetex.generator.content.command import Command
from bonetex.generator.environment import Environment
from bonetex.generator import utils
__all__ = ["Document"]


class Document(object):
    command_document_class = Command("documentclass")

    def __init__(self, document_class="article", document_option=None, generate_mode="latex2e"):
        if document_option is None:
            document_option = {}
        if document_class is None:
            self.preamble = ContentList(separator="\n")
        else:
            self.preamble = ContentList(
                self.command_document_class(document_class, **document_option),
                separator="\n"
            )
        self.body = Environment("document", ContentList(separator="\n", end=""))
        self.mode = generate_mode
        self.package = []

        # 方法别名
        self.pre_append = self.pre_append
        self.append = self.body_append

    def reset(self, document_class="article", document_option=None):
        if document_option is None:
            document_option = {}
        self.preamble = ContentList(
            self.command_document_class(document_class, **document_option),
            separator="\n"
        )
        self.body = Environment("document", ContentList(separator="\n", end=""))
        self.package = []

    def use(self, func):
        use = utils.command_use_package
        self.package.append(func)
        if func == "math":
            self.preamble.append(use("array"))
            self.preamble.append(use("amsmath"))
        if func == "cn":
            self.preamble.append(use("ctex"))
        if func == "minipage":
            self.preamble.append(use("minipage"))
        if func == "base":
            self.preamble.append(use("ctex"))
            self.preamble.append(use("multirow"))
            self.preamble.append(use("graphicx"))

    def latex(self):
        if self.mode == "latex2e":
            out = self.preamble.latex()
            out += self.body.latex()
            return out

    def pre_append(self, *contents):
        self.preamble.append(*contents)
        return self

    def body_append(self, *contents):
        # for c in contents:
        #     if hasattr(c, "package"):
        #         self.package.append(c.package)
        self.body.contents.append(*contents)
        return self

    def title(self, title, author=None):
        self.pre_append(utils.command_title(title))
        if author is not None:
            self.pre_append(utils.command_author(r"Bone\TeX"))
        self.body_append(utils.command_make_title())
