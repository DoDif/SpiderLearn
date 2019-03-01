# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from book.settings import MySQL_HOST
import json
import os


class BookPipeline(object):
    def process_item(self, item, spider):
        sql = """INSERT INTO book(
        book_name,book_author,book_type)
        VALUES(
        '%s','%s','%s')
        """ % (item["name"], item["author"], item["type"])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("insert OK")
        except Exception as e:
            self.db.rollback()
            print("insert Flase")
        return item

    def open_spider(self, spider):
        self.db = pymysql.connect("localhost", "root", "1123", "books", charset="utf8")

        self.cursor = self.db.cursor()
        # sql = """CREATE TABLE IF NOT EXISTS book(
        # id INT NOT NULL AUTO_INCREMENT,
        # book_name VARCHAR(10) NOT NULL,
        # book_author VARCHAR(10) NOT NULL,
        # book_type VARCHAR(4) NOT NULL,
        # PRIMARY KEY (id)
        # )ENGINE InnoDB
        # """
        # self.cursor.execute(sql)

    def close_spider(self, spider):
        self.db.close()


class ChapterPipeline(object):
    """store chapter name and url"""

    def process_item(self, item, spider):
        FileAdd = "%s/%s.json" % (os.getcwd(), item["name"])
        print("start write" + FileAdd)
        with open(FileAdd, "w") as file:
            str = json.dumps(item["chapter_info"])
            file.write(str)
            print("write OK")
