# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import os
import json
import types
import errno
import random
import socket
import requests
import termcolor
from requests_toolbelt.multipart.encoder import MultipartEncoder


def merge_iterable_objs(*args):
    _ = []

    for arg in args:
        if isinstance(arg, (list, set, tuple)):
            for _arg in arg:
                _.extend(merge_iterable_objs(_arg))
        else:
            _.append(arg)

    return _


def error_mark(str_):
    print(termcolor.colored(str(str_), 'red'))


def warning_mark(str_):
    print(termcolor.colored(str(str_), 'yellow'))


def health_mark(str_):
    print(termcolor.colored(str(str_), 'green'))


def color_mark(str_, color='blue'):
    print(termcolor.colored(str(str_), str(color)))


def upload_to_oss(target_name, content):
    upload_url = "http://ws.yqn.qa2:30016/api/File/UploadProcess"
    multipart_encoder = MultipartEncoder(
        fields={
            'FileTypeId': '9',
            'Folder': 'file_convert_org',
            'File': ('{file_name}'.format(file_name=target_name), content, 'application/octet-stream')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    headers = {
        'Content-Type': multipart_encoder.content_type
    }
    try:
        response = requests.post(upload_url, data=multipart_encoder, headers=headers)
    except Exception as e:
        print(e)
        return ''

    response_json = json.loads(response.text)

    if response_json['isSuccess'] and response_json['data'] and response_json['data'][0]['isSuccess']:
        return response_json['data'][0]['fileUrl'][:response_json['data'][0]['fileUrl'].index('?')]  # 文件过期问题临时处理
    else:
        return ''


def load_module_from_pyfile(path, silent=False):
    d = types.ModuleType("route")
    d.__file__ = path
    try:
        with open(path, "rb") as config_file:
            exec(compile(config_file.read(), path, "exec"), d.__dict__)
    except IOError as e:
        if silent and e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
            return False
        e.strerror = "无法读取文件 (%s)" % e.strerror
        raise
    return d


def host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("114.114.114.114", 53))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        error_mark(e)
        return "127.0.0.1"
    else:
        return ip


def host_name():
    return socket.gethostname()


def conf_loader(path):
    config = None
    path = str(path)

    def _config_loader(upper_name, default=None):
        nonlocal config
        upper_name = str(upper_name)
        if config is None and os.path.exists(path):
            config = load_module_from_pyfile(path)

        if getattr(config, upper_name, False):
            return getattr(config, upper_name)

        elif os.environ.get(upper_name, False):
            return os.environ.get(upper_name)

        else:
            return default

    return _config_loader


if __name__ == '__main__':
    print(merge_iterable_objs([1], 4, [5, [6, 7]]))
