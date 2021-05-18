import scrapy


class ThreadItem(scrapy.Item):
    pinned = scrapy.Field()
    thread_id = scrapy.Field()
    author_name = scrapy.Field()
    author_link = scrapy.Field()
    title = scrapy.Field()
    Update_date = scrapy.Field()
    url = scrapy.Field()
