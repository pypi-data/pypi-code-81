#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/25 10:42
# @Author : 詹荣瑞
# @File : table.py
# @desc : 本代码未经授权禁止商用
import xlrd
import re
import csv
from typing import Union, List
from bonetex.generator.environment import Environment
from bonetex.generator.content.content import ContentList, ContentBase
from bonetex.generator.content.command import Command, CommandLine
from bonetex.generator import utils
__all__ = ["Tabular", "TableBase", "ExcelTable", "CSVTable", "ArrayTable"]


class Tabular(Environment):

    def __init__(self, arrangement=""):
        super(Tabular, self).__init__("tabular")
        self.arrangement = arrangement
        self.begin = Command("begin", end="\n")
        self.contents.separator = "\n"
        self.columns_num = 0

    def load(self, tabular_list: List[Union[str, list]]):
        """

        :param tabular_list: 具有一定结构的列表，[[columns_num, arrangement method],[*arrangement],...]
        :return: self
        """
        self.columns_num, a_mode = tabular_list[0]
        if a_mode == "alone":
            self.arrangement = "".join(tabular_list[1][:2]) * self.columns_num + tabular_list[1][2]
        elif a_mode == "full":
            self.arrangement = "|" + "|".join(tabular_list[1]) + "|"
        elif a_mode == "string":
            self.arrangement = tabular_list[1]

        contents = []
        for line in tabular_list[2:]:
            if isinstance(line, str):
                contents.append(CommandLine(line, [], [], end=""))
            else:
                contents.append(ContentList(*filter(None, line), separator=" & ", end=r"\\"))
        self.contents.append(*contents)
        return self

    def latex(self, indent=""):
        a_num = len(re.compile(r"[lcrpmb]").findall(self.arrangement))
        if a_num != self.columns_num:
            self.arrangement += self.arrangement[-1] * (self.columns_num - a_num)
        next_indent = indent + "  "

        out = self.begin("tabular", self.arrangement).latex(indent)
        out += self.contents.latex(next_indent)
        out += self.end.latex(indent)
        return out


class TableBase(Environment):
    command_multicolumn = Command("multicolumn", "")
    command_multirow = Command("multirow", "")

    def __init__(self, name, centering=True, table_mode="htbp"):
        self.forms = ContentList(separator="\n", end="")
        super(TableBase, self).__init__("table", ContentList(
            utils.commandline_centering if centering else ContentBase(),
            utils.command_caption(name),
            utils.command_label(f"tab:{id(self)}"),
            self.forms
        ), ([], {"n_float": table_mode}))

    def load(self, *tabular_lists: List[Union[str, list]]):
        for tl in tabular_lists:
            self.forms.append(Tabular().load(tl))
        return self

    def latex(self, indent=""):
        next_indent = indent + "  "

        out = self.begin.latex(indent)
        out += self.contents.latex(next_indent)
        out += self.end.latex(indent)
        return out


class ArrayTable(TableBase):

    def load(self, array, arrangement: str = "c"):
        if len(arrangement) == 1:
            mode = "alone"
            arrangement = ["|", arrangement, "|"]
        else:
            mode = "string"
        num = 0
        tabular_list = [[0, mode], arrangement, "hline"]

        for line in array:
            tabular_list.append(line)
            tabular_list.append("hline")
            num = max(len(line), num)

        tabular_list[0][0] = num
        super(ArrayTable, self).load(tabular_list)
        return self


class CSVTable(TableBase):

    def load(self, path, arrangement: str = "c"):
        if len(arrangement) == 1:
            mode = "alone"
            arrangement = ["", arrangement, ""]
        else:
            mode = "string"
        num = 0
        tabular_list = [[0, mode], arrangement, "toprule"]
        with open(path)as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                tabular_list.append(row)
                num = max(len(row), num)
        tabular_list[0][0] = num
        tabular_list.append("bottomrule")
        tabular_list.insert(4, "midrule")
        super(CSVTable, self).load(tabular_list)
        return self


class ExcelTable(TableBase):
    def load(self, path, arrangement: str = "c", load_merge_cell=True):
        data = xlrd.open_workbook(path)
        if len(arrangement) == 1:
            mode = "alone"
            if load_merge_cell:
                arrangement = ["", arrangement, ""]
            else:
                arrangement = ["|", arrangement, "|"]
        else:
            mode = "string"
        for sheet in data.sheets():
            tabular_list = [[sheet.ncols, mode], arrangement, "hline"]
            for r in range(sheet.nrows):
                tabular_list.append(sheet.row_values(r))
                if not load_merge_cell:
                    tabular_list.append("hline")
            if load_merge_cell:
                for row1, row2, col1, col2 in sheet.merged_cells:
                    col_num = col2 - col1
                    row_num = row2 - row1
                    tabular_list_row = tabular_list[row1 + 3]
                    if row2 == row1 + 1:
                        merged_col_cell = self.command_multicolumn(col_num, "c", tabular_list_row[col1])
                        tabular_list[row1 + 3] = [
                            *tabular_list_row[:col1],
                            merged_col_cell.latex(),
                            *[None] * (col_num - 1),
                            *tabular_list_row[col2:]
                        ]
                    else:
                        merged_row_cell = self.command_multirow(row_num, "*", tabular_list_row[col1])
                        merged_col_cell = self.command_multicolumn(col_num, "c", merged_row_cell.latex())
                        tabular_list[row1 + 3] = [
                            *tabular_list_row[:col1],
                            merged_col_cell.latex(),
                            *[None] * (col_num - 1),
                            *tabular_list_row[col2:]
                        ]
                        merged_col_cell = self.command_multicolumn(col_num, "c", "")
                        for i in range(row1 + 4, row2 + 3):
                            tabular_list[i] = [
                                *tabular_list[i][:col1],
                                merged_col_cell.latex(),
                                *[None] * (col_num - 1),
                                *tabular_list[i][col2:]
                            ]
                tabular_list.append("hline")
                tabular_list.insert(4, "hline")
            super(ExcelTable, self).load(tabular_list)
        return self
