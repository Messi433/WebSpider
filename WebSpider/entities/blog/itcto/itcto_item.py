# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/25'

import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_blog
from scripts.es_script.init_blog_es import BlogType, get_suggests

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


# 时间处理
def date_produce(post_date):
    post_date = re.match(r".*?(\d.*\d).*", post_date)
    try:
        post_date = datetime.datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S").date()  # 格式化的时间str转化为date
    except Exception as e:
        post_date = datetime.datetime.now().date()  # 时间出现异常则转化为当前(爬取)时间
    return post_date


def returnValue(value):
    return value


class ItCtoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ItCtoItem(scrapy.Item):
    title = scrapy.Field()
    post_date = scrapy.Field(
        input_processor=MapCompose(date_produce),
        output_processor=TakeFirst()
    )
    content = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_object_id = scrapy.Field()

    # 保存数据到es
    def save_es(self):
        itcto = BlogType()
        itcto.title = self['title']
        itcto.post_date = self["post_date"]
        itcto.content = remove_tags(self["content"])
        itcto.url = self["url"]
        itcto.meta.id = self["url_object_id"]

        '''对数据进行搜索建议的初始化'''
        itcto.suggest = get_suggests(es_blog, BlogType, ((itcto.title, 10), (itcto.content, 4)))
        itcto.save()  # 保存数据
