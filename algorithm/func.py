from .openie_utils import *
from .syntax_utils import *
from nltk.parse import CoreNLPParser
import spacy
import neuralcoref


def text_2_triple_list(text, strength):
    nlp = spacy.load("en")
    neuralcoref.add_to_pipe(nlp)
    api = CoreNLPParser(url='http://39.98.186.125:9000')
    api.parser_annotator = "tokenize,ssplit,coref,openie"
    parser = CoreNLPParser(url='http://39.98.186.125:9000')

    text = clean_text(text)
    text = remove_adjective_possessive_pronoun(text)
    doc = nlp(text)
    text = doc._.coref_resolved
    entities = []
    entities_labels = []
    for e in doc.ents:
        if e.label_ in supported_entity_types:
            entities.append(e.text)
            entities_labels.append(e.label_)

    json_text = api.api_call(text)
    sentences = ssplit_article_into_sentences(json_text, step=-1)
    triples = []
    for sentence in sentences:
        json_sentence = api.api_call(sentence)
        triples += extract_triples_by_openie(json_sentence)
    entities = list(set(entities))

    triples = filter_triples_by_entities(triples, entities, strength)
    triples = beautify_triples(triples)
    triples = remove_meaningless_triples(triples)
    triples = check_triples_by_pos(triples)
    triples = remove_duplicate_triples(triples)

    return generate_structured_triples(triples, entities, entities_labels)
