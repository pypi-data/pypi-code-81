import feedparser
from .constants import CURRENCY_RSS_MAPS


def trim_eur_rate(currency_code):
    url = CURRENCY_RSS_MAPS.get(currency_code.upper())
    _feed = feedparser.parse(url)
    entry = _feed.entries[1]
    return float(entry['cb_exchangerate'].split('\n')[0])


def get_rate(base="EUR", target="USD"):
    if base == "EUR":
        return trim_eur_rate(target)
    return float(trim_eur_rate(target) / trim_eur_rate(base))
