import re


def remove_unicode_symbols(s):
    if s is None:
        return ""
    b = str(s).encode("ascii", errors='ignore')
    return str(b.decode("ascii"))


def camel_to_snake(s, upper=False):
    if not s:
        return s

    if '_' in s:
        words = [camel_to_snake(w, upper) for w in s.split('_')]
        s = "_".join(words)

    else:
        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)

    return upper and s.upper() or s.lower()


def camel_case_split(s, as_set=False, lower=False):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', s)

    if as_set and lower:
        return set([m.group(0).lower() for m in matches])

    if not as_set and lower:
        return [m.group(0).lower() for m in matches]

    return [m.group(0) for m in matches]


def get_first_word(s):
    return camel_case_split(s)[0]
