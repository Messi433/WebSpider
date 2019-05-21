# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/25'

import re

import scrapy
from scrapy.http import Request
import redis

from WebSpider.utils.util import get_md5
from WebSpider.entities.blog.itcto.itcto_item import ItCtoItem, ItCtoItemLoader

r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class ItCtoSpider(scrapy.Spider):
    name = 'itcto'
    allowed_domains = ['http://blog.51cto.com/original']
    key_name = 'url_itcto'
    '''爬取该网站最新的原创文章的5k条数据和推荐文章5k条数据   更新频率快'''
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(ItCtoSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "ItCtoSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        itcto_item = ItCtoItem()
        itcto_loader = ItCtoItemLoader(item=itcto_item, response=response)

        itcto_loader.add_css("title", "h1.artical-title::text")
        itcto_loader.add_css("post_date", "div.artical-title-list a.time::text")
        # 阅读人数
        # itcto_loader.add_css("read_count", "div.artical-title-list a.read::text")
        itcto_loader.add_value("url", response.url)
        itcto_loader.add_value("url_object_id", get_md5(response.url))
        content = self.process_data(response.xpath("//div[contains(@class,'artical-content')]//text()").getall())

        itcto_item["content"] = content
        itcto_item = itcto_loader.load_item()

        yield itcto_item

    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)
        return data
