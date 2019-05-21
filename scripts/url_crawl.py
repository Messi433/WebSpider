# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/17'

import sys
import os

from scrapy.cmdline import execute
'''爬虫非cmd测试脚本'''
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
# url blog
execute(['scrapy', 'crawl', 'url_bole'])
# execute(['scrapy', 'crawl', 'url_itpub'])
# execute(['scrapy', 'crawl', 'url_itcto'])
# execute(['scrapy', 'crawl', 'url_oschina'])
# url course
# execute(['scrapy', 'crawl', 'url_runoob'])
# execute(['scrapy', 'crawl', 'url_course_bai'])
# execute(['scrapy', 'crawl', 'url_lxf'])
# execute(['scrapy', 'crawl', 'url_w3c'])
