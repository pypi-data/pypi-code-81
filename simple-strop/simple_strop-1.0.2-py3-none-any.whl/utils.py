from string import punctuation

PUNCTUATION = set(punctuation)
VOWELS = {"a", "e", "i", "o", "u"}

del punctuation


def is_capitalized(string):
    """Return true if the string starts with a capital letter, false otherwise."""

    first_char = string[0]
    return first_char == first_char.upper()


def is_all_caps(string):
    """Return true if the entire string is in capital letters, false otherwise."""

    return all([char == char.upper() for char in string])


def is_vowel(char):
    """Return true if the character is a vowel, false otherwise."""

    return char.lower() in VOWELS


def is_consonant(char):
    """Return true if the character is a consonant, false otherwise."""

    return not is_vowel(char) and char not in PUNCTUATION
