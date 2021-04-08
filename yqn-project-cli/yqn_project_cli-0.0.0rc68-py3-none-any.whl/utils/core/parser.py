# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/13
import abc
import inspect
from flask_restx.reqparse import (
    Argument,
    RequestParser
)
from yqn_project_cli.utils.core.exceptions import APIException


class DAArgument(Argument):
    """ http request 参数对象化及校验提示转换 """
    def handle_validation_error(self, error, bundle_errors):

        error_str = str(error)

        if "Missing required parameter" in error_str:
            error_msg = '必传参数'

        elif 'not a valid choice' in error_str:
            error_msg = '不是有效选项'

        elif 'invalid literal for int' in error_str or 'not a valid integer' in error_str:
            error_msg = '不是有效整数'

        elif 'must be a non-negative integer' in error_str:
            error_msg = '不是非负整数'

        elif 'must be a positive integer' in error_str:
            error_msg = '不是正整数'

        elif 'must be within the range' in error_str:
            error_msg = '不在有效范围'

        elif 'boolean type must be non-null' in error_str:
            error_msg = '布尔类型禁止为空'

        elif 'Invalid literal for boolean()' in error_str:
            error_msg = '不支持转为布尔类型'

        elif 'Invalid date literal' in error_str:
            error_msg = '不是有效日期'

        elif 'not a valid ipv4 address' in error_str:
            error_msg = '不是有效IPv4'

        elif 'not a valid ipv6 address' in error_str:
            error_msg = '不是有效IPv6'

        elif 'not a valid ip' in error_str:
            error_msg = '不是有效IP'

        elif 'not a valid email' in error_str:
            error_msg = '不是有效邮箱'

        elif 'does not match pattern' in error_str:
            error_msg = '不符匹配规则'

        elif 'Expected a valid ISO8601 date/time interval' in error_str \
                or 'must be a valid ISO8601 date/time interval' in error_str:
            error_msg = '不是ISO8601格式日期时间'

        elif 'not a valid URL' in error_str:
            error_msg = '不是有效链接'

        else:
            error_msg = error_str

        raise APIException('请求参数有误', data={self.name: error_msg})


class DARequestParser(RequestParser):
    """ http request 参数解析 """
    def __init__(self, *args, **kwargs):
        super(DARequestParser, self).__init__(*args, **kwargs)
        arguments = inspect.getmembers(self.__class__, lambda arg: isinstance(arg, DAArgument))
        for name, argument in arguments:
            self.add_argument(argument)

    def parse_args(self, req=None, strict=False):
        try:
            result = super(DARequestParser, self).parse_args(req, strict)

            for k, v in result.items():
                single_parser = getattr(self, 'parse_' + str(k), False)
                if single_parser and callable(single_parser):
                    single_parser(v)

            general_parser = getattr(self, 'parse', False)
            if general_parser and callable(general_parser):
                general_parser(result)

        except Exception as e:
            raise e

        else:
            return result


class DAJsonBase(metaclass=abc.ABCMeta):
    """DAJson解析调用"""
    @abc.abstractmethod
    def to_json(self):
        raise NotImplementedError
