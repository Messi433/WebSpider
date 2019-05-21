# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/25'

import re

import scrapy
from scrapy.http import Request
import redis

from WebSpider.utils.util import get_md5
from WebSpider.entities.blog.itpub.itpub_item import ItPubItem, ItPubItemLoader

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class ItPubSpider(scrapy.Spider):
    name = 'itpub'
    allowed_domains = ['http://blog.itpub.net/']
    key_name = 'url_itpub'
    '''大型网站数据量在10W+'''
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(ItPubSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "ItPubSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        itpub_item = ItPubItem()
        itpub_loader = ItPubItemLoader(item=itpub_item, response=response)

        itpub_loader.add_css("title", "h1.preview-title::text")
        itpub_loader.add_xpath("post_date", "//div[@class = 'mess']/span[3]//text()")
        itpub_loader.add_value("url", response.url)
        itpub_loader.add_value("url_object_id", get_md5(response.url))
        content = self.process_data(response.xpath("//div[@class = 'preview-main']//text()").getall())

        itpub_item["content"] = content
        itpub_item = itpub_loader.load_item()

        yield itpub_item

    def parse_detail(self, response):
        pass

    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)
        return data
