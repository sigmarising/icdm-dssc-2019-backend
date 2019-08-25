import re
from nltk.parse import CoreNLPParser

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
               .replace(" her ", " ").replace(" its ", " ").replace(" our ", " ")\
               .replace(" their ", " ").replace("alongside", "and")
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


def filter_triples_by_entities(triples, entities, strength):
    ret_triples = []
    if strength == 1:
        return triples
    elif strength == 2:
        for triple in triples:
            for entity in entities:
                if entity in triple[0] or triple[0] in entity or entity in triple[2] or triple[2] in entity:
                    ret_triples.append(triple)
                    break
    elif strength == 3:
        for triple in triples:
            source_flag = False
            target_flag = False
            for entity in entities:
                if entity in triple[0] or triple[0] in entity:
                    source_flag = True
                if entity in triple[2] or triple[2] in entity:
                    target_flag = True
            if source_flag and target_flag:
                ret_triples.append(triple)

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
        source = source.replace(" 's", "'s").replace("s '", "s'").replace("# ", "#").replace("$ ", "$").replace(" %", "%n")
        if source.lower().startswith("the "):
            source = source[4:]
        if source.lower().startswith("an "):
            source = source[3:]
        if source.lower().startswith("a "):
            source = source[2:]
        source = source.replace("`` ", "\"").replace(" ''","\"").replace("` ", "'").replace(" '","'")

        target = target.replace("-LRB-", "(").replace("-RRB-", ")").replace("( ", "(").replace(" )", ")")
        target = target.replace(" 's", "'s").replace("s '", "s'").replace("# ", "#").replace("$ ", "$").replace(" %", "%")
        if target.lower().startswith("the "):
            target = target[4:]
        if target.lower().startswith("an "):
            target = target[3:]
        if target.lower().startswith("a "):
            target = target[2:]
        target = target.replace("`` ", "\"").replace(" ''","\"").replace("` ", "'").replace(" '","'")

        relation = relation.replace("is ", "").replace("at_time", "at")
        relation = relation.replace("`` ", "\"").replace(" ''","\"")

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
        if triple[0].strip() == triple[2].strip():
            continue
        if triple[0].strip() in ["IT", "It", "it"] or triple[2].strip() in ["IT", "It", "it"]:
            continue
        if triple[1].strip().lower() == "of" or triple[1].strip().lower() == "for" or triple[1].strip().lower() == "with" or triple[1].strip().lower() == "if":
            continue
        if triple[1].lower() == "'s":
            continue
        triple[1] = triple[1].replace("'s", "").strip()
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
    ret_triples = []
    for triple in triples:
        flag = False
        for exist_triple in ret_triples:
            if triple[0] == exist_triple[0] and triple[2] == exist_triple[2]:
                flag = True
                break
        if not flag:
            ret_triples.append(triple)

    return ret_triples


def check_triples_by_pos(triples):
    pos_tagger = CoreNLPParser(url='http://39.98.186.125:9000', tagtype='pos')
    ret_triples = []
    for triple in triples:
        source = triple[0]
        relation = triple[1]
        target = triple[2]
        source_pos = ",".join([e[1] for e in pos_tagger.tag(source.split(" "))])
        relation_pos = ",".join([e[1] for e in pos_tagger.tag(relation.split(" "))])
        target_pos = ",".join([e[1] for e in pos_tagger.tag(target.split(" "))])

        if "VB" in source_pos or "VB" in target_pos:
            continue
        if "NN" not in source_pos or "NN" not in target_pos:
            continue
        if "NN" in relation_pos:
            if " at" in relation.lower():
                relation = "at"
            elif "of" not in relation.split(" ") and len(relation.split(" ")) > 1:
                continue

        ret_triples.append([source, relation, target])

    return ret_triples


def generate_structured_triples(triples, entities, entities_labels):
    ret_triples = []
    for triple in triples:
        sourceType = "default"
        targetType = "default"
        for i, entity in enumerate(entities):
            if entity in triple[0] or triple[0] in entity:
                sourceType = entities_labels[i]
            if entity in triple[2] or triple[2] in entity:
                targetType = entities_labels[i]
        ret_triples.append({"source":triple[0],"sourceType":sourceType,
                            "target":triple[2],"targetType":targetType,"relation":triple[1]})

    return ret_triples


def normalize_entities(triples, syntax_triples):
    ents = []
    ents += [e[0] for e in triples]
    ents += [e[2] for e in triples]
    new_syntax_triples = []
    for triple in syntax_triples:
        source = triple[0]
        relation = triple[1]
        target = triple[2]
        for ent in ents:
            if source in ent or ent in source:
                source = ent
            if target in ent or ent in target:
                target = ent
        if source == target:
            continue
        new_syntax_triples.append([source, relation, target])
    # print(len(triples), len(syntax_triples))
    return triples + new_syntax_triples
