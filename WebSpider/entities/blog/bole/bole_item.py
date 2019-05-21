import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_blog
from scripts.es_script.init_blog_es import BlogType, get_suggests

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


# 日期处理函数
def date_produce(value):
    try:
        post_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        post_date = datetime.datetime.now().date()
    return post_date


class BoleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BoleItem(scrapy.Item):
    title = scrapy.Field()
    post_date = scrapy.Field(
        input_processor=MapCompose(date_produce),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    content = scrapy.Field()

    # 保存数据到es
    def save_es(self):
        bole = BlogType()

        bole.title = self['title']
        bole.post_date = self["post_date"]
        bole.content = remove_tags(self["content"])
        bole.url = self["url"]
        bole.meta.id = self["url_object_id"]

        '''对数据进行搜索建议的初始化'''
        bole.suggest = get_suggests(es_blog, BlogType, ((bole.title, 10), (bole.content, 4)))
        bole.save()  # 保存数据
