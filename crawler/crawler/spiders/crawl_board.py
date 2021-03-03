import scrapy
import json
from datetime import date, timedelta

class BoardSpider(scrapy.Spider):
    """ Parse threads of th board
        input: start urls
        input type: str
        input: parsing deep
        input: date in str format
        output: csv file
    """

    #spider variables
    name = "board_spider"
    start_urls = ["http://fishing.kiev.ua/vb3/forumdisplay.php?f=216"]

    # Parsing depth variables
    def __init__(self):
        self.parsing_depth = timedelta(days=2) #get N days old threads
        self.today = 'Сегодня'
        self.yesterday = 'Вчера'


    def parse(self, response):
        """ recursively parse threads to the given deep """

        # get pagination and next page url
        tables = response.xpath('//table')
        next_page = tables[11].css('a::attr(href)').get()

        # get all threads
        threads = response.xpath("//tbody[@id='threadbits_forum_216']")
        rows = threads.xpath('tr')

        # define clipboard
        threads_data = []

        # get data from all threads
        for row in rows:
            # take columns
            cols = row.xpath('td')

            # pinned topic?
            sticky = "Важная тема"
            pinned = False
            alts = cols[2].css('img::attr(alt)').getall()
            if sticky in alts:
                pinned = True

            #get date
            thread_update_date = cols[3].xpath('div').css('::text').get()
            thread_update_date = ''.join(thread_update_date.split())

            if thread_update_date == self.today:
                thread_update_date = date.today()
            elif thread_update_date == self.yesterday:
                thread_update_date = date.today() - timedelta(days=1)
            else:
                thread_update_date = thread_update_date.split('.')
                thread_update_date = date(day=int(thread_update_date[0]), \
                                          month=int(thread_update_date[1]), \
                                          year=int(thread_update_date[2])
                                          )

            #stop if thread_update_date exceeds parsing_depth
            if date.today() - thread_update_date > self.parsing_depth:
                if not pinned:
                    break


            # get url for the topic
            thread_id = cols[0].attrib['id']
            thread_id = thread_id.split("_")[-1]
            url = f"showthread.php?t={thread_id}"

            # get title
            title = cols[2].xpath('div/a')
            title = title.css("a::text").get()

            # get topic starter profile link
            author_link = cols[2].css("span::attr(onclick)").get()
            author_link = author_link.split("'")[1]

            # get topic starter name
            author_name = cols[2].css("span::text").getall()[-1]

            # write down to the clipboard
            threads_data.append([pinned, thread_id, author_name, author_link, \
                                title, thread_update_date.__str__(), url])

        # write down to the file
        data_to_write = json.dumps(threads_data)
        with open('threads.csv', 'w') as f:
            f.write(data_to_write)
