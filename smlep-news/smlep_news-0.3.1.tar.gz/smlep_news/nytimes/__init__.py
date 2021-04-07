import requests

from .article import Article

base = "https://api.nytimes.com/svc/mostpopular/v2/viewed/"


def get_most_viewed_articles(key, days_count):
    if days_count not in [1, 7, 30]:
        raise ValueError("The days period must be 1, 7 or 30")
    url = "{}{}.json?api-key={}".format(base, days_count, key)

    r = requests.get(url)
    r.raise_for_status()

    return [Article(a) for a in r.json()["results"]]
