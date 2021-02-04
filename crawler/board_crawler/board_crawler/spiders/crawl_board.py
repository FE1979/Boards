import scrapy

class BoardSpider(scrapy.Spider):
    """ Parse threads of th board
        input: start urls
        input type: str
        input: parsing deep
        input: date in str format
        output: csv file
    """

    name = "board_spider"

    start_urls = ["http://fishing.kiev.ua/vb3/forumdisplay.php?f=216"]


    def parse(self, response):
        """ recursively parse threads to the given deep """
        
        # get pagination and next page url
        tables = response.xpath('//table')
        next_page = tables[11].css('a::attr(href)').get()

        # get all threads 
        threads = response.xpath("//tbody[@id='threadbits_forum_216']")
        rows = threads.xpath('tr')

        # define clipboard
        threads_data = ""

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

            # get url for the topic
            url = cols[2].css("a::attr(href)").get()

            # get title
            title = cols[2].xpath('div/a')
            title = cols[2].css("a::text").get()

            # get topic starter profile link
            author_link = cols[2].css("span::attr(onclick)").get()
            author_link = author_link.split("'")[1]

            # get topic starter name
            author_name = cols[2].css("span::text").get()

            # get when last message was made
            last_message_date = cols[3].xpath('div')
            last_message_date = last_message_date[0].css("::text").get()

            # write down to the clipboard
            threads_data = threads_data + '; '.join([str(pinned), author_name, author_link, title, url, last_message_date, "\n"])

        # write down to the file
        with open('threads.csv', 'w') as f:
            f.write(threads_data)
