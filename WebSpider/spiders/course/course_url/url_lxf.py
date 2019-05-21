# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import scrapy
import redis
from scrapy.http import Request
from urllib import parse

'''创建redis连接'''
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlLxfSpider(scrapy.Spider):
    name = 'url_lxf'
    allowed_domains = ['https://www.liaoxuefeng.com/']
    key_name = "url_lxf"
    # 小型编程教程网站
    start_urls = [
        'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000',  # python教程
        'https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000',  # JavaScript教程
        'https://www.liaoxuefeng.com/wiki/001508284671805d39d23243d884b8b99f440bfae87b0f4000',  # SQL教程
        'https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000',  # Git教程
    ]

    def __init__(self, **kwargs):  # 初始化redis队列
        super(UrlLxfSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlLxfSpider"

    def parse(self, response):
        unit_urls = response.xpath("//ul[@id = 'x-wiki-index']//a[@class = 'x-wiki-index-item']/@href").getall()
        for url in unit_urls:
            url = parse.urljoin(response.url, url)
            r.sadd(self.key_name, url)
