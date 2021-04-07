# -*- coding:utf-8 -*-
# @Author   : Haogooder
# @Date     : 2021/4/2
# @FileName : climan
# @Desc     : The description of this file
import argparse
import logging
from typing import TypeVar, Any, Union, List, Generic

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)-10s] %(lineno)6d:%(filename)-16s | %(message)s")
T = TypeVar('T')


class CliMan(Generic[T]):
    _arg_parser_: argparse.ArgumentParser
    _arg_obj_: argparse.Namespace

    @staticmethod
    def init(desc: str = ...):
        logging.debug("init ...")
        CliMan._arg_parser_ = argparse.ArgumentParser(description=desc)

    @staticmethod
    def add_flag(*flag_name: str, default: str = None, required: bool = False, choices: List = None,
                 help_msg: str = None, action: str = 'store', nargs: Union[int, str] = None, const: Any = None):
        if not hasattr(CliMan, "_arg_parser_"):
            raise CliParseError("Add Flag Fail, Please Invoke init()")
        logging.debug("add flag: {0}".format(flag_name))
        arg_type = str
        CliMan._arg_parser_.add_argument(*flag_name, action=action, nargs=nargs, const=const, default=default,
                                         type=arg_type,
                                         choices=choices, required=required, help=help_msg)

    @staticmethod
    def add_arg(arg_name: str, default: str = None, choices: List = None,
                help_msg: str = None, action: str = 'store', nargs: Union[int, str] = None, const: Any = None):
        if not hasattr(CliMan, "_arg_parser_"):
            raise CliParseError("Add Arg Fail, Please Invoke init()")
        logging.debug("add arg: {0}".format(arg_name))
        arg_type = str
        CliMan._arg_parser_.add_argument(arg_name, action=action, nargs=nargs, const=const, default=default,
                                         type=arg_type,
                                         choices=choices, help=help_msg)

    @staticmethod
    def parse(*args: str):
        if not hasattr(CliMan, "_arg_parser_"):
            raise CliParseError("Parse Fail, Please Invoke init() and add_arg()/add_flag()")
        logging.debug("parse ...")
        CliMan._arg_obj_ = CliMan._arg_parser_.parse_args(args)

    @staticmethod
    def get_int(key: str) -> int:
        if not hasattr(CliMan, "_arg_obj_"):
            raise CliParseError("Get Value Fail, Please Invoke init() and add_arg()/add_flag(), then parse()")

        try:
            rlt = int(CliMan._arg_obj_.__dict__.get(key))
        except ValueError:
            raise CliParseError("解析参数类型出错，请先检查参数类型设置")
        return rlt

    @staticmethod
    def get_str(key: str) -> str:
        if not hasattr(CliMan, "_arg_obj_"):
            raise CliParseError("Get Value Fail, Please Invoke init() and add_arg()/add_flag(), then parse()")

        try:
            rlt = str(CliMan._arg_obj_.__dict__.get(key))
        except ValueError:
            raise CliParseError("Parse Arg/Flag Type Fail")
        return rlt

    @staticmethod
    def get_float(key: str) -> float:
        if not hasattr(CliMan, "_arg_obj_"):
            raise CliParseError("Get Value Fail, Please Invoke init() and add_arg()/add_flag(), then parse()")

        try:
            rlt = float(CliMan._arg_obj_.__dict__.get(key))
        except ValueError:
            raise CliParseError("Parse Arg/Flag Type Fail")
        return rlt
    
    @staticmethod
    def get_bool(key: str) -> bool:
        if not hasattr(CliMan, "_arg_obj_"):
            raise CliParseError("Get Value Fail, Please Invoke init() and add_arg()/add_flag(), then parse()")

        try:
            rlt = bool(CliMan._arg_obj_.__dict__.get(key))
        except ValueError:
            raise CliParseError("Parse Arg/Flag Type Fail")
        return rlt


class CliParseError(RuntimeError):
    pass


if __name__ == "__main__":
    pass
