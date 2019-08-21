import json
from django.db import transaction
from . import models
from algorithm.graph import *


def service_article_list():
    """
    look in the db and get the articles' category and identity
    :return:
    """
    with transaction.atomic():
        all_article = models.Article.objects.all().values('category', 'identity').order_by('category')
    res = {}
    for article in all_article:
        if article["category"] in res.keys():
            res[article["category"]].append(article["identity"])
        else:
            res[article["category"]] = [article["identity"]]
    for v in res.values():
        v.sort()
    return res


def service_article_info(category, identity):
    """
    find the article info in db
    :param category: category
    :param identity: category
    :return: content and graph
    """
    with transaction.atomic():
        info = models.Article.objects.filter(category=category, identity=identity).values('content', 'graph')
    res = {
        "content": "",
        "graph": ""
    }
    if info.exists():
        res["content"] = info[0]["content"]
        res["graph"] = json.loads(info[0]["graph"].strip(), encoding='utf-8')
    return res


def service_knowledge_graph(text):
    """
    service for convert text to knowledge graph (in json dict)
    :param text: input text
    :return: json dict
    """
    print(text_2_echarts_data_json_str(text))
    return text_2_echarts_data_json(text)
