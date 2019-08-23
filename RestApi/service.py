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


def service_article_info(category, identity, strength, category_methond):
    """
    find the article info in db
    :param category: industry
    :param identity: id
    :param strength:
        convert str config to int:
            Weak: 1
            Medium: 2
            Strong: 3
    :param category_methond:
        convert str config to int
            Entity Category: 1
            Communities Detection: 2
    :return: content and graph
    """
    lookup_str = 'graph' + strength
    if category_methond == 'Entity Category':
        lookup_str += 'Et'
    elif category_methond == 'Communities Detection':
        lookup_str += 'Cd'

    with transaction.atomic():
        info = models.Article.objects.filter(category=category, identity=identity).values('content', lookup_str)
    res = {
        "content": "",
        "graph": ""
    }
    if info.exists():
        res["content"] = info[0]["content"]
        res["graph"] = json.loads(info[0][lookup_str].strip(), encoding='utf-8')
    return res


def service_knowledge_graph(text, strength, category_methond):
    """
    service for convert text to knowledge graph (in json dict)
    :param text: input text
    :param strength:
        convert str config to int:
            Weak: 1
            Medium: 2
            Strong: 3
    :param category_methond:
        convert str config to int
            Entity Category: 1
            Communities Detection: 2
    :return: json dict
    """
    param_strength, param_category = 0, 0
    if strength == "Weak":
        param_strength = 1
    elif strength == "Medium":
        param_strength = 2
    elif strength == 'Strong':
        param_strength = 3

    if category_methond == "Entity Category":
        param_category = 1
    elif category_methond == "Communities Detection":
        param_category = 2

    return text_2_echarts_data_json(text, param_strength, param_category)
