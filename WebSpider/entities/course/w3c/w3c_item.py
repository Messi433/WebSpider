import scrapy
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_course
from scripts.es_script.init_course_es import CourseType, get_suggests

# 连接远程服务器上的elasticsearch服务
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


class W3cItem(scrapy.Item):
    sub_title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    def save_es(self):
        w3c = CourseType()
        w3c.sub_title = self['sub_title']
        w3c.content = self["content"]
        w3c.url = self["url"]
        w3c.meta.id = self["url_object_id"]
        '''对数据进行搜索建议的初始化'''
        w3c.suggest = get_suggests(es_course, CourseType,
                                   ((w3c.sub_title, 10), (w3c.content, 4)))
        w3c.save()
