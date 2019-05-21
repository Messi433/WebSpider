import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from elasticsearch_dsl import connections

from scripts.es_script.init_blog_es import BlogType, get_suggests
from WebSpider.utils.es_util import es_blog

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


# 时间处理
def date_produce(post_date):
    try:
        post_date = datetime.datetime.strptime(post_date, "%Y-%m-%d %H:%M").date()  # 格式化的时间str转化为date
    except Exception as e:
        post_date = datetime.datetime.now().date()  # 时间出现异常则转化为当前(爬取)时间
    return post_date


class CnblogItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class CnblogItem(scrapy.Item):
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

    def save_es(self):
        cnblog = BlogType()
        cnblog.title = self['title']
        cnblog.post_date = self["post_date"]
        cnblog.content = self["content"]
        cnblog.url = self["url"]
        cnblog.meta.id = self["url_object_id"]
        '''对数据进行搜索建议的初始化'''
        cnblog.suggest = get_suggests(es_blog, BlogType,
                                      ((cnblog.title, 10), (cnblog.content, 4)))
        cnblog.save()  # 保存数据
