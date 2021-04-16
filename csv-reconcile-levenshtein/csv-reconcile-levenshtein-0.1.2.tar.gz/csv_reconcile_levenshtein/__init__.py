__version__ = '0.1.2'

from csv_reconcile import scorer
from Levenshtein import distance


@scorer.register
def getNormalizedFields():
    return ()


@scorer.register
def processScoreOptions(options):
    if not options:
        return

    options['stopwords'] = [w.lower() for w in options['stopwords']]


@scorer.register
def scoreMatch(left, right):
    ln = max(left, right) * 1.0

    return 100.0 * (ln - distance(left, right)) / ln


@scorer.register
def normalizeWord(word, **scoreOptions):
    return ()
