# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class Scrapingbook2Pipeline:
    def __init__(self):
        self.conn = sqlite3.connect('my_books.db')
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(
                            title text,
                            author text,
                            price text,
                            star text,
                            reviewNum text
                         )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into quotes_tb values (?,?,?,?)""", (
            item['title'][0],
            item['author'][0],
            item['price'][0],
            item['star'][0]
        ))
        self.conn.commit()
