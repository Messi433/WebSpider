import re
import datetime

import scrapy
from scrapy.http import Request
import redis
from w3lib.html import remove_tags

from WebSpider.entities.blog.oschina.oschina_item import OSChinaItem, OSChinaItemLoader
from WebSpider.utils.util import get_md5

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class OSChinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['https://www.oschina.net/']
    key_name = 'url_oschina'
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(OSChinaSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "OSChinaSpider"

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, dont_filter=True)

    def parse(self, response):
        oschina_item = OSChinaItem()
        oschina_itemloader = OSChinaItemLoader(item=oschina_item, response=response)

        oschina_itemloader.add_value("url", response.url)
        oschina_itemloader.add_value("url_object_id", get_md5(response.url))
        oschina_itemloader.add_xpath("title", "//div[@class = 'article-detail']//h2[@class = 'header']/text()")
        content = self.process_data(response.xpath("//div[@id = 'articleContent']/*[not(@class)]").getall())
        post_date = self.date_produce(response.xpath("//div[contains(@class,'meta-wrap')]/div[1]/text()").getall())

        oschina_item['content'] = content
        oschina_item['post_date'] = post_date
        oschina_itemloader.load_item()
        yield oschina_item

    def process_data(self, data):
        data = remove_tags("".join(data))
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000|&gt;|&nbsp;", "", data)
        return data

    def date_produce(self, data):
        data = "".join(data)
        raw_date = re.search(r'.*?(\d.*\d).*', data).group(1)
        try:
            post_date = datetime.datetime.strptime(raw_date, '%Y/%m/%d %H:%M').date()
        except Exception as e:
            post_date = datetime.datetime.now().date()
        return post_date
