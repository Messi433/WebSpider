# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/31'

from elasticsearch_dsl import connections,Index

# 建立连接
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)
# 获得索引
index = Index(name="blog_index",doc_type="doc")

if __name__ == "__main__":
    # 删除索引
    index.delete()
    print('Delete the blog_index successfully')