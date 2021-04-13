#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 15:20
    @Author : Yin Jian
    @Version：V 0.1
    @File : auth.py
    @desc :
"""
import base64
import hashlib
import hmac

from Crypto.Cipher import AES

from datavita.core.utils.compat import str


class Auth:
    """格式化传入参数后进行的 hmac_sha1

     :param access_id:
     :param access_secret:
     """

    def __init__(self, access_id: str, access_secret: str):
        self.access_id = access_id
        self.access_secret = access_secret

    def make_authorization(self, data) -> str:
        """
            生成sign字符串
        """
        hmac_code = hmac.new(self.access_secret.encode(), data.encode(), hashlib.sha1).digest()
        vr = base64.b64encode(hmac_code).decode()
        return vr

    def aes_decode(self, data):
        """
            解密方法
        :param data:
        :return:
        """
        try:
            # 初始化加密器
            aes = AES.new(str.encode(self.access_secret), AES.MODE_ECB)
            # 解密
            decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")
            # 去除多余补位
            decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]
            return decrypted_text
        except Exception as e:
            raise e
