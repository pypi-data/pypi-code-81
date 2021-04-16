#！/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/5 14:12
# @Author : Cuiluming
# @File : test.py
# @Software: PyCharm
from xlrd import xldate_as_tuple
from datetime import datetime
import xlrd
import os,queue
from operator import itemgetter
# import accio.locust_run

class file_analysis(object):
    @staticmethod
    def creatparm(project_name,loadfile):
            root_path = os.path.join(os.getcwd())
            book = xlrd.open_workbook(os.path.join(str(root_path),'projects',project_name,'Params', 'Excel',loadfile))
            # book =xlrd.open_workbook("F:\\accio_ui\\projects\\www24\\Params\\Excel\\performance_1612409441.xls")
            # 获取第一个sheet页
            sheet1 = book.sheets()[0]
            # 获取总行数
            rows = sheet1.nrows
            # 获取总列数
            cols = sheet1.ncols
            # print(cols)
            col_dict = {}
            for i in range(sheet1.ncols):
                col_dict[sheet1.cell_value(0, i)] = i
                # print(i)
                # print(col_dict.keys())
            # 输出每一列数据
            all_content = []
            for i in range(cols):
                col_content = []
                j = 1
                for j in range(rows):
                    ctype = sheet1.cell(j, i).ctype  # 表格的数据类型
                    # ctype = sheet1.cell(i, j).ctype
                    cell = sheet1.cell_value(j, i)  # 取第i列第j行数据
                    if ctype == 2 and cell % 1 == 0:  # 如果是整形
                        cell = int(cell)
                    elif ctype == 3:  # 如果是日期型
                        # 转成datetime对象
                        date = datetime(*xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%d/%m %H:%M:%S')
                    elif ctype == 4:  # 如果是boolean型
                        cell = True if cell == 1 else False
                    elif ctype==1:# 如果是str
                        cell=cell
                    col_content.append(cell)
                all_content.append(col_content)
            # print(all_content)
            new_dict = {}
            listkey = []
            for key in col_dict.items():
                listkey.append(list(key))
            count = 0
            for i in all_content:
                tem_list = []
                for j in i[1:]:
                    tem_list.append(j)
                new_dict[listkey[count][0]] = tem_list
                # print(new_dict)
                count += 1

            # 获取sheet对象
            sheet = book.sheet_by_index(0)
            rows, cols = sheet.nrows, sheet.ncols
            title = sheet.row_values(0)
            # print(title)
            return new_dict,title

    @staticmethod
    def put_queue_data(new_dict,title):
        class_list = []
        title_list = []
        for i in title:
            j=i.split(".")
            class_list.append(j[0])
            title_list.append(j[1])
        # 去重之后的class_list
        class_list=sorted(set(class_list), key=class_list.index)
        queue_parm_count = []
        queue_assert_count = []
        for i in range(len(class_list)):
            queue_parm_count.append("queue_data_parm{0}".format(i+1))
            queue_assert_count.append("queue_data_assert{0}".format(i+1))

        re_str = ""
        jshu = 0
        re_str_assert = ""
        index_class_list = 0 #下标
        key_list = []
        for k, v in new_dict.items():
            key_list.append(k)
            # 一次读入多列值
        out = itemgetter(*key_list)(new_dict)
        max_len = 0
        for i in out:
            if max_len < len(i):
                max_len = len(i)
        for s in range(len(class_list)):
            re_str = ""
            re_str_assert = ""
            data = [x for j, x in enumerate(title) if x.find(class_list[s]) != -1]

            print(data)
            for i in data:
                if i.find('expect_value')>=0 :
                    # 增加断言
                    re_str_assert = re_str_assert + "\"expect_value\"" + ":out[" + str(jshu) + "][count]"
                else:
                    re_str = re_str + "\"" + i.split(".")[1] + "\"" + ":out[" + str(jshu) + "][count]" + ","
                    jshu += 1

            re_str =  "params = {"+re_str[:-1]+"}"
            re_str_assert =  "params = {"+re_str_assert[:-1]+"}"
            jshu += 1
            count = 0
            for i in range(max_len):
                for j in range(len(data)):
                    i.split(".")[1]:out[j][count]
                    count += 1
            #     queue_data_parm1.put_nowait(params)


            # queue_parm_count[s]= queue.Queue()
            # queue_assert_count[s]= queue.Queue()


        # return queue_data_parm1, queue_data_assert1, queue_data_parm2, queue_data_assert2




if __name__ == '__main__':
    f=file_analysis()
    new_dict,title = f.creatparm("www24",loadfile="loadfile.xlsx")
    f.put_queue_data(new_dict,title)

