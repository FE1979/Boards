import scrapy
from ..items import ThreadItem
from datetime import date, timedelta

class BoardSpider(scrapy.Spider):
    """ Parse threads of the board
        input: start urls
        input type: str
        input: parsing deep
        input type: int
        input: forum url
        input type: str
        input: board url (part of url, concat with forum url)
        input type: str
        constants: today and yesterday to get proper date
    """

    #spider variables
    name = "board_spider"


    # Parsing variables
    def __init__(self):
        self.parsing_depth = timedelta(days=3) # int(getattr(self, ' depth', None))
        self.today = 'Сегодня'
        self.yesterday = 'Вчера'
        self.forum = "http://fishing.kiev.ua/vb3/"
        self.board = "forumdisplay.php?f=216"


    def start_requests(self):
        yield scrapy.Request(self.forum + self.board, self.parse)


    def parse(self, response):
        """ recursively parse threads to the given deep """

        # get pagination and next page url
        tables = response.xpath('//table')
        next_page = tables[11].css('a::attr(href)').get()
        next_page = self.forum + next_page

        # get all threads
        threads = response.xpath("//tbody[@id='threadbits_forum_216']")
        rows = threads.xpath('tr')

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

            # yield scrapped data
            thread = ThreadItem()
            thread = {
            'Pinned': pinned,
            'Thread_id': thread_id,
            'Author_name': author_name,
            'Author_link': author_link,
            'Title': title,
            'Update_date': thread_update_date.__str__(),
            'Url': url
            }

            yield thread

        # go to next page if not the end
        if date.today() - thread_update_date < self.parsing_depth:
            yield response.follow(next_page, callback=self.parse)
