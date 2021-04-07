import os

from datetime import datetime, timedelta

from smlep_news.figaro import get_figaro_articles
from smlep_news.github import get_trending_repos
from smlep_news.guardian import get_recent_articles
from smlep_news.product_hunt import get_top_products
from smlep_news.tools import build_list_from_request
from smlep_news.weather import get_weather

today = datetime.now()
yesterday = today - timedelta(1)


def link(name, target):
    return '<a href="' + target + '"> ' + name + "</a>"


def format_weather(city_name, lat, lon, size, lg="en"):
    res = "{} {}<br>".format("Météo à" if lg == "fr" else "Weather in", city_name)
    suffix = "d'humidité<br>" if lg == "fr" else "humidity<br>"
    weathers = get_weather(lat, lon, os.environ["WEATHER_KEY"], hourly=True, lang=lg)
    for weather in weathers[:size]:
        res += "{}: {}°C / {} / {}% {}".format(
            weather.time.strftime("%Hh%M"),
            weather.temperature,
            weather.condition.description,
            weather.humidity,
            suffix,
        )
    return res


def format_ph(size, lg="en"):
    res = ""
    if lg == "en":
        res += "Top products from yesterday<br>"
    if lg == "fr":
        res += "Meilleurs produits d'hier<br>"
    products = get_top_products(
        os.environ["PH_CLIENT_ID"], os.environ["PH_CLIENT_SECRET"], yesterday, size
    )
    for product in products[:size]:
        res += link(product.name, product.url) + ": "
        res += product.description
        res += "<br>"
    return res


def format_gh(size, lg="en"):
    res = ""
    if lg == "en":
        res += "Top repos from yesterday<br>"
    if lg == "fr":
        res += "Meilleurs dépôts GitHub d'hier<br>"
    repos = get_trending_repos(" ", yesterday, today, size)

    for repo in repos[:size]:
        res += link(repo.name, repo.url)
        if repo.description is not None:
            res += ": " + repo.description
        res += "<br>"
    return res


def format_guardian(size):
    res = "Recent news<br>"
    articles = get_recent_articles(os.environ["GUARDIAN_KEY"], yesterday)
    for article in articles[:size]:
        res += link(article.title, article.url) + "<br>"
    return res


def format_figaro(size, long=False):
    res = "Articles récents<br>"
    articles = get_figaro_articles()
    for article in articles[:size]:
        res += link(article.title, article.url)
        if long:
            res += ": " + article.summary
        res += "<br>"
    return res
