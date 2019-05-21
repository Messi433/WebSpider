# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import re

import scrapy
from scrapy.http import Request
import redis
from urllib import parse

from WebSpider.entities.course.w3c.w3c_item import W3cItem
from WebSpider.utils.util import get_md5

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class W3cSpider(scrapy.Spider):
    name = 'w3c'
    allowed_domains = ['https://www.w3cschool.cn/']
    key_name = "url_w3c"
    start_urls = list(r.smembers(key_name))

    def __init__(self, **kwargs):
        super(W3cSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "W3cSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        items = response.xpath("//div[@id = 'nestable_handbook']//li[@class = 'dd-item']"
                               "/ol[@class = 'dd-list']//li[@class = 'dd-item']/div[contains(@class,'dd-content')]")
        for item in items:
            sub_title = item.xpath("./a/text()").get()
            sub_url = item.xpath("./a/@href").get()
            yield Request(url=parse.urljoin(response.url, sub_url), callback=self.parse_detail,
                          meta={"sub_title": sub_title}, dont_filter=True)

    def parse_detail(self, response):
        w3c_item = W3cItem()

        sub_title = response.meta.get("sub_title")
        url = response.url
        content = self.process_data(response.xpath("//div[@class = 'content-bg']//text()").getall())
        url_object_id = get_md5(url)

        w3c_item['content'] = content
        w3c_item['sub_title'] = sub_title
        w3c_item['url'] = url
        w3c_item['url_object_id'] = url_object_id
        yield w3c_item

    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)
        return data
