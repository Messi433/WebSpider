# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/11/7'

import re
import json

import scrapy
from scrapy.http import Request


class IpProxySpider(scrapy.Spider):
    name = 'ip_proxy'
    allowed_domains = ['https://www.xicidaili.com/']
    # 西刺高匿免费ip代理
    start_urls = ['https://www.xicidaili.com/nn/']

    def parse(self, response):
        pass
