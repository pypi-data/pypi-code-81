# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/11
from yqn_project_cli.utils.core.parser import DAArgument, DARequestParser


class MainIndexParser(DARequestParser):
    choices1 = DAArgument('choices1', required=True, type=int, location='args')
    choices2 = DAArgument('choices2', required=True, type=int, location='args')

    @staticmethod
    def parse(data):
        print('parse', data)
        return data

    @staticmethod
    def parse_choices1(value):
        print('parse_choices1', value)
        return value
