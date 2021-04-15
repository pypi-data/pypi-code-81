# -*- encoding: utf-8 -*-
'''
@文件    :base.py
@说明    :
@时间    :2021/02/22 17:59:21
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''
from typing import Union
import os
import codecs
import pickle

def project_root_path(cur_file, projectname, *args, **kwargs):

    _project_root_dir = os.path.join(os.path.abspath(os.path.dirname(cur_file)).split(projectname)[0], projectname)
    return os.path.join(_project_root_dir, *args)

def read_params_from_localfile(filepath: str) -> Union[None, dict]:
    """
    从本地文件读取运行时参数
    :param filepath str 参数文件
    """
    ret_params = None
    if os.path.exists(filepath) and os.path.isfile(filepath):
        with codecs.open(filepath, "rb") as _f:
            _fcc = _f.read()
            try:
                ret_params = pickle.loads(_fcc)
            except Exception as e:
                print(e)
    return ret_params

def write_params_to_localfile(filepath: str, obj: dict) -> bool:
    """
    往本地文件写入运行时参数
    :param filepath str 参数文件
    :param obj dict 写入内容
    """
    ret_check = False
    try:
        with codecs.open(filepath, "wb") as _f:
            _f.write(pickle.dumps(obj))
            ret_check = True
    except Exception as e:
        print(e)
    return ret_check