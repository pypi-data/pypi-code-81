#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/28 19:35
# @Author : 詹荣瑞
# @File : latex3.py
# @desc : 本代码未经授权禁止商用
class ContentBase(object):

    def latex(self, indent=""):
        raise NotImplementedError


class ContentChain(ContentBase):

    def __init__(self, *contents, separator=" ", end="\n"):
        self.separator = separator
        self.end = end

        if contents:
            self.contents = list(contents)
        else:
            self.contents = []

    def __iter__(self):
        for out in self.contents:
            yield out

    def append(self, *obj):
        self.contents.extend(obj)

    def latex(self, indent=""):
        contents = []
        if "\n" in self.separator:
            new_indent = indent
        else:
            new_indent = ""
        for c in self.contents:
            if hasattr(c, "latex"):
                contents.append(c.latex(new_indent))
            else:
                contents.append(f"{new_indent}{str(c)}")
        contents = indent + self.separator.join(contents) + self.end
        return contents


class Token(ContentBase):

    def __init__(self, content: ContentBase):
        self.content = content

    def latex(self, indent=""):
        new_indent = indent + "  "
        return f"{indent}{{\n{self.content.latex(new_indent)}\n{indent}}}"


class Command(ContentBase):

    def __init__(self, content: str):
        self.content = content

    def latex(self, indent=""):
        return f"{indent}\\{self.content}"


class CommandLine(ContentBase):

    def __init__(self, name, args=()):
        arg_spec = ""
        for arg in args:
            if isinstance(arg, Token):
                arg_spec += "n"
            elif isinstance(arg, Command):
                arg_spec += "N"
        name = Command(f"{name}:{arg_spec}")
        self.content = ContentChain([name, *args])

    def latex(self, indent=""):
        return self.content.latex(indent)


class LaTeX3Command(ContentBase):

    def __init__(self, name, arg_spec=""):
        self.name = name
        self.arg_spec = arg_spec

    def latex(self, indent=""):
        return f"{self.name}:{self.arg_spec}"


class LaTeX3CommandLine(ContentBase):

    def __init__(self, command, args=(), end="\n"):
        self.command = command
        self.rgs = args
        self.end = end

    def latex(self, indent=""):
        return f"{indent}{self.name}:{self.arg_spec}"


cs_set = Command("cs_set:Npn")
es_on = Command("ExplSyntaxOn")()
es_off = Command("ExplSyntaxOff")()
