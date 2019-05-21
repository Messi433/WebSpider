# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import scrapy
import redis
from scrapy.http import Request
from urllib import parse

'''创建redis连接'''
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlRunoobSpider(scrapy.Spider):
    name = 'url_runoob'
    allowed_domains = ['http://www.runoob.com/']
    start_urls = ['http://www.runoob.com/']
    key_name = "url_runoob"

    def __init__(self, **kwargs):
        super(UrlRunoobSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlRunoobSpider"

    def parse(self, response):
        unit_divs = response.xpath("//div[contains(@class,'codelist-desktop')]")
        for unit_div in unit_divs:
            course_urls = unit_div.xpath(".//a[contains(@class,'item-top')]/@href")
            for course_url in course_urls:
                course_url = "http:" + course_url.get()
                yield Request(url=parse.urljoin(response.url, course_url), callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        units = response.xpath("//div[@id = 'leftcolumn']//a")
        for unit in units:
            raw_url = unit.xpath("./@href").get()
            url = parse.urljoin(response.url, raw_url)
            r.sadd(self.key_name, url)
