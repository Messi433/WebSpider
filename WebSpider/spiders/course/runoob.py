# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import re

import scrapy
from scrapy.http import Request
import redis

from WebSpider.entities.course.runoob.runoob_item import RunoobItem
from WebSpider.utils.util import get_md5

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class RunoobSpider(scrapy.Spider):
    name = 'runoob'
    allowed_domains = ['http://www.runoob.com/']
    key_name = "url_runoob"
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(RunoobSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "RunoobSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        runoob_item = RunoobItem()
        sub_title = self.process_data(response.xpath("//div[@id = 'content']//h1[1]//text()").getall())
        if sub_title == "":
            sub_title = "菜鸟教程"
        content = self.process_data(response.xpath("//div[@id = 'content']//*//text()").getall())
        url = response.url
        url_object_id = get_md5(url)

        runoob_item['content'] = content
        runoob_item['sub_title'] = sub_title
        runoob_item['url'] = url
        runoob_item['url_object_id'] = url_object_id
        yield runoob_item

    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)
        return data
