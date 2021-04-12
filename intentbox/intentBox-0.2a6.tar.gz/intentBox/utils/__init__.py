from logging import getLogger
import os
from enum import IntEnum, auto
from difflib import SequenceMatcher

try:
    import rapidfuzz
except ImportError:
    rapidfuzz = None



from intentBox.utils.bracket_expansion import SentenceTreeParser

LOG = getLogger("intentBox")

flatten = lambda l: [item for sublist in l for item in sublist]


def normalize(text, lang='', remove_articles=False):
    words = tokenize(text)
    if lang and lang.startswith("en"):
        if remove_articles:
            removals = ["the", "a", "an", "in", "on", "at"]
            words = [w for w in words if w.lower() not in removals]
    return " ".join(w for w in words if w)


def expand_parentheses(sent):
    """
    ['1', '(', '2', '|', '3, ')'] -> [['1', '2'], ['1', '3']]
    For example:
    Will it (rain|pour) (today|tomorrow|)?
    ---->
    Will it rain today?
    Will it rain tomorrow?
    Will it rain?
    Will it pour today?
    Will it pour tomorrow?
    Will it pour?
    Args:
        sent (list<str>): List of tokens in sentence
    Returns:
        list<list<str>>: Multiple possible sentences from original
    """
    return SentenceTreeParser(sent).expand_parentheses()


def invert_dict(base):
    return {v: k for k, v in base.items()}


def tokenize(text):
    # very simple, tokenize punctuation
    punct = [".", ",", ";", "-", "!", "?"]
    for p in punct:
        text = text.replace(p, " " + p + " ")
    return [w for w in text.split(" ") if w.strip()]


def resolve_resource_file(res_name):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for ~/.mycroft/res_name first, and
    if not found will look at /opt/mycroft/res_name,
    then finally it will look for res_name in the 'mycroft/res'
    folder of the source code package.

    Example:
    With mycroft running as the user 'bob', if you called
        resolve_resource_file('snd/beep.wav')
    it would return either '/home/bob/.mycroft/snd/beep.wav' or
    '/opt/mycroft/snd/beep.wav' or '.../mycroft/res/snd/beep.wav',
    where the '...' is replaced by the path where the package has
    been installed.

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """
    # First look for fully qualified file (e.g. a user setting)
    if os.path.isfile(res_name):
        return res_name

    # Now look for ~/chatterbox/res_name (in user folder)
    filename = os.path.expanduser("~/chatterbox/" + res_name)
    if os.path.isfile(filename):
        return filename

    # Resource cannot be resolved
    raise FileNotFoundError(res_name)


def expand_options(sentece):
    sentences = []
    sentece = sentece.replace("[", "(").replace("]", "| )")
    for exp in expand_parentheses(tokenize(sentece)):
        sentences.append(" ".join(exp).replace("(", "[").replace(")", "]"))
    return sentences


def expand_keywords(sentence):
    kwords = {"required": [], "optional": []}

    in_optional = False
    for exp in expand_parentheses(tokenize(sentence)):
        if "[" in exp:
            in_optional = True
            required = exp[:exp.index("[")]
            kwords["required"].append(" ".join(required))
            optional = exp[exp.index("[") + 1:]
            kwords["optional"].append(
                " ".join(optional).replace("]", "").strip())
        elif in_optional:
            optional = exp
            kwords["optional"].append(
                " ".join(optional).replace("]", "").strip())
            if "]" in exp:
                in_optional = False
        else:
            kwords["required"].append(" ".join(exp))
    return kwords


def merge_dict(base, delta, merge_lists=False, skip_empty=False,
               no_dupes=True, new_only=False):
    """
        Recursively merges two dictionaries
        including dictionaries within dictionaries.

        Args:
            base:  Target for merge
            delta: Dictionary to merge into base
            merge_lists: if a list is found merge contents instead of replacing
            skip_empty: if an item in delta is empty, dont overwrite base
            no_dupes: when merging lists deduplicate entries
            new_only: only merge keys not yet in base
    """

    for k, d in delta.items():
        b = base.get(k)
        if isinstance(d, dict) and isinstance(b, dict):
            merge_dict(b, d, merge_lists, skip_empty, no_dupes, new_only)
        else:
            if new_only and k in base:
                continue
            if skip_empty and d in [None, "", []]:
                # dont replace if new entry is empty
                # False and 0 should still be replaced
                pass
            elif all((isinstance(b, list), isinstance(d, list), merge_lists)):
                if no_dupes:
                    base[k] += [item for item in d if item not in base[k]]
                else:
                    base[k] += d
            else:
                base[k] = d
    return base


class MatchStrategy(IntEnum):
    SIMPLE_RATIO = auto()
    RATIO = auto()
    PARTIAL_RATIO = auto()
    TOKEN_SORT_RATIO = auto()
    TOKEN_SET_RATIO = auto()
    PARTIAL_TOKEN_RATIO = auto()
    PARTIAL_TOKEN_SORT_RATIO = auto()
    PARTIAL_TOKEN_SET_RATIO = auto()


def _validate_matching_strategy(strategy):
    if rapidfuzz is None and strategy != MatchStrategy.SIMPLE_RATIO:
        LOG.error("rapidfuzz is not installed, "
                  "falling back to SequenceMatcher for all match strategies")
        LOG.warning("pip install rapidfuzz")
        return MatchStrategy.SIMPLE_RATIO
    return strategy


def fuzzy_match(x, against, strategy=MatchStrategy.SIMPLE_RATIO):
    """Perform a 'fuzzy' comparison between two strings.
    Returns:
        float: match percentage -- 1.0 for perfect match,
               down to 0.0 for no match at all.
    """
    strategy = _validate_matching_strategy(strategy)
    if strategy == MatchStrategy.RATIO:
        score = rapidfuzz.fuzz.ratio(x, against) / 100
    elif strategy == MatchStrategy.PARTIAL_RATIO:
        score = rapidfuzz.fuzz.partial_ratio(x, against) / 100
    elif strategy == MatchStrategy.TOKEN_SORT_RATIO:
        score = rapidfuzz.fuzz.token_sort_ratio(x, against) / 100
    elif strategy == MatchStrategy.TOKEN_SET_RATIO:
        score = rapidfuzz.fuzz.token_set_ratio(x, against) / 100
    elif strategy == MatchStrategy.PARTIAL_TOKEN_SORT_RATIO:
        score = rapidfuzz.fuzz.partial_token_sort_ratio(x, against) / 100
    elif strategy == MatchStrategy.PARTIAL_TOKEN_SET_RATIO:
        score = rapidfuzz.fuzz.partial_token_set_ratio(x, against) / 100
    elif strategy == MatchStrategy.PARTIAL_TOKEN_RATIO:
        score = rapidfuzz.fuzz.partial_token_ratio(x, against) / 100
    else:
        score = SequenceMatcher(None, x, against).ratio()

    return score


def match_one(query, choices, match_func=None,
              strategy=MatchStrategy.SIMPLE_RATIO):
    """
        Find best match from a list or dictionary given an input

        Arguments:
            query:   string to test
            choices: list or dictionary of choices

        Returns: tuple with best match, score
    """
    return match_all(query, choices, match_func, strategy)[0]


def match_all(query, choices, match_func=None,
              strategy=MatchStrategy.SIMPLE_RATIO):
    """
        match scores from a list or dictionary given an input

        Arguments:
            query:   string to test
            choices: list or dictionary of choices

        Returns: list of tuples (match, score)
    """
    strategy = _validate_matching_strategy(strategy)
    match_func = match_func or fuzzy_match
    if isinstance(choices, dict):
        _choices = list(choices.keys())
    elif isinstance(choices, list):
        _choices = choices
    else:
        raise ValueError('a list or dict of choices must be provided')
    matches = []
    for c in _choices:
        if isinstance(choices, dict):
            matches.append((choices[c], match_func(query, c, strategy)))
        else:
            matches.append((c, match_func(query, c, strategy)))

    # TODO solve ties

    return sorted(matches, key=lambda k: k[1], reverse=True)


if __name__ == "__main__":
    sentences = ['i ( love | like ) mycroft',
                 'mycroft is ( open | free | private )']

    sentences += [
        'what is weather like [ in canada | in france | in portugal ]',
        'how is weather like [ in { location } ]',
        'tell me weather [ at { location } | in { location } ]']
    for s in sentences:
        print(expand_keywords(s))
