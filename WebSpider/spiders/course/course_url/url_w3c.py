# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/6'

import re

import scrapy
import redis
from scrapy.http import Request
from urllib import parse

'''创建redis连接'''
r = redis.StrictRedis(host="114.115.246.224", password="k753951", decode_responses=True)


class UrlW3cSpider(scrapy.Spider):
    name = 'url_w3c'
    allowed_domains = ['https://www.w3cschool.cn/']
    key_name = "url_w3c"
    start_urls = [
        'https://www.w3cschool.cn/manual/index/webqdkf',  # WEB前端开发
        'https://www.w3cschool.cn/manual/index/fwqdkf',  # 服务器端开发
        'https://www.w3cschool.cn/manual/index/sjkkf',  # 数据库开发
        'https://www.w3cschool.cn/manual/index/yddkf',  # 移动端开发
        'https://www.w3cschool.cn/manual/index/dsjkf',  # 大数据开发
        'https://www.w3cschool.cn/manual/index/fwqkf',  # 服务器运维
        'https://www.w3cschool.cn/manual/index/kfgjjc',  # 开发工具
        'https://www.w3cschool.cn/manual/index/kfkjjc',  # 开发框架
        'https://www.w3cschool.cn/manual/index/cybgrj',  # 常用办公软件
    ]

    def __init__(self, **kwargs):
        super(UrlW3cSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "UrlW3cSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath(
            "//ul[@class = 'manual-ul']//li[contains(@class , 'manual-item2')]/div[@class = 'manual-intro']/h4/a/@href").getall()
        for url in urls:
            url = parse.urljoin(response.url, url)
            r.sadd(self.key_name, url)

        next_url = response.xpath("//div[@class = 'pagination']/a[last()]/@href").get()
        if next_url:
            # 当前请求页页码
            current_page_number = self.process_page_number(response.url)
            # 下一页页码
            next_page_number = self.process_page_number(next_url)
            # 如果是最后一页
            if current_page_number > next_page_number:
                print("已解析到最后一页")
                return self.start_requests
            else:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def parse_course(self, response):
        pass

    def process_page_number(self, str):
        # 当初次请求url时,不显示页码,会导致正则匹配出现异常,捕获并处理该异常
        try:
            page_number = int(re.search(r'page=?(\d*)', str).group(1))
        except Exception as e:
            page_number = 1
        return page_number
