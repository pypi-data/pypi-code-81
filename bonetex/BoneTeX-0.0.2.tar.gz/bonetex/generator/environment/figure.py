#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/31 19:24
# @Author : 詹荣瑞
# @File : figure.py
# @desc : 本代码未经授权禁止商用
import cv2
import os
from .environment import FileEnvironment
from bonetex.generator.content.content import ContentList, ContentBase
from bonetex.generator import utils


class FigureBase(FileEnvironment):

    def __init__(self, name, centering=True, figure_mode="htbp", resources_folder=""):
        self.graphics = ContentList(separator="\n", end="")
        super().__init__("figure", ContentList(
            utils.commandline_centering if centering else ContentBase(),
            self.graphics,
            utils.command_caption(name),
            utils.command_label(f"tab:{id(self)}")
        ), ([], {"n_float": figure_mode}), resources_folder)
        if not os.path.exists(f"{resources_folder}/images"):
            print("Create", resources_folder)
            os.mkdir(f"{resources_folder}/images")

    def load(self, *graphics: str):
        num = len(self.graphics)
        for g in graphics:
            num += 1
            img = cv2.imread(g)
            path = f"images/{id(self)}_{num}.png"
            if img is not None:
                cv2.imwrite(os.path.join(self.resources_folder, path), img)
                self.graphics.append(utils.command_include_graphics(path))
        return self

    def latex(self, indent=""):
        next_indent = indent + "  "

        out = self.begin.latex(indent)
        out += self.contents.latex(next_indent)
        out += self.end.latex(indent)
        return out
