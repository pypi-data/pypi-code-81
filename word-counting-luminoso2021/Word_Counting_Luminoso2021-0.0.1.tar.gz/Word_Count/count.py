def word_counting(txt):
    """
    This function will accept the text line,
    remove all special characters,
    split into separate words,
    change all words into lowercase,
    find unique words,
    count frequency for unique words,
    return words, counts combination as a dictionary.
    """
    import re

    # remove all special characters and separate words and make all words in lowercase
    pattern = r'[^A-Za-z ]'
    regex = re.compile(pattern)
    wordlist = regex.sub('', txt).split(' ')
    wordlist = [w.lower() for w in wordlist]

    # find unique words for listing and count frequency and return the dictionary form of word:counts
    unique_wordlist = list(set(wordlist))
    word_freq = [wordlist.count(p) for p in unique_wordlist]
    counts = dict(zip(unique_wordlist, word_freq))

    return counts
