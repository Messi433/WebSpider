# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import scrapy
from urllib import parse
from scrapy.http import Request
import redis

'''创建redis连接'''
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlCourseBaiSpider(scrapy.Spider):
    name = 'url_course_bai'
    allowed_domains = ['https://www.yiibai.com/']
    start_urls = ['https://www.yiibai.com/']
    # 缓存中redis key_name
    key_name = "url_course_bai"

    def __init__(self, **kwargs):
        super(UrlCourseBaiSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlCourseBaiSpider"

    # 抽取大类
    def parse(self, response):
        lis = response.xpath("//ul[@class = 'pagemenu']//li[not(@class)]")
        for li in lis:
            class_url = li.xpath("./a/@href").get()
            yield Request(url=parse.urljoin(response.url, class_url)
                          , callback=self.parse_class, dont_filter=True)

    # 抽取课程
    def parse_class(self, response):
        lis = response.xpath("//ul[@class = 'pagemenu']//li[not(@class)]")
        for li in lis:
            course_url = li.xpath("./a/@href").get()
            yield Request(url=parse.urljoin(response.url, course_url), callback=self.parse_unit, dont_filter=True)

    # 抽取单元 每个单元的url作为数据解析的入口
    def parse_unit(self, response):
        lis = response.xpath("//ul[@class = 'pagemenu']//li[not(@class)]")

        for li in lis:
            sub_url = li.xpath("./a/@href").get()
            url = parse.urljoin(response.url, sub_url)
            # 将url添加到redis缓存
            r.sadd(self.key_name, url)
