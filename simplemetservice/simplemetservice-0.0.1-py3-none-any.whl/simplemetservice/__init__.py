"""
Simple Python package for accessing MetService data
"""
import requests as _requests
import re as _re

_DEFAULT_BASE = 'http://metservice.com/publicData'

_TOWN_SLUG_REGEX = _re.compile(r'\/([\w-]+)$')

def _get_data(endpoint: str, base: str):
    """
    Retrieves data from the MetService public data site.
    """
    try:
        resp = _requests.get(base + endpoint)
        resp.raise_for_status()
        return resp.json()
    except _requests.HTTPError:
        raise _requests.HTTPError()
        return None

def _city_data(city: str, endpoint: str, base: str):
    return _get_data(endpoint.format(city), base)

def get_cities_list(base = _DEFAULT_BASE):
    """
    Returns a dictionary of valid city names.
    """
    resp = _get_data("/webdata/towns-cities", base)

    search = resp["layout"]["search"]

    towns = {}
    for island in search:
        for region in island["items"]:
            for town in region["children"]:
                town_url = town["url"]


                towns[town["label"]] = _TOWN_SLUG_REGEX.search(town_url).group(1)

    return str(towns).encode('utf-8')

def _getLocalForecastData(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/localForecast{city}', base)

def getSunProtectionAlert(city: str, base: str = _DEFAULT_BASE):
    return _get_data(f'/sunProtectionAlert{city}', base)

def _getOneMinObs(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/oneMinObs_{city}', base)

def _getHourlyObsAndForecast(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/hourlyObsAndForecast_{city}', base)

def _getLocalObs(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/localObs_{city}', base)

def _getTides(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/tides_{city}', base)

def _getWarningsData(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/warningsForRegion3_urban.{city}', base)

def _getRisesData(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/riseSet_{city}', base)

def _getPollenData(city: str, base: str = _DEFAULT_BASE):
    """
    Returns unprocessed data
    """
    return _get_data(f'/pollen_town_{city}', base)

#def getDaily(city: str, base: str = _DEFAULT_BASE):
    #return _get_data(f'/climateDataDailyTown_{city}_32', base)

def getForecast(city, day: str = "today"):
    """
    Returns the forecast for the specified city and day.
    Use "get_cities_list()" for all valid city names.
    "day" is default 'today', use 'tommorow' for the next day, use 'overmorow' for the day after tommorow and add additional 'over's for subsequent days. e.g. 'overovermorow'
    """
    if day == "today":
        d = 0
        today = _getLocalForecastData(city)["days"][d]
        oneword = "; Morning: " + today["partDayData"]["morning"]["forecastWord"] + ", Afternoon: " + today["partDayData"]["afternoon"]["forecastWord"] + ", Evening: " + today["partDayData"]["evening"]["forecastWord"]
    elif day == "tommorow":
        d = 1
        today = _getLocalForecastData(city)["days"][d]
        oneword = "; Morning: " + today["partDayData"]["morning"]["forecastWord"] + ", Afternoon: " + today["partDayData"]["afternoon"]["forecastWord"] + ", Evening: " + today["partDayData"]["evening"]["forecastWord"]
    else:
        d = 1 + (day.count("over"))
        today = _getLocalForecastData(city)["days"][d]
        oneword = ""
    return today["dow"] + " " + today["date"] + ": " + today["forecast"] + " High of " + today["max"]  + " - Low of " + today["min"] + oneword + " - issued at:" + today["issuedAt"]

def getPollen(city, day: str = "today"):
    """
    Returns the pollen level and type for the specified city and day.
    Use "get_cities_list()" for all valid city names.
    "day" is default 'today', use 'tommorow' for the next day, use 'overmorow' for the day after tommorow and add additional 'over's for subsequent days. e.g. 'overovermorow'
    """
    if day == "today":
        d = 0
    elif day == "tommorow":
        d = 1
    else:
        d = 1 + (day.count("over"))
    today = _getPollenData(city)["pollen"][d]
    return "Pollen Level: " + today["level"] + ", Type:" + today["type"] + " - Valid From: " + today["validFrom"] + " To " + today["validTo"]
def getWarnings(city):
    """
    Returns any warnings for the specified city.
    """
    warnings = _getWarningsData(city)["warnings"]
    if warnings == []:
        return None
    else:
        return warnings
def getSunRise(city):
    """
    Returns todays sunrise for the specified city.
    """
    return _getRisesData(city)["sunRise"]
def getSunSet(city):
    """
    Returns todays sunset for the specified city.
    """
    return _getRisesData(city)["sunSet"]
def getMoonRise(city):
    """
    Returns todays moonrise for the specified city.
    """
    return _getRisesData(city)["moonRise"]
def getMoonSet(city):
    """
    Returns todays moonset for the specified city.
    """
    return _getRisesData(city)["moonSet"]
def getFirstlight(city):
    """
    Returns todays first light for the specified city.
    """
    return _getRisesData(city)["firstlight"]
def getLastLight(city):
    """
    Returns todays last ligth for the specified city.
    """
    return _getRisesData(city)["lastLight"]
def getClothingLayers(city):
    """
    Returns todays recommended number of clothing layers for the specified city.
    """
    return "Number Of Clothing Layers Required: " + _getOneMinObs(city)["clothingLayers"]
def getWindProofLayers(city):
    """
    Returns todays recommended number of wind proof clothing layers for the specified city.
    """
    return "Number Of Wind Proof Layers Required: " + _getOneMinObs(city)["windProofLayers"]
