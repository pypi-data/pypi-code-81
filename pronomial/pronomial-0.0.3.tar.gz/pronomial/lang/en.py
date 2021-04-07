from nltk import pos_tag as _ptag
from nltk.tokenize import word_tokenize

CATEGORY_EN = {
    'male': ['he', 'him', 'himself', 'his'],
    'female': ['she', 'her', 'herself', 'hers'],
    'first': ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our',
              'ours', 'ourselves'],
    'neutral': ['it', 'itself', 'its'],
    'plural': ['they', 'them', 'themselves', 'their', 'theirs', "who"]
}
PRONOUN_TAG_EN = ['PRP', 'PRP$', 'WP', 'WP$']
NOUN_TAG_EN = ['NN', 'NNP']
JJ_TAG_EN = ['JJ']
PLURAL_NOUN_TAG_EN = ['NNS', 'NNPS']
SUBJ_TAG_EN = ["nsubj", "dobj"]

GENDERED_WORDS_EN = {
    "female": ["mom", "mother", "woman", "women", "aunt", "girl", "girls",
               "sister", "sisters", "mothers"],
    "male": ["dad", "father", "man", "men", "uncle", "boy", "boys",
             "brother", "brothers", "fathers"]
}


def pos_tag_en(tokens):
    if isinstance(tokens, str):
        tokens = word_tokenize(tokens)

    postagged = _ptag(tokens)

    # HACK this fixes some know failures from postag
    # this is not sustainable but important cases can be added at any time
    # PRs + unittests welcome!
    ONOFF_VERBS = ["turn"]
    ON_OFF = ["on", "off"]
    for idx, (w, t) in enumerate(postagged):
        next_w, next_t = postagged[idx + 1] if \
                             idx < len(postagged) - 1 else ("", "")
        if w.lower() in ONOFF_VERBS and next_w.lower() in ON_OFF:
            # turn on/off
            if t == "NN":
                postagged[idx] = (w, "VBZ")
                postagged[idx + 1] = (next_w, "RP")
    # END HACK

    return postagged
