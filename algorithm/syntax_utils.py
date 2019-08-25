def parse_tree(tree, triples):

    sr, re, ta = None, None, None

    if tree.label() == "NP" and tree.height() == 3:
        entity_tokens = tree.flatten().leaves()
        entity = " ".join(entity_tokens)
        return entity, None
    elif tree.label().startswith("VB") or tree.label().startswith("IN"):
        relation_tokens = tree.flatten().leaves()
        relation = "_".join(relation_tokens)
        return None, relation
    elif tree.height() == 2:
        return None, None

    for i in range(len(tree)):
        e, r = parse_tree(tree[i], triples)
        if not sr:
            if e:
                sr = e
            if r:
                re = r
        elif sr and not re:
            if r:
                re = r
            if e:
                ta = e
        elif sr and re and not ta:
            if e:
                ta = e
        if sr and re and ta:
            triples.append([sr, re, ta])
            ta = None

    return sr, re


def parse_tree_v2(tree, triples):
    queue = []
    if tree.label() == "NP":
        if tree.height() == 3:
            entity_tokens = tree.flatten().leaves()
            entity = " ".join(entity_tokens)
            return [(entity, "e")]
        else:
            i = 0
            while i < len(tree):
                if tree[i].label() == "CC" or tree[i].label() == "," or tree[i].label() == "PP":
                    break
                i += 1
            if i == len(tree) or tree[i][0][0] == "of":
                entity_tokens = tree.flatten().leaves()
                entity = " ".join(entity_tokens)
                return [(entity, "e")]
    elif tree.label().startswith("VB") or tree.label().startswith("IN"):
        relation_tokens = tree.flatten().leaves()
        relation = " ".join(relation_tokens)
        return [(relation, "r")]
    elif tree.height() == 2 and (tree.label() == "CC" or tree.label() == "," or tree[0] == "alongside"):
        return [("CC", "c")]
    elif tree.height() == 2:
        return []

    for i in range(len(tree)):
        queue += parse_tree_v2(tree[i], triples)

    source, relation, target = None, None, None  # 只考虑了连接词在target的情况

    for record in queue:
        if record[1] == "e":
            if not target:
                target = record[0]
            else:
                source = record[0]
                relation = None
        elif record[1] == "r":
            if target:
                source = target
                target = None
            relation = record[0]
        elif record[1] == "c":
            target = None

        if source and relation and target:
            triples.append([source, relation, target])

    i = 0
    while i < len(queue):
        if queue[i][1] == "e":
            break
        else:
            i += 1

    return queue         # 可能返回queue的所有效果更好
