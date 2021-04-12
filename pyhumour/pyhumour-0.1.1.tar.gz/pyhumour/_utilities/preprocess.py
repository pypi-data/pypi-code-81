import re
import json
from nltk import (
    tokenize,
    pos_tag
)
import os
import sys

def preprocess_text(text):
    text = text.lower()
    resources_path = os.path.join(os.path.dirname(sys.modules["pyhumour"].__file__), "resources")
    contraction_map = json.load(open(os.path.join(resources_path, "contraction_map.json")))
    change_characters = {'‚': ',', '\ufeff': ' ', '„': '"', "—": '-', '™': ' ', '″': '"', 'ƒ': 'f', '�': ' ',
                         '′': "'", '‘': "'",
                         '…': '...', '’': "'", '‑': '-', '\u2028': ' ', 'π': 'π', 'Ł': ' ', '⚪': ' ', '–': '-',
                         '\u200b': ' ', '”': '"',
                         'Н': 'H', '€': '€'}
    is_change_characters = set(text).intersection(change_characters.keys())
    if is_change_characters:
        for i in is_change_characters:
            text = re.sub(i, change_characters[i], text)
    # contraction_map removal
    words = set(text.split())  # taking all the unique words in a sentence
    is_change_words = words.intersection(contraction_map.keys())
    if is_change_words:
        for i in is_change_words:
            text = re.sub(i, contraction_map[i], text)
    if '<' in set(text):
        text = re.sub("<.*>", "", text)
    text = " ".join(text.split())
    text = " ".join(tokenize.sent_tokenize(text))
    text = " ".join(tokenize.word_tokenize(text))

    return text


def preprocess_texts(text_list: list) -> list:
    preprocess_texts_list = []
    for text in text_list:
        preprocess_texts_list.append(preprocess_text(text))

    return preprocess_texts_list


def pos_tag_texts(text_list: list) -> list:
    pos_tag_text_list = []
    for text in text_list:
        pos_tag_text_list.append(pos_tag(tokenize.word_tokenize(text)))

    return pos_tag_text_list