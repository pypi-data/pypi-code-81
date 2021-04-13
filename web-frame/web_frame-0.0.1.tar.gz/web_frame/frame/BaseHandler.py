import types
from abc import ABC
from typing import Any

import tornado.web
import tornado.ioloop

import json

from tornado import httputil
from tornado.web import Application

from web_frame.context import config
from web_frame.frame.HandlerHelper import check_auth, command_mapper
from web_frame.utils.CommonUtil import CJsonEncoder
from web_frame.utils.DataClient import DataClient
from web_frame.utils.FileUtil import file_upload
from web_frame.utils.IOUtil import ERRMSG_OK, ERRNO_OK, ERRNO_INVALID_PARAM
from web_frame.utils.JwtUtil import auth


class BaseHandler(tornado.web.RequestHandler, ABC):
    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any):
        super().__init__(application, request, **kwargs)
        self.command_map = {}
        methods = self.methods()
        self.client = DataClient(config.data_server_url)
        for i in range(len(methods)):
            method = getattr(self, methods[i])
            if getattr(method, "__req__", None):
                self.command_map[method.__command__] = method

    def methods(self):
        return (list(filter(
            lambda m: not m.startswith("__") and not m.startswith("_") and callable(getattr(self, m)) and
                      type(getattr(self, m, None)) == types.MethodType,
            self.__dir__())))

    @check_auth
    @command_mapper
    def get(self):
        pass

    @check_auth
    @command_mapper
    def post(self):
        pass

    def set_default_header(self):
        origin = self.request.headers.get("Origin")
        if origin:
            self.set_header("Access-Control-Allow-Origin", origin)
        else:
            self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
        self.set_header("Access-Control-Expose-Headers", "Access-Token")
        self.set_header("Access-Control-Allow-Credentials", "true")

        return True

    def options(self):
        self.set_default_header()
        self.write({
            "errno": 0,
        })

    def write_custom_error(self, errno, errmsg):
        self.write({
            "errno": errno,
            "errmsg": errmsg,
        })

    def write_401(self):
        self.set_status(401)

    def write_json_data(self, data):
        self.write(json.dumps(data, cls=CJsonEncoder, ensure_ascii=False))

    def write_data(self, data):
        self.write(data)

    # 注册用户权限验证  判断token 和token中key 是否合法, cookie中是否有用户信息,默认有效期1月
    def set_current_user(self, username):
        self.set_secure_cookie("user", username)

    def get_current_user(self) -> Any:
        username = self.get_secure_cookie("user")
        if isinstance(username, bytes) or isinstance(username, bytearray):
            username = username.decode("utf-8")
        return username

    def auth_login(self):
        return auth(self.get_token(), self.current_user)

    def get_token(self):
        token = self.request.headers.get("Authorization", None)
        if token is None:
            token = self.get_argument("token", "")
        return token

    def can_read_cache(self):
        can_cache = self.request.headers.get("Can-read-cache", "True")
        if can_cache.lower() == "false":
            can_cache = False
        else:
            can_cache = True
        return can_cache

    def upload_file(self, file_key, file_checker=lambda x: True):
        file_metas = self.request.files.get(file_key, None)
        filename = file_metas[0]['filename']
        if not file_checker(filename):
            return self.write_data(self.result_err("文件上传失败：{} 文件格式不匹配！".format(filename)))
        return file_upload(file_metas, config.temp_path)

    @staticmethod
    def result_ok(data=None, errmsg=ERRMSG_OK):
        res = {
            "errno": ERRNO_OK,
            "errmsg": errmsg,
        }
        if data is not None:
            res["data"] = data
        return res

    @staticmethod
    def result_err(msg, errno=ERRNO_INVALID_PARAM):
        return {
            "errno": errno,
            "errmsg": msg,
        }

    @staticmethod
    def result_custom_ok(data, **kwargs):
        kwargs["errno"] = ERRNO_OK
        kwargs["errmsg"] = ERRMSG_OK
        kwargs["data"] = data
        return kwargs
