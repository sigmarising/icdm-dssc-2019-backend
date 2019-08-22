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
