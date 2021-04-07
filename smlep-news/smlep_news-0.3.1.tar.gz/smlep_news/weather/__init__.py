import requests
from .weather import CurrentWeather, DailyWeather, HourlyWeather

base = "https://api.openweathermap.org/data/2.5/onecall"


def get_weather(lat, lon, api_key, hourly=False, daily=False, lang="en"):
    exclude = "minutely"
    if not hourly:
        exclude += ",hourly"
    if not daily:
        exclude += ",daily"

    url = "{}?lat={}&lon={}&appid={}&exclude={}&units=metric&lang={}".format(
        base, lat, lon, api_key, exclude, lang
    )

    r = requests.get(url)
    r.raise_for_status()
    jr = r.json()

    res = [CurrentWeather(jr["current"])]
    if hourly:
        res += [HourlyWeather(j) for j in jr["hourly"]]
    if daily:
        res += [DailyWeather(j) for j in jr["daily"]]
    return res
