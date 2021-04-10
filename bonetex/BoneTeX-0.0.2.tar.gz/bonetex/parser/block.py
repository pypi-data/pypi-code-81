#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/5 17:51
# @Author : 詹荣瑞
# @File : block.py
# @desc : 本代码未经授权禁止商用
class Block(object):

    def __init__(self, source, flag):
        self.source = source
        self.flag = flag
        self.dependencies = []
        self.parsers = {
            "script": self.parse_script,
            "structure": self.parse_script,
            "template": self.parse_script,
        }
        self.script = ""

    def parse_script(self):
        code_string = self.source.replace("$.", "_doc.")
        code_string = code_string.replace("%[", "_blocks[")
        self.script = code_string.replace("generate_pdf", "")
        # code_string = code_string.replace("generate_pdf", "_compiler.generate_pdf()")
        return self.script

    def parse(self):
        return self.parsers[self.flag]()
