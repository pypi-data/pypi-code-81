#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/6 22:08
# @Author : 詹荣瑞
# @File : bonetex_command.py
# @desc : 本代码未经授权禁止商用
import argparse
from bonetex.server.server import app
from bonetex.parser import parser_bone
from bonetex.parser.parser_bone import code_init


def main():
    try:
        methods[args.method]()
    except KeyError:
        print(f"不存在方法<{args.method}>")


def server():
    app.run(port=args.port)


def parse():
    try:
        with open(args.path + ".btex", mode='r', encoding="utf-8") as file:
            out = parser_bone.parse(file.read())
        with open(args.path + ".py", mode='w', encoding="utf-8") as file:
            file.write(code_init + "".join(code for name, code in out))
    except FileNotFoundError:
        print(f"未找到<{args.path}>文件")


parser = argparse.ArgumentParser(description='使用BoneTeX命令')
parser.add_argument('method', default="server", type=str, nargs='?',
                    help='指定BoneTeX命令方法')
parser.add_argument('--port', default=6954, type=int, help='指定服务器端口')
parser.add_argument('--path', default="", type=str, help='指定源文件')
args = parser.parse_args()
methods = {
    "server": server,
    "parse": parse,
}

if __name__ == '__main__':
    main()
