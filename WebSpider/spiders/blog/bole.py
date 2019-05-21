# -*- coding: utf-8 -*-
__author__ = 'caoke'
__date__ = '2018/10/25'

import scrapy
from scrapy.http import Request
import redis

from WebSpider.entities.blog.bole.bole_item import BoleItem, BoleItemLoader
from WebSpider.utils.util import get_md5

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class BoleSpider(scrapy.Spider):
    name = 'bole'
    allowed_domains = ['http://www.jobbole.com/']
    key_name = 'url_bole'
    # start_urls = ['http://blog.jobbole.com/all-posts/']
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(BoleSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "BoleSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        bole_item = BoleItem()

        '''itemloader方式抽取'''
        item_loader = BoleItemLoader(item=bole_item, response=response)

        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("post_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("content", "div.entry")

        bole_item = item_loader.load_item()

        yield bole_item

    def parse_detail(self, response):
        pass
