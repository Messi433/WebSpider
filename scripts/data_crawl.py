# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/17'

import sys
import os

from scrapy.cmdline import execute
'''爬虫非cmd测试脚本'''
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
# blog
execute(['scrapy', 'crawl', 'bole'])
# execute(['scrapy', 'crawl', 'oschina'])
# execute(['scrapy','crawl','cnblog'])
# execute(['scrapy','crawl','itpub'])
# execute(['scrapy','crawl','itcto'])
# # course
# execute(['scrapy','crawl','runoob'])
# execute(['scrapy','crawl','course_bai'])
# execute(['scrapy','crawl','lxf'])
# execute(['scrapy','crawl','w3c'])
