from .utils import is_capitalized, is_vowel


def get_initial_consonant_cluster(word):
    """Get the length of the initial consonant cluster of a word."""

    for i in range(len(word)):
        if is_vowel(word[i]):
            break
        else:
            i += 1
    return word[:i], i


def piglatin_word(word):
    """Converts a single word into piglatin. Assumes no spaces or punctuation."""

    if is_vowel(word[0]):
        pigged = f"{word}way"
    elif not is_vowel(word[1]):
        clstr, clstr_len = get_initial_consonant_cluster(word)
        pigged = f"{word[clstr_len:]}{clstr}ay"
    else:
        pigged = f"{word[1:]}{word[0]}ay"
    return pigged if not is_capitalized(word) else pigged.capitalize()


def piglatin(string):
    """Convert the given string into piglatin. Does not currently support punctuation and
    will naively treat punctuation as just another letter."""

    words = string.split()

    return " ".join([piglatin_word(w) for w in words])


def reverse(string):
    """Return the given string in reverse order."""

    out = [string[-1 * (i + 1)] for i in range(len(string))]
    return "".join(out)
