import re


def word_tokenize(input_string):
    return [m.group() for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def char_indexed_word_tokenize(input_string):
    return [(m.start(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def span_indexed_word_tokenize(input_string):
    return [(m.start(0), m.end(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def chunk(text, delimiters):
    pattern = f"({'|'.join(delimiters)})"
    pts = re.split(pattern, text)
    return [p.strip() for p in pts if p.strip()]


def get_common_chunks(samples):
    s2k = {}
    raked = []
    for sample in samples:
        new_kws = word_tokenize(sample)
        s2k[sample] = list(set([k for k in new_kws if len(k) > 3]))
        raked += s2k[sample]
    return [k for k in list(set(raked)) if all(k in v for v in s2k.values())]


if __name__ == "__main__":
    samples = ["what do you dream about",
               "what did you dream about",
               "what are your dreams about"]
    print(get_common_chunks(samples))
    # ['what', 'about']

    keywords = ["mycroft"]
    sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
    print(chunk(sentence, keywords))
    # ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft', 'is FOSS!']

    print(word_tokenize(sentence))
    # ['sometimes', 'i', 'develop', 'stuff', 'for', 'mycroft', ',', 'mycroft', 'is', 'FOSS', '!']

    print(char_indexed_word_tokenize(sentence))
    # [(0, 'sometimes'), (10, 'i'), (12, 'develop'), (20, 'stuff'), (26, 'for'), (30, 'mycroft'), (37, ','), (39, 'mycroft'), (47, 'is'), (50, 'FOSS'), (54, '!')]

    print(span_indexed_word_tokenize(sentence))
    # [(0, 9, 'sometimes'), (10, 11, 'i'), (12, 19, 'develop'), (20, 25, 'stuff'), (26, 29, 'for'), (30, 37, 'mycroft'), (37, 38, ','), (39, 46, 'mycroft'), (47, 49, 'is'), (50, 54, 'FOSS'), (54, 55, '!')]
