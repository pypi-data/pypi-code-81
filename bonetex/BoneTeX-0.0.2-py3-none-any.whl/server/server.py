#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/19 12:59
# @Author : 詹荣瑞
# @File : server.py
# @desc : 本代码未经授权禁止商用
import code
import os
from flask_socketio import SocketIO

from apiflask import APIFlask, Schema, input, output
from apiflask.fields import String
from flask import request, jsonify
from bonetex.parser import parse, parse_block, code_init, code_reset
from bonetex.parser import parse_tex

app = APIFlask(__name__)


target_dir = os.path.join(os.getcwd(), "../../resources")
target_name = os.path.join(os.getcwd(), "../../resources")
interpreter = code.InteractiveInterpreter()
interpreter.runcode(code_init)

class ParseBlockInSchema(Schema):
    type = String(required=True)
    name = String(required=True)
    code = String(required=True)


class ParseBlockOutSchema(Schema):
    code = String(required=True)


@app.get('/get_pid')
def get_pid():
    return jsonify({
        "pid": os.getpid()
    })


@app.post('/parse')
def parse_code():
    interpreter.runcode(code_reset)
    response = {
        "block-python": {},
        "block-tex": {},
        "code-python": code_init,
        "code-tex": "",
        "code-safe-tex": "",
    }
    # method = request.json["method"].split("/")
    #
    # if method[0] == "parse_block":
    #     response["code-python"] = parse_block(request.json["name"], method[1], request.json["code"])
    # elif method[0] == "parse_full":
    if request.json["template"] == "bone":
        interpreter.runcode("render = bone_template_render")
    elif request.json["template"] == "mustache":
        interpreter.runcode("render = mustache_render")
    for name, code_block in parse(request.json["code"]):
        response["block-python"][name] = code_block
        response["code-python"] += f"\r\n{code_block}\r\n"
        interpreter.runcode(code_block)
    response["code-tex"] = interpreter.locals["_doc"].latex()
    response["code-safe-tex"] = parse_tex(response["code-tex"])

    return jsonify(response)


@app.route('/open_file', methods=["POST"])
def open_file():
    (filepath, filename_ex) = os.path.split(request.json['path'])
    (filename, extension) = os.path.splitext(filename_ex)
    os.chdir(filepath)
    # print(os.path.join(filepath, filename))
    interpreter.runcode(
        f"_compiler = Compiler(_doc, r'{os.path.join(filepath, filename)}', "
        f"compilers='xelatex')"
    )
    return jsonify({
        "success": True
    })


@app.route('/save', methods=['POST'])
def save():
    success = True
    try:
        with open(request.json["dir"], mode="w", encoding="utf-8") as file:
            file.write(request.json["code"].replace("\r\n", "\n"))
    except FileNotFoundError:
        success = False

    return jsonify({
        "success": success
    })


@app.route('/generate', methods=['Post'])
def generate():
    interpreter.runcode(
        "_compiler.generate_pdf()"
    )
    _compiler = interpreter.locals["_compiler"]
    return jsonify({
        "curdir": _compiler.path,
        "name": _compiler.name
    })


if __name__ == '__main__':
    app.run(port=6954)
