# -*- coding: utf-8 -*-
__author__ = 'caoke'
__date__ = '2018/10/25'

import scrapy
from scrapy.http import Request
from urllib import parse
import redis

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlBoleSpider(scrapy.Spider):
    name = 'url_bole'
    allowed_domains = ['http://www.jobbole.com/']
    '''爬取最新文章5000条'''
    start_urls = ['http://blog.jobbole.com/all-posts/']
    key_name = 'url_bole'

    def __init__(self, **kwargs):
        super(UrlBoleSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlBoleSpider"

    def parse(self, response):

        post_items = response.css("#archive .floated-thumb .post-thumb a")
        # 将url存入redis缓存中
        for post_item in post_items:
            url = post_item.css("::attr(href)").extract_first("")
            r.sadd(self.key_name, url)

        # 提取下一页
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)
