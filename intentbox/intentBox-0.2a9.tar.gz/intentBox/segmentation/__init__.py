from intentBox.segmentation.simple import Segmenter
import re

try:
    import RAKEkeywords
except ImportError:
    RAKEkeywords = None


def rake(text, lang="en-us"):
    if not RAKEkeywords:
        raise ImportError("failed to import module RAKEkeywords")
    return RAKEkeywords.Rake(lang=lang).extract_keywords(text)


def chunk(text, delimiters=None):
    delimiters = delimiters or [".", ",", "!", "?", ";"]
    pattern = f"({'|'.join(delimiters)})"
    pts = re.split(pattern, text)
    return [p.strip() for p in pts if p.strip()]


def segment_keywords(text, lang="en-us", simple=False):
    if RAKEkeywords and lang and not simple:
        return chunk(text, delimiters=[_[0] for _ in rake(text, lang)])
    return text.split(" ")


def get_common_chunks(samples, lang="en-us"):
    s2k = {}
    raked = []
    for sample in samples:
        new_kws = segment_keywords(sample, lang=lang, simple=True)
        s2k[sample] = list(set([k for k in new_kws if len(k) > 3]))
        raked += s2k[sample]
    return [k for k in list(set(raked)) if all(k in v for v in s2k.values())]


if __name__ == "__main__":
    from pprint import pprint

    samples = ["should I bring an umbrella",
               "do I need an umbrella",
               "should I bring a rain coat",
               "do I need a rain coat"]

    #pprint(keyword_start_split(samples))
    # [{'name': 'start_kw',
    #   'required': True,
    #   'samples': ['should I bring', 'do I need']
    #  },
    #  {'name': 'required_kw',
    #   'required': True,
    #   'samples': ['a rain jacket', 'an umbrella', 'a rain coat']
    #  }]

    pprint(keyword_end_split(samples))
    exit()
    pprint(keyword_split(samples))
    # [{'name': 'start_kw',
    #   'required': True,
    #   'samples': ['should I bring', 'do I need']},
    #  {'name': 'entity_kw_rain jacket',
    #   'required': True,
    #   'samples': ['rain jacket', 'rain coat', 'umbrella']}]

    samples = ["do you dream",
               "do you dream about anything",
               "do you have a dream",
               "do you have dreams",
               "do you have any dreams"]
    pprint(keyword_entity_split(samples))
    # [{'name': 'entity_kw_dream', 'required': True, 'samples': ['dream', 'dreams']},
    #  {'name': 'question_kw',
    #   'required': True,
    #   'samples': ['do you',
    #               'do you have a',
    #               'do you have',
    #               'do you have any']},
    #  {'name': 'helper_kw', 'required': False, 'samples': ['about anything']}]

    samples = ["what do you dream about",
               "what did you dream about",
               "what are your dreams about"]
    pprint(keyword_entity_split(samples))
    # [{'name': 'entity_kw_dreams', 'required': True, 'samples': ['dreams', 'dream']},
    #  {'name': 'question_kw',
    #   'required': True,
    #   'samples': ['what do you', 'what did you', 'what are your']},
    #  {'name': 'helper_kw',
    #   'required': True,
    #   'samples': ['about', 'about', 'about']}]

    samples = ["do you dream",
               "did you dream",
               "do you have dreams"]
    pprint(keyword_entity_split(samples))
    # [{'name': 'entity_kw_dreams', 'required': True, 'samples': ['dreams', 'dream']},
    #  {'name': 'question_kw',
    #   'required': True,
    #   'samples': ['do you', 'did you', 'do you have']}]