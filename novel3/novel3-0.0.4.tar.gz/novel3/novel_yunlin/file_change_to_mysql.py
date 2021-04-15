'''
Author: GanJianWen
Date: 2021-02-26 20:53:59
LastEditors: GanJianWen
LastEditTime: 2021-02-27 18:28:31
QQ: 1727949032
GitHub: https://github.com/1727949032a/
Gitee: https://gitee.com/gan_jian_wen_main
'''
from py3db import mysql, log
from os import listdir
from os import path
import json


class FileToMySql:
    def __init__(self) -> None:
        self.mysql_config = self.get_mysql_config()
        self.ip = self.mysql_config["ip"]
        self.user = self.mysql_config["user_name"]
        self.password = self.mysql_config["password"]
        self.database = self.mysql_config["database"]
        self.fp = open("%s/../json/illegal_chapter_name.json" %
                       path.abspath(__file__), 'r', encoding='utf-8')
        self.datas = json.load(self.fp)
        self.log = log.Log("./mysql.log")
        self.mysql = mysql.MySql(
            self.ip, self.user, self.password, self.database)

    @classmethod
    def get_mysql_config(cls):
        mysql_config_path = "%s/../config/mysql.json" % path.abspath(__file__)
        return json.load(fp=open(
            mysql_config_path,
            "r",
            encoding="utf-8"
        ))

    def get_book_name_from_mysql(self):
        self.db = self.mysql.create_connect()
        sql = "select book_name from book where latest=0;"
        cursor = self.mysql.db.cursor()
        cursor.execute(sql)
        book_name_list = cursor.fetchall()
        self.mysql.close_connect()
        return book_name_list

    def clear_illegal_chapter_name(self, chapter_name):
        for illegal in self.datas:
            chapter_name = chapter_name.replace(illegal, '')
        return chapter_name

    def insert_book_all_chapters(self):
        book_name_list = self.get_book_name_from_mysql()
        for book_message in book_name_list:
            book_name = book_message[0]
            self.log.info("正在插入%s" % book_name)
            book_path = "小说/%s" % book_name
            chapter_list = listdir(book_path)
            if not chapter_list:
                continue
            else:
                chapter_list = sorted(
                    chapter_list, key=lambda x: path.getctime(path.join(book_path, x)))

            for chapter in chapter_list:
                chapter_path = "小说/%s/%s" % (book_name, chapter)
                with open(chapter_path, 'r', encoding='utf-8') as fp:
                    contents = fp.read()
                    fp.close()
                chapter_name = chapter.replace(
                    '.html', '')
                chapter_name = self.clear_illegal_chapter_name(chapter_name)
                sql = "insert into chapter values(NULL,'%s','%s','%s');" % (
                    book_name, chapter_name, contents)
                self.db = self.mysql.create_connect()
                self.mysql.operation_database(sql, chapter_name)
            update = "update book set latest=1 where book_name='%s';" % book_name
            self.mysql.operation_database(update)


if __name__ == "__main__":
    file_to_mysql = FileToMySql()
    file_to_mysql.insert_book_all_chapters()
