# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/10/31'

'''参阅elasticsearch_DSL官方文档'''
from elasticsearch_dsl import Document, Completion, Keyword, Text
from elasticsearch_dsl import connections
from elasticsearch_dsl.analysis import CustomAnalyzer

# 连接远程服务器上的elasticsearch服务
connections.create_connection(hosts=['114.115.246.224:9200'], timeout=20)


# 重写CustomAnalyzer否则报错
class CustomAnalyzer(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


# ik分词器
ik_analyzer = CustomAnalyzer("ik_smart", filter=["lowercase"])


# 初始化搜索建议
def get_suggests(es_con, index, info_tuple):
    es = es_con
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            words = es.indices.analyze(index="course_index",
                                       body={"analyzer": "ik_max_word", "text": "{0}".format(text)})
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests


# 初始化索引
class CourseType(Document):
    suggest = Completion(analyzer=ik_analyzer)

    sub_title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'course_index'
        settings = {
            "number_of_shards": 5,
            "number_of_replicas": 1
        }


if __name__ == "__main__":
    CourseType.init()
    print('Initialize the course_index successfully')
