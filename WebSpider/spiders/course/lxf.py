# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import scrapy
from scrapy.http import Request
import redis
from w3lib.html import remove_tags

from WebSpider.entities.course.runoob.runoob_item import RunoobItem
from WebSpider.utils.util import get_md5

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class LxfSpider(scrapy.Spider):
    name = 'lxf'
    allowed_domains = ['https://www.liaoxuefeng.com/']
    key_name = "url_lxf"
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(LxfSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "LxfSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        response.xpath("//div[@class = 'x-content']/h4[1]/text()")
