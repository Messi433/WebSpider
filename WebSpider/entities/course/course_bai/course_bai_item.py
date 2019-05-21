import scrapy
from elasticsearch_dsl import connections

from WebSpider.utils.es_util import es_course
from scripts.es_script.init_course_es import CourseType, get_suggests

'''连接远程服务器上的elasticsearch服务'''
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


class CourseBaiItem(scrapy.Item):
    sub_title = scrapy.Field()  # 教程单元
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    def save_es(self):
        course_bai = CourseType()
        course_bai.sub_title = self['sub_title']
        course_bai.content = self["content"]
        course_bai.url = self["url"]
        course_bai.meta.id = self["url_object_id"]
        '''对数据进行搜索建议的初始化'''
        course_bai.suggest = get_suggests(es_course, CourseType,
                                          ((course_bai.sub_title, 10), (course_bai.content, 4)))
        course_bai.save()
