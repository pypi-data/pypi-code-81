import feedparser
from .fig_article import FigArticle


def get_figaro_articles():
    news_feed = feedparser.parse("http://www.lefigaro.fr/rss/figaro_actualites.xml")
    entries = news_feed.entries
    entry = news_feed.entries[1]

    res = []
    for entry in entries:
        res.append(FigArticle(entry))

    return res
