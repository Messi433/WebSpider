# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/25'

import re
from urllib import parse


import scrapy
from scrapy.http import Request
from elasticsearch import Elasticsearch
import redis

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlItCtoSpider(scrapy.Spider):
    name = 'url_itcto'
    allowed_domains = ['http://www.51cto.com/']
    key_name = 'url_itcto'
    '''爬取该网站最新的原创文章的5k条数据和推荐文章5k条数据   更新频率快'''
    start_urls = [
        "http://blog.51cto.com/original",
        "http://blog.51cto.com/artcommend"
    ]

    def __init__(self, **kwargs):
        super(UrlItCtoSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlItCtoSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        lis = response.xpath("//ul[@class='artical-list']//li")
        # 将url存入缓存
        for li in lis:
            url = li.xpath(".//a[@class = 'tit']/@href").get()
            r.sadd(self.key_name, url)

        # 提取下一页url
        next_url = response.xpath("//li[@class = 'next']/a/@href").get()
        if next_url:
            next_url = parse.urljoin(response.url, next_url)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)
