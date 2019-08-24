# RESTFul API

The RESTful API of this backend.

---

## 1. Article List Map

Get the category and identity of each article.

### Request

* Method: GET
* URL: `api/v1/articleListMap`

```json
{
}
```

### Response

```json
{
    "category1": [
        "identity1",
        "identity2",
    ],
    "category2": [
        "identity1",
        "identity2",
        "identity3",
    ],
    "category3": [
        "identity1"
    ]
}
```

---

## 2. Article Info

Get the sepecific article's content and knowledge graph (in echarts' data json string).

### Request

* Method: GET
* URL: `api/v1/articleInfo`

```json
{
    "category": "fruit",
    "identity": "id123456",
    "strength": "Medium",
}
```

### Response

```json
{
    "content": "BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. ",
    "graph": {
        "nodes": [],
        "edges": [],
        "classification": {},
        "categories": {}
    }
}
```

---

## 3. Knowledge Graph

Get the Knowledge Graph of the sepecific text.

### Request

* Method: GET
* URL: `api/v1/knowledgeGraph`

```json
{
    "text": "BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. ",
    "strength": "Medium",
}

```

### Response

```json
{
    "graph": {
        "nodes": [],
        "edges": [],
        "classification": {},
        "categories": {}
    }
}
```

---

## About Echarts' Graph Data Json

```json
{
    "nodes": [
        {
            "name": "car",
            "value": 10,
            "category": "",
            "symbolSize": 0.111
        },
        {
            "name": "store",
            "value": 30,
            "category": "",
            "symbolSize": 0.222
        }
    ],
    "edges": [
        {
            "source": "car",
            "target": "store",
            "label": {
                "formatter": "at"
            }
        }
    ],
    "classification": {
        "entityCategory": {
            "car": "Name",
            "store": "Location"
        },
        "communitiesDetection": {
            "car": "community 1",
            "store": "community 2"
        }
    },
    "categories": {
        "entityCategory": [
            { "name": "Name" },
            { "name": "Location" }
        ],
        "communitiesDetection": [
            { "name": "community 1" },
            { "name": "community 2" }
        ],
    }
}
```

* `name`: identify the node
* `value`: the degree of this node
* `category`: the community of this node
* `symbolSize`: the pagerank of this node
* `source`, `target`: the end of the edge
* `label.formatter`: the label of the edge
