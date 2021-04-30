import scrapy
import w3lib.html as w3
import json


class TopicSpider(scrapy.Spider):
    """ Parse each topic to get info about item for sell
        input: start urls
        input type: str
        input: forum url
        input type: str
    """

    #spider variables
    name = "topic_spider"

    # Parsing variables
    def __init__(self):
        self.forum = "http://fishing.kiev.ua/vb3/"


    def start_requests(self):
        """ loads threads urls from json file and scrap """

        with open('threads.json', 'r') as f:
            threads = f.read()

        threads = json.loads(threads)
        urls = [self.forum + item['Url'] for item in threads]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        """ recursively parse each topic in the list of threads """

        #get pagination
        next_page = response.css('a')
        for item in next_page:
            if 'next' in item.attrib.values():
                next_page = self.forum + item.attrib['href']
                break

        # Get divs with id has 'post_message'
        posts_list = []
        for item in response.css('div'):
            if 'id' in item.attrib.keys():
                if 'post_message' in item.attrib['id']:
                    posts_list.append(item)

        # clear html tags and controls from post messages
        posts_list = [w3.remove_tags(x.get()) for x in posts_list]

        # Save post collection
        posts = {f'post_{i}': posts_list[i] for i in range(len(posts_list))}

        # Look for attachments and get them
        links = response.css('a')
        attachments = set()

        for item in links:
            for value in item.attrib.values():
                if 'attachment' in value:
                    attachments.add(value)

        # add attachments to the posts
        posts.update({'attach': attachments})

        yield posts
