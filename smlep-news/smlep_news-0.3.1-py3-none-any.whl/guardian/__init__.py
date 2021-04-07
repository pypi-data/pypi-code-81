import requests
from .article import Article

base = "https://content.guardianapis.com/world"


def get_recent_articles(key, from_date):
    url = "{}?api-key={}&order-by=relevance&from-date={}".format(
        base, key, from_date.strftime("%Y-%m-%d")
    )

    r = requests.get(url)
    r.raise_for_status()

    return [Article(a) for a in r.json()["response"]["results"]]
