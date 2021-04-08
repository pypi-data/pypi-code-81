# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-11-25 15:32:11
:LastEditTime: 2021-04-08 17:41:56
:LastEditors: HuangJingCan
@Description: 
"""

from seven_framework.web_tornado.base_handler.base_api_handler import *


class ErpBaseHandler(BaseApiHandler):
    param_info = {}

    def get_erp_params(self, param):
        """
        @description: 获取参数
        @last_editors: XiaoYongChun  
        """
        body_json = self.request.body
        if str(body_json, "utf-8") != "":
            param_info = json.loads(body_json)

        return param_info[param]

    def check_erp_sign(self):
        """
        @description: 验证签名
        @last_editors: XiaoYongChun
        """
        appsecret = config.get_value("appsecret", "tlq1w9&t%4pf!l7uhz7ptw")

        self.request.headers["Content-type"]

        headers_dict = {}

        version = self.request.headers.get("version", "")
        nonce = self.request.headers.get("nonce", "")
        appid = self.request.headers.get("appid", "")
        time = self.request.headers.get("time", "")
        sign = self.request.headers.get("sign", "")

        headers_dict["version"] = version
        headers_dict["nonce"] = nonce
        headers_dict["appid"] = appid
        headers_dict["time"] = time

        params_sorted = sorted(headers_dict.items(), key=lambda e: e[0], reverse=False)

        sign_params = appsecret + ("".join(u"{}{}".format(k, v) for k, v in params_sorted))

        check_sign = CryptoHelper.md5_encrypt(sign_params).upper()

        if sign == check_sign:
            return True

        self.logger_error.error(f'签名校验错误,客户端传递{sign},服务端校验{check_sign},md5前字符串{appsecret + ("".join(u"{}".format(v) for k, v in params_sorted))}')
        return False

    def response_error_msg(self, state, msg):
        """
        :description: 返回错误消息
        :param state: 状态
        :param msg: 消息
        :return http_reponse
        :last_editors: XiaoYongChun
        """
        result_data = {}
        result_data["code"] = state
        result_data["msg"] = msg
        result_data["result"] = []

        self.http_reponse(JsonHelper.json_dumps(result_data))
