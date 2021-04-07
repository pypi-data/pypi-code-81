import requests
from .repository import Repository
from smlep_news.tools import build_list_from_request

base = "https://api.github.com/"


def get_trending_repos(key, from_date, to_date, count=30):
    if count > 100:
        raise ValueError(
            "More than 100 items cannot be retrieved in one page, got {}".format(count)
        )
    url = base + "search/repositories?q=" + key
    url += "+created:{}..{}".format(
        from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
    )
    url += "&sort=stars&order=desc&per_page={}".format(count)
    r = requests.get(url)
    return build_list_from_request(r, "items", Repository)
