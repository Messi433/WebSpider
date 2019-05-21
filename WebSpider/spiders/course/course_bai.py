# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import re

import scrapy
from scrapy.http import Request
import redis

from WebSpider.utils.util import get_md5
from WebSpider.entities.course.course_bai.course_bai_item import CourseBaiItem

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class CourseBaiSpider(scrapy.Spider):
    name = 'course_bai'
    allowed_domains = ['https://www.yiibai.com/']
    key_name = "url_course_bai"
    start_urls = list(r.smembers(key_name))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        course_bai_item = CourseBaiItem()

        sub_title = self.process_data(response.xpath("//div[@id = 'navs']//h1[@class = 'article-title']//text()").get())
        content = self.process_data(response.xpath("//div[@class = 'article-content']/*[not(@style)]//text()").getall())
        url = response.url
        url_object_id = get_md5(url)

        course_bai_item['sub_title'] = sub_title
        course_bai_item['content'] = content
        course_bai_item['url'] = url
        course_bai_item['url_object_id'] = url_object_id

        yield course_bai_item

    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)

        return data
