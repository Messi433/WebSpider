# -*- coding: utf-8 -*-
__author__ = 'caoke'
__date__ = '2018/10/25'

import os
import re
from urllib import parse

import scrapy
from scrapy.http import Request
from elasticsearch import Elasticsearch

from WebSpider.utils.util import get_md5
from WebSpider.entities.blog.cnblog.cnblog_item import CnblogItem, CnblogItemLoader
from WebSpider.utils.es_util import break_crawl


class CnblogSpider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['https://www.cnblogs.com']
    '''直接爬取不做url与数据分离爬取'''
    # 爬取门类:
    start_urls = [
        'https://www.cnblogs.com/cate/2/',
        'https://www.cnblogs.com/cate/108703/',
        'https://www.cnblogs.com/cate/108712/',
        'https://www.cnblogs.com/cate/108724/',

    ]

    def __init__(self, **kwargs):
        super(CnblogSpider, self).__init__(self, **kwargs)

    def __str__(self):
        return "CnblogSpider"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('当前页码' + response.url)
        post_nodes = response.xpath("//div[@class = 'post_item']//div[@class = 'post_item_body']/h3//a")
        # 解析当前页码文章
        for node in post_nodes:
            # 解析每篇文章的url
            url = node.xpath("./@href").get()
            # 解析每篇文章的标题
            title = node.xpath('.//text()').get()
            yield Request(url=url, callback=self.parse_detail, meta={"title": title}, dont_filter=True)
        # 获取下一页页码的url
        next_url = response.xpath("//div[@class = 'pager']//a[last()]/@href").get()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        # 当程序爬取20000行数据时中断爬取
        # break_crawl()

        cnblog_item = CnblogItem()
        cnblog_loader = CnblogItemLoader(item=cnblog_item, response=response)
        # 从meta中获取上一级的文章标题
        title = response.meta.get("title")
        # 解析文章内容
        content = self.process_data(response.xpath("//div[@id = 'cnblogs_post_body']//*//text()").getall())
        cnblog_loader.add_xpath("post_date", "//span[@id = 'post-date']//text()")
        cnblog_loader.add_value("url", response.url)
        cnblog_loader.add_value("url_object_id", get_md5(response.url))

        cnblog_item['title'] = title
        cnblog_item['content'] = content
        cnblog_item = cnblog_loader.load_item()
        yield cnblog_item

    # 内容处理
    def process_data(self, data):
        data = "".join(data)
        data = re.sub(r"\s|\u3000|\xa0|\n|\r|n0000", "", data)
        return data
