import datetime
import scrapy
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_course
from scripts.es_script.init_course_es import CourseType, get_suggests

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


def date_produce(value):
    try:
        post_date = datetime.datetime.strptime(value, '%Y年%m月%d日 %H:%M:%S').date()
    except Exception as e:
        post_date = datetime.datetime.now().date()
    return post_date


class RunoobItem(scrapy.Item):
    sub_title = scrapy.Field()  # 教程单元
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    def save_es(self):
        runoob = CourseType()
        runoob.sub_title = self['sub_title']
        runoob.content = self["content"]
        runoob.url = self["url"]
        runoob.meta.id = self["url_object_id"]
        '''对数据进行搜索建议的初始化'''
        runoob.suggest = get_suggests(es_course, CourseType,
                                      ((runoob.sub_title, 10), (runoob.content, 4)))
        runoob.save()
