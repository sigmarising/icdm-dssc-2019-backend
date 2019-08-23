import json
import community as c
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


def triple_list_2_echarts_data_json(triple: list, category: int) -> dict:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :param category:
        support two type:
            1: Use Entity Category
            2: Use Communities Detection
    :return: the json dict
    """
    # generate json string
    echarts_json = {
        "nodes": [],
        "edges": [],
        "categories": []
    }

    # we support DiGraph in the beginning
    graph = nx.DiGraph()

    # the category list when use entity type
    entity_types = set()

    # add nodes and edges
    for item in triple:
        entity_x = item["source"]
        entity_x_type = item["sourceType"]
        entity_y = item["target"]
        entity_y_type = item["targetType"]
        relation = item["relation"]

        entity_types.add(entity_x_type)
        entity_types.add(entity_y_type)

        if not graph.has_node(entity_x):
            if category == 1:
                graph.add_node(entity_x, category=entity_x_type)
            elif category == 2:
                graph.add_node(entity_x)
        if not graph.has_node(entity_y):
            if category == 1:
                graph.add_node(entity_y, category=entity_y_type)
            elif category == 2:
                graph.add_node(entity_y)
        if not graph.has_edge(entity_x, entity_y):
            graph.add_edge(entity_x, entity_y, relation=relation)

    # add pageRank and degree to nodes
    page_rank_dict = nx.algorithms.link_analysis.pagerank(graph)
    for k, v in page_rank_dict.items():
        graph.nodes[k]["pageRank"] = v
        graph.nodes[k]["degree"] = graph.degree[k]

    # category of nodes
    if category == 1:
        entity_types = list(entity_types)
        entity_types.sort()
        for entity_type in entity_types:
            echarts_json["categories"].append({
                "name": entity_type
            })
    elif category == 2:
        # communities of nodes
        communities = c.best_partition(nx.Graph(graph))
        for node, community in communities.items():
            graph.nodes[node]["category"] = "community " + str(community + 1)

        # fill in categories
        for index in list(set(communities.values())):
            echarts_json["categories"].append({
                "name": "community " + str(index + 1)
            })

    # fill in nodes info
    for node, attr in graph.nodes.items():
        echarts_json["nodes"].append({
            "name": node,
            "value": attr["degree"],
            "category": attr["category"],
            "symbolSize": attr["pageRank"]
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


def triple_list_2_echarts_data_json_str(triple: list, category: int) -> str:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :param category:
        support two type:
            1: Use Entity Category
            2: Use Communities Detection
    :return: the json str
    """
    json_dict = triple_list_2_echarts_data_json(triple, category)
    return json.dumps(json_dict, ensure_ascii=False)


def text_2_echarts_data_json(text: str, strength: int, category: int) -> dict:
    """
    convert text to echarts data json str
    :param text: input text
    :param strength:
        support three strength:
            1: weak
            2: medium
            3: strong
    :param category:
        support two type:
            1: Use Entity Category
            2: Use Communities Detection
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
    return triple_list_2_echarts_data_json(triple_list, category)


def text_2_echarts_data_json_str(text: str, strength: int, category: int) -> str:
    """
    convert text to echarts data json str
    :param text: input text
    :param strength:
        support three strength:
            1: weak
            2: medium
            3: strong
    :param category:
        support two type:
            1: Use Entity Category
            2: Use Communities Detection
    :return: json str
    """
    return json.dumps(text_2_echarts_data_json(text, strength, category), ensure_ascii=False)
