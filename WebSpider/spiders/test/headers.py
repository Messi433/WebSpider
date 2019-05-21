# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/11/7'

import re
import json

import scrapy


class HeadersSpider(scrapy.Spider):
    name = 'headers'
    allowed_domains = ['http://httpbin.org']
    start_urls = ['http://httpbin.org/user-agent', 'http://httpbin.org/ip']

    def parse(self, response):
        http_code = response.status
        url_suffix = self.match_suffix(response.url)
        if url_suffix == '/ip':
            ip = json.loads(response.text)['origin']
            print(ip)
        elif url_suffix == '/user-agent':
            user_agent = json.loads(response.text)['user-agent']
            print(user_agent)

    def match_suffix(self, str):
        str1 = re.match(r'.*(/.*)', str).group(1)
        return str1
