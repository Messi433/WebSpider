'''参阅elasticsearch_DSL官方文档'''
import os

from elasticsearch import Elasticsearch

from scripts.es_script.init_blog_es import BlogType
from elasticsearch_dsl import connections

# 连接远程服务器上的elasticsearch服务
es_server = Elasticsearch(hosts=['114.115.246.224'])

'''返回blog索引信息'''
es_blog = connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20, index=BlogType)
'''返回course索引信息'''
es_course = connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20, index=BlogType)


def break_crawl():
    '''当程序爬取20000行数据时中断爬取'''
    resp = BlogType.search()
    count = resp.count()
    if count >= 20000:
        print('爬够了!!!')
        '''爬够了中断程序'''
        os._exit(0)
