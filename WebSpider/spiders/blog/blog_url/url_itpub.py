# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/25'

import re

import scrapy
from scrapy.http import Request
from urllib import parse
import redis
from elasticsearch import Elasticsearch



# 连接远程服务器上的redis服务
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlItPubSpider(scrapy.Spider):
    name = 'url_itpub'
    allowed_domains = ['http://blog.itpub.net/']
    key_name = 'url_itpub'
    '''大型网站数据量在10W+'''
    # 爬取门类:数据库、大数据、应用开发、linux、数字化转型、人工智能、区块链、架构设计、自动化运维、移动开发、云计算、it基础架构
    start_urls = [
        'http://blog.itpub.net/appdevelop/',
        'http://blog.itpub.net/database/',
        'http://blog.itpub.net/linux/',
        'http://blog.itpub.net/bigdata/',
        'http://blog.itpub.net/digitaltransfor/',
        'http://blog.itpub.net/ai/',
        'http://blog.itpub.net/blockchain/',
        'http://blog.itpub.net/structruing/',
        'http://blog.itpub.net/autooperation/',
        'http://blog.itpub.net/mobiledev/',
        'http://blog.itpub.net/embedded/',
        'http://blog.itpub.net/cloudcomputing/',
        'http://blog.itpub.net/itinfar/'
    ]

    def __init__(self, **kwargs):
        super(UrlItPubSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlItPubSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        items = response.xpath("//ul[@id='list']//li[@class='list-item']")
        if items:
            # 将url存入缓存中
            for item in items:
                url = item.xpath("./a/@href").get()
                if url:
                    r.sadd(self.key_name, url)
        else:
            print(response.url)
            print("当前页面需要解析的url为空")
            # 解析页面为空,则退出当前解析,解析其他的start_urls
            return self.start_requests

        # 提取下一页url
        next_url = response.xpath("//div[@class='load-more']/a/@href").get()
        if next_url:
            # 下一页页码
            next_number = self.match_number(next_url)
            if next_number > 500:
                print("当前分类爬够了500页,继续爬取其他的start_urls")
                return self.start_requests
            else:
                next_url = parse.urljoin(response.url, next_url)
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def match_number(self, str):
        number = int(re.match(r'.*?(\d.*).*', str).group(1))
        return number
