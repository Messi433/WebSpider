import re
import datetime
import time
import json

import scrapy
from scrapy.http import Request
from urllib import parse
import redis

# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlOSChinaSpider(scrapy.Spider):
    name = 'url_oschina'
    allowed_domains = ['https://www.oschina.net/']
    ''' 
        开源中国16个门类的推荐博客
    '''
    key_name = 'url_oschina'
    start_urls = [
        # 前沿技术
        'https://www.oschina.net/blog?classification=5611447'  # 人工智能
        'https://www.oschina.net/blog?classification=5593654'  # 大数据
        'https://www.oschina.net/blog?classification=428639'  # 云计算
        'https://www.oschina.net/blog?classification=5765988'  # 区块链
        # 开发领域
        'https://www.oschina.net/blog?classification=428602',  # 移动开发
        'https://www.oschina.net/blog?classification=428612',  # 前端开发
        'https://www.oschina.net/blog?classification=428640',  # 服务端开发/管理
        'https://www.oschina.net/blog?classification=429511',  # 游戏开发
        'https://www.oschina.net/blog?classification=428609',  # 编程语言
        'https://www.oschina.net/blog?classification=428610',  # 数据库
        'https://www.oschina.net/blog?classification=428611',  # 企业开发
        'https://www.oschina.net/blog?classification=428647',  # 图像/多媒体
        'https://www.oschina.net/blog?classification=428613',  # 系统运维
        'https://www.oschina.net/blog?classification=428638',  # 软件工程
        'https://www.oschina.net/blog?classification=430884',  # 开源硬件
        'https://www.oschina.net/blog?classification=430381',  # 其他类型

    ]

    def __init__(self, **kwargs):
        super(UrlOSChinaSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlOSChinaSpider"

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, dont_filter=True)

    def parse(self, response):
        blog_items = response.xpath("//div[contains(@class,'blog-item')]")

        for blog_item in blog_items:
            url = blog_item.xpath(".//a[@class = 'header']/@href").get()
            if url:
                r.sadd(self.key_name,url)

        next_url = response.xpath("//a[contains(@class,'pagination__next')]/@href").get()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)
