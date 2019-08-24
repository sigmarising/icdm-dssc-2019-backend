import json
import community as nx_c
import networkx as nx
from .func import text_2_triple_list


# def text_2_triple_list(text: str, strength: int) -> list:
#     """
#     input the text and return the knowledge graph triple (in list)
#     :param text:
#         A Text String to Analysis with UTF-8 charset
#     :param strength:
#         support three strength:
#             1: weak
#             2: medium
#             3: strong
#     :return:
#         the Triple list of Knowledge Graph
#         (with two additional entity type, none should be 'default')
#         one possible example:
#         [
#             {
#                 "source": "car",
#                 "sourceType": "default",
#                 "target": "store",
#                 "targetType": "name"
#                 "relation": "at",
#             },
#         ]
#     """
#     pass


def triple_list_2_echarts_data_json(triple: list) -> dict:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :return: the json dict
    """
    # generate json string
    echarts_json = {
        "nodes": [],
        "edges": [],
        "classification": {
            "entityCategory": {},
            "communitiesDetection": {}
        },
        "categories": {
            "entityCategory": [],
            "communitiesDetection": []
        }
    }

    # we support DiGraph in the beginning
    graph = nx.DiGraph()

    # the category list for two condition
    categories_entity = set()
    categories_community = set()

    # add nodes and edges
    for item in triple:
        entity_x = item["source"]
        entity_y = item["target"]
        relation = item["relation"]

        entity_x_type = item["sourceType"]
        entity_y_type = item["targetType"]

        categories_entity.add(entity_x_type)
        categories_entity.add(entity_y_type)

        echarts_json["classification"]["entityCategory"][entity_x] = entity_x_type
        echarts_json["classification"]["entityCategory"][entity_y] = entity_y_type

        if not graph.has_node(entity_x):
            graph.add_node(entity_x)
        if not graph.has_node(entity_y):
            graph.add_node(entity_y)
        if not graph.has_edge(entity_x, entity_y):
            graph.add_edge(entity_x, entity_y, relation=relation)

    # add pageRank and degree to nodes
    page_rank_dict = nx.algorithms.link_analysis.pagerank(graph)
    for k, v in page_rank_dict.items():
        graph.nodes[k]["pageRank"] = v
        graph.nodes[k]["degree"] = graph.degree[k]

    # community detection
    communities = nx_c.best_partition(nx.Graph(graph))
    for node, community in communities.items():
        label = "community " + str(community + 1)
        echarts_json["classification"]["communitiesDetection"][node] = label
        categories_community.add(label)

    # set category in echarts json
    categories_entity = list(categories_entity)
    categories_entity.sort()
    categories_community = list(categories_community)
    categories_community.sort()
    for entity in categories_entity:
        echarts_json["categories"]["entityCategory"].append({
            "name": entity
        })
    for entity in categories_community:
        echarts_json["categories"]["communitiesDetection"].append({
            "name": entity
        })

    # fill in nodes info
    for node, attr in graph.nodes.items():
        echarts_json["nodes"].append({
            "name": node,
            "value": attr["degree"],
            "symbolSize": attr["pageRank"],
            "category": ""
        })

    # fill in edges info
    for edge, attr in graph.edges.items():
        echarts_json["edges"].append({
            "source": edge[0],
            "target": edge[1],
            "label": {
                "formatter": attr["relation"]
            }
        })
    return echarts_json


def triple_list_2_echarts_data_json_str(triple: list) -> str:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :return: the json str
    """
    json_dict = triple_list_2_echarts_data_json(triple)
    return json.dumps(json_dict, ensure_ascii=False)


def text_2_echarts_data_json(text: str, strength: int) -> dict:
    """
    convert text to echarts data json str
    :param text: input text
    :param strength:
        support three strength:
            1: weak
            2: medium
            3: strong
    :return: json dict
    """
    triple_list = [
        {
            "source": "a",
            "target": "b",
            "relation": "at"
        },
        {
            "source": "b",
            "target": "c",
            "relation": "at"
        },
        {
            "source": "b",
            "target": "d",
            "relation": "at"
        },
        {
            "source": "b",
            "target": "e",
            "relation": "at"
        },
        {
            "source": "e",
            "target": "f",
            "relation": "at"
        },
        {
            "source": "f",
            "target": "h",
            "relation": "at"
        },
        {
            "source": "f",
            "target": "g",
            "relation": "at"
        },
        {
            "source": "f",
            "target": "k",
            "relation": "at"
        }
    ]
    triple_list = text_2_triple_list(text, strength)
    return triple_list_2_echarts_data_json(triple_list)


def text_2_echarts_data_json_str(text: str, strength: int) -> str:
    """
    convert text to echarts data json str
    :param text: input text
    :param strength:
        support three strength:
            1: weak
            2: medium
            3: strong
    :return: json str
    """
    return json.dumps(text_2_echarts_data_json(text, strength), ensure_ascii=False)
