#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/18 11:58
# @Author : 詹荣瑞
# @File : parser_bone.py
# @desc : 本代码未经授权禁止商用
import re

block_types = ["template", "script", "include"]
variable = r"[_A-z\u4e00-\u9fa5][_A-z\u4e00-\u9fa50-9]*"
re_block = re.compile(r"%\[(" + variable + r")]\s*([A-z-]+)\s*")
re_structure = re.compile(r"( *)([$%])\.(" + variable + r"):\s*(\S*)?\r?\n?")

code_init = (
    "import os\n"
    "from sympy import *\n"
    "from bonetex.generator import *\n"
    "from bonetex.compile import Compiler\n"
    "from bonetex.utils import *\n"
    "_doc = Document('article')\n"
    "_current_section: ContentList\n"
    "_blocks = {}\n"
)
code_reset = (
    "_doc.reset('article')\n"
    "_blocks = {}\n"
)


def func_structure(matched):
    indent, flag, key, args = matched.groups()
    if flag == "$":
        if "section" in key:
            level = key.count("sub")
            return (
                f"{indent}_current_section.append(Section({args}, level={level}))\n"
                f"{indent}_current_section = _current_section[-1]\n"
            )
        elif "table" in key:
            return (
                f"{indent}_temp_table = ArrayTable({args}.get('name', ''))\n"
                f"{indent}_temp_table.load({args}.get('content'), "
                f"{args}.get('arrangement', 'c'))\n"
                f"{indent}_current_section.append(_temp_table)\n"
            )
        # elif "content" in key:
        #     f"{indent}_current_section.append(Section({args}, level={level}))\n"
        elif "include" in key:
            with open(args, 'r', encoding='utf-8') as file:
                file.read()
            return (
                f"{indent}with open({args}, 'r', encoding='utf-8') as file:\n"
                f"{indent}    _current_section.append(file.read())\n"
            )
    elif flag == "%":
        if args:
            return f"{indent}_current_section.append(render(_blocks['{key}'], {args}))\n"
        else:
            return f"{indent}_current_section.append(_blocks['{key}'])\n"


def split_block(code_string: str):
    block = []
    for res in re_block.finditer(code_string):
        name, flag = res.groups()
        span = res.span()
        block.append((name, flag, span))
    for i, (name, flag, span) in enumerate(block[:-1]):
        yield name, flag, code_string[span[1]:block[i + 1][2][0] - 1]
    if block:
        name, flag, span = block[-1]
        yield name, flag, code_string[span[1]:]


def parse_block(name: str, flag: str, code_string: str):
    if flag == "template-tex":
        return f"_blocks['{name}'] = r'''{code_string}'''\n"
    elif flag == "structure":
        code_string = re_structure.sub(
            func_structure,
            code_string,
        )
        return (
            f"_blocks['{name}'] = ContentList()\n"
            f"_current_section: ContentList = _blocks['{name}']\n"
            f"{code_string}"
        )
    elif flag == "script":
        code_string = code_string.replace("$.", "_doc.")
        code_string = code_string.replace("%[", "_blocks[")
        code_string = code_string.replace("generate_pdf", "")
        # code_string = code_string.replace("generate_pdf", "_compiler.generate_pdf()")
        return code_string


def parse(code_string: str):
    main_code: str = ""
    # code_string = code_string.replace("\r\n", "\n")
    for name, flag, code_string in split_block(code_string):
        if name == "main":
            main_code = parse_block(name, flag, code_string)
        else:
            yield name, parse_block(name, flag, code_string)
    if main_code:
        yield "main", main_code


class Parser(object):

    def __init__(self):
        pass


if __name__ == '__main__':
    import code
    import sys

    print("# #  Started BoneTeX  # #")
    interpreter = code.InteractiveInterpreter()
    code_init = "\n".join([
        "from bonetex import Document",
        "from bonetex.content import *",
        "from bonetex.environment import *",
        "_doc = Document('article')",
        "_blocks = {}",
    ])
    interpreter.runcode(code_init)
    for name, code_block in parse(sys.argv[1]):
        interpreter.runcode(code_block)
        print(code_block)
    interpreter.runcode("print(_doc.latex())")
