'''
Author: GanJianWen
Date: 2021-02-26 14:18:07
LastEditors: GanJianWen
LastEditTime: 2021-02-27 21:51:02
QQ: 1727949032
GitHub: https://github.com/1727949032a/
Gitee: https://gitee.com/gan_jian_wen_main
'''
from .image_to_str_map import ImageToStr
from .yun_lin_zhan_ye_scrapy import YuLinZhanYeScrapy
from .file_change_to_mysql import FileToMySql
from os import system


def spider_run():
    choose = 1
    while choose > 0:
        system("cls")
        print("1、爬取小说")
        print("2、图片转文字")
        print("3、将数据插入数据库")
        print("0、退出")
        choose = int(input("选择:"))
        if choose == 1:
            spider = YuLinZhanYeScrapy()
            spider.main()
        if choose == 2:
            demo = ImageToStr()
            demo.image_to_str()
        if choose == 3:
            demo = FileToMySql()
            demo.insert_book_all_chapters()
