import json
import community as c
import networkx as nx
from .func import text_2_triple_list


# def text_2_triple_list(text: str) -> list:
#     """
#     input the text and return the knowledge graph triple (in list)
#     :param text: A Text String
#     :return:
#         the Triple list of Knowledge Graph
#         one possible example:
#         [
#             {
#                 "source": "car",
#                 "target": "store",
#                 "relation": "at"
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
        "categories": []
    }

    # we support DiGraph in the beginning
    graph = nx.DiGraph()

    # add nodes and edges
    for item in triple:
        entity_x = item["source"]
        entity_y = item["target"]
        relation = item["relation"]

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

    # communities of nodes
    communities = c.best_partition(nx.Graph(graph))
    for node, community in communities.items():
        graph.nodes[node]["category"] = "category" + str(community + 1)

    # fill in categories
    for index in list(set(communities.values())):
        echarts_json["categories"].append({
            "name": "category" + str(index + 1)
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


def triple_list_2_echarts_data_json_str(triple: list) -> str:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :return: the json str
    """
    json_dict = triple_list_2_echarts_data_json(triple)
    return json.dumps(json_dict, ensure_ascii=False)


def text_2_echarts_data_json(text: str) -> dict:
    """
    convert text to echarts data json str
    :param text: input text
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
    triple_list = text_2_triple_list(text)
    return triple_list_2_echarts_data_json(triple_list)


def text_2_echarts_data_json_str(text: str) -> str:
    """
    convert text to echarts data json str
    :param text: input text
    :return: json str
    """
    return json.dumps(text_2_echarts_data_json(text), ensure_ascii=False)
