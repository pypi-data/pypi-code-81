# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     encrypt
   Description :   用于编码转码
   Author :        Asdil
   date：          2021/3/31
-------------------------------------------------
   Change Activity:
                   2021/3/31:
-------------------------------------------------
"""
__author__ = 'Asdil'
import base64
import pickle


def base_encrypt(data):
    """base_encrypt方法用于base64转码

    Parameters
    ----------
    data : str
        需要转码的字符串
    Returns
    ----------
    """
    data = bytes(data, encoding="utf8")
    encrypt_data = base64.b64encode(data)
    encrypt_data = str(encrypt_data, encoding="utf8")
    return encrypt_data


def base_decrypt(data):
    """base_decrypt方法用于

    Parameters
    ----------
    data : str
        转码后字段

    Returns
    ----------
    """
    data = bytes(data, encoding="utf8")
    decrypt_data = base64.b64decode(data)
    decrypt_data = str(decrypt_data, encoding="utf8")
    return decrypt_data


def encode(data):
    """encode方法用于压缩数据编程字符串

    Parameters
    ----------
    data : object
        任何对象

    Returns
    ----------
    """
    data = pickle.dumps(data)
    data = base64.b64encode(data)
    return data


def decode(data):
    """decode方法用于解压byte字符串转化为对象

    Parameters
    ----------
    data : byte
        byte对象
    Returns
    ----------
    """
    if type(data) is dict:
        return data
    data = base64.b64decode(data)
    data = pickle.loads(data)
    return data