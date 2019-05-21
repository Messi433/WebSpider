import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_blog
from scripts.es_script.init_blog_es import BlogType, get_suggests

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


def title_produce(str):
    title = re.sub(r'\s|\n', '', str)
    return title


def returnValue(value):
    return value


class OSChinaItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class OSChinaItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(title_produce),
        output_processor=TakeFirst()
    )
    post_date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_object_id = scrapy.Field()

    def save_es(self):
        oschina = BlogType()
        oschina.title = self['title']
        oschina.post_date = self["post_date"]
        oschina.content = self["content"]
        oschina.url = self["url"]
        # oschina.read_count = self["read_count"]
        oschina.meta.id = self["url_object_id"]
        '''对数据进行搜索建议的初始化'''
        oschina.suggest = get_suggests(es_blog, BlogType, ((oschina.title, 10), (oschina.content, 4)))
        oschina.save()  # 保存数据
