import re

supported_entity_types = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC",
                          "PRODUCT", "EVENT", "WORK_OR_ART", "LAW"]




def clean_text(text):
    text = text.strip().replace("“", '"').replace("”", '"').replace("’", "'")\
               .replace("‘", "'").replace("``", "\"").replace("''", "\"").replace("_", "-")
    text = re.sub(" +", " ", text)
    text_tokens = text.split(" ")
    new_text_tokens = []
    for i, token in enumerate(text_tokens):
        if re.match(".+\.[A-Z].*", token):
            if token.endswith("."):
                new_text_tokens += [token]
                continue
            i = len(token) - 1
            while i >= 0:
                if token[i] == ".":
                    break
                i -= 1
            new_text_tokens += [token[:i+1], token[i+1:]]
        elif re.match(".+\?[A-Z].*", token):
            i = len(token) - 1
            while i >= 0:
                if token[i] == "?":
                    break
                i -= 1
            new_text_tokens += [token[:i + 1], token[i + 1:]]
        else:
            new_text_tokens += [token]
    text = " ".join(new_text_tokens)
    return text


def remove_adjective_possessive_pronoun(text):
    text = text.replace(" my ", " ").replace(" your ", " ").replace(" his ", " ")\
               .replace(" her ", " ").replace(" its ", " ").replace(" our ", " ").replace(" their ", " ")
    text = re.sub(" +", " ", text)
    return text


def coreference_resolution(json_text):
    sentences = []
    for sentence in json_text["sentences"]:
        sentences.append([e["word"] for e in sentence["tokens"]])
    for cluster_id, cluster in json_text["corefs"].items():
        original_entity = cluster[0]["text"]
        for i in range(1, len(cluster)):
            if cluster[i]["text"] in ["my", "your", "his", "her", "its", "our", "their"]:
                continue
    return [" ".join(sentence) for sentence in sentences]


def filter_triples_by_entities(triples, entities):
    ret_triples = []
    for triple in triples:
        for entity in entities:
            if entity in triple[0] or triple[0] in entity or entity in triple[2] or triple[2] in entity:
                ret_triples.append(triple)
                break
    return ret_triples


def extract_triples_by_openie(json_text):
    def is_subset(set1, set2):
        if (set1[0] <= set2[0] and set1[1] >= set2[1]) or (set1[0] >= set2[0] and set1[1] <= set2[1]):
            return True
        return False

    def is_meanless_triple(source, source_index, relation, relation_index, target, target_index):
        if source_index[0] >= relation_index[0] and source_index[0] <= relation_index[1] - 1:
            return True
        if source_index[1] - 1 >= relation_index[0] and source_index[1] - 1 <= relation_index[1] - 1:
            return True
        if target_index[0] >= relation_index[0] and target_index[0] <= relation_index[1] - 1:
            return True
        if target_index[1] - 1 >= relation_index[0] and target_index[1] - 1 <= relation_index[1] - 1:
            return True
        return False

    triples = []
    for sentence in json_text["sentences"]:
        sentence_triples = []
        for triple in sentence["openie"]:
            source = triple["subject"]
            source_index = triple["subjectSpan"]
            relation = triple["relation"]
            relation_index = triple["relationSpan"]
            target = triple["object"]
            target_index = triple["objectSpan"]
            source_tokens = source.split(" ")
            target_tokens = target.split(" ")

            if is_meanless_triple(source, source_index, relation, relation_index, target, target_index):
                continue

            if "in" in source_tokens or "in" in target_tokens \
                    or "at" in source_tokens or "at" in target_tokens \
                    or "by" in source_tokens or "by" in target_tokens:
                continue

            CHANGE_FLAG = False
            for cur_triple in sentence_triples:
                cur_source_index = cur_triple["index"][0]
                cur_relation_index = cur_triple["index"][1]
                cur_target_index = cur_triple["index"][2]
                cur_source = cur_triple["text"][0]
                cur_relation = cur_triple["text"][1]
                cur_target = cur_triple["text"][2]
                if is_subset(cur_source_index, source_index) \
                    and is_subset(cur_relation_index, relation_index) \
                    and is_subset(cur_target_index, target_index):

                    CHANGE_FLAG = True

                    if len(source) > len(cur_source):
                        cur_triple["index"][0] = source_index
                        cur_triple["text"][0] = source
                    if len(relation) < len(cur_relation):
                        cur_triple["index"][1] = relation_index
                        cur_triple["text"][1] = relation
                    if len(target) > len(cur_target):
                        cur_triple["index"][2] = target_index
                        cur_triple["text"][2] = target

            if not CHANGE_FLAG:
                sentence_triples.append({"index": [source_index, relation_index, target_index],
                                         "text": [source, relation, target]})
        for triple in sentence_triples:
            triples.append(triple["text"])
    return triples


def beautify_triples(triples):
    ret_triples = []
    for triple in triples:
        source = triple[0]
        relation = triple[1]
        target = triple[2]

        source = source.replace("-LRB-", "(").replace("-RRB-", ")").replace("( ", "(").replace(" )", ")")
        source = source.replace(" 's", "'s").replace("s '", "s'").replace("# ", "#").replace("$ ", "$").replace(" %", "%")
        source = source.replace("The ", "").replace("THE ", "").replace("the ", "") \
            .replace("An ", "").replace("AN ", "").replace("an ", "") \
            .replace("A ", "").replace("a ", "")

        target = target.replace("-LRB-", "(").replace("-RRB-", ")").replace("( ", "(").replace(" )", ")")
        target = target.replace(" 's", "'s").replace("s '", "s'").replace("# ", "#").replace("$ ", "$").replace(" %", "%")
        target = target.replace("The ", "").replace("THE ", "").replace("the ", "") \
            .replace("An ", "").replace("AN ", "").replace("an ", "") \
            .replace("A ", "").replace("a ", "")

        relation = relation.replace("is ", "").replace("at_time", "at")

        ret_triples.append([source, relation, target])

    return ret_triples


def remove_meaningless_triples(triples):
    def is_meaningless_entity(entity):
        if len(entity) <= 1:
            return True
        tokens = entity.split(" ")
        if len(tokens) == 1:
            if (not re.match(".*[A-Z].*", tokens[0]) and not ("-" in tokens[0])):
                return True
        return False
    ret_triples = []
    for triple in triples:
        if is_meaningless_entity(triple[0]) or is_meaningless_entity(triple[2]):
            continue
        if triple[0] == triple[2]:
            continue
        ret_triples.append(triple)
    return ret_triples


def ssplit_article_into_sentences(json_text, step):
    sentences = []
    for sentence in json_text["sentences"]:
        sentences.append(" ".join([e["word"] for e in sentence["tokens"]]).strip())

    if step == -1:
        return [" ".join(sentences)]
    elif step == 0:
        return sentences
    else:
        ret_sentences = []
        for i in range(len(sentences) - step):
            ret_sentences.append(" ".join(sentences[i: i+step]))
        return ret_sentences


def remove_duplicate_triples(triples):
    str_triples = ["|||".join(triple) for triple in triples]
    str_triples = list(set(str_triples))
    return [[e.strip() for e in str_triple.split("|||")] for str_triple in str_triples]
