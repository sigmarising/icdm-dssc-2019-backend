import json
import math
import itertools
import networkx as nx


def text_2_triple_list(text: str) -> list:
    """
    input the text and return the knowledge graph triple (in list)
    :param text: A Text String
    :return:
        the Triple list of Knowledge Graph
        one possible example:
        [
            {
                "source": "car",
                "target": "store",
                "relation": "at"
            },
        ]
    """
    pass


def triple_list_2_echarts_data_json_str(triple: list) -> str:
    """
    input the triple list and convert it to echarts data json str (using networkX)
    :param triple: the triple list
    :return: the json string
    """
    graph = nx.Graph()

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
    k = math.floor(math.log2(len(graph.nodes))) + 1  # the triple has at least 2 node, so k >= 2
    comp = nx.algorithms.community.girvan_newman(graph)
    limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    communities = None
    for communities_iter in limited:
        communities = tuple(sorted(c) for c in communities_iter)
    for index, community in enumerate(communities, 1):
        label = "category" + str(index)
        for node in community:
            graph.nodes[node]["category"] = label

    # generate json string
    echarts_json = {
        "nodes": [],
        "edges": []
    }
    for node, attr in graph.nodes.items():
        echarts_json["nodes"].append({
            "name": node,
            "value": attr["degree"],
            "category": attr["category"],
            "symbolSize": attr["pageRank"]
        })
    for edge, attr in graph.edges.items():
        echarts_json["edges"].append({
            "source": edge[0],
            "target": edge[1],
            "label": {
                "formatter": attr["relation"]
            }
        })
    return json.dumps(echarts_json, ensure_ascii=False)


def text_2_echarts_data_json_str(text: str) -> str:
    """
    convert text to echarts data json str
    :param text: input text
    :return: json str
    """
    # triple_list = text_2_triple_list(text)
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
    return triple_list_2_echarts_data_json_str(triple_list)