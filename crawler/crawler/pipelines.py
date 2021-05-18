# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ThreadPipeline:

    collection_name = 'threads'

    def __init__(self, sqlite_db):
        self.sqlite_db = sqlite_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_db=crawler.settings.get('SQLITE_DB')
        )

    def open_spider(self, spider):
        self.con = sqlite3.connect(self.sqlite_db)
        self.cur = self.con.cursor()

        try:
            self.cur.execute("""DROP TABLE temp_threads""")
        except:
            pass

        try:
            self.cur.execute("""CREATE TABLE temp_threads
                        (pinned text, thread_id integer, author_name text,
                        author_link text, title text, update_date text, url text)""")
        except:
            pass

        self.con.commit()


    def close_spider(self, spider):
        self.con.close()


    def process_item(self, item, spider):
        vals = tuple(item.values())
        self.cur.execute("INSERT INTO temp_threads VALUES (" + 6*'?, ' + '?)', vals)
        self.con.commit()
        return item
