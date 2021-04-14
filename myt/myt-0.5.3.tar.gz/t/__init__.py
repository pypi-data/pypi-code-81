import pytz
import datetime
import json
import requests
from . import suncalc

JSON_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""datetime format string for generating JSON content
"""

def localTimezone():
    tznow = datetime.datetime.now().astimezone()
    return tznow.tzinfo

def datetimeToJsonStr(dt):
    if dt is None:
        return None
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        # Naive timestamp, convention is this must be UTC
        return f"{dt.strftime(JSON_TIME_FORMAT)}Z"
    return dt.strftime(JSON_TIME_FORMAT)


def utcFromDateTime(dt, assume_local=True):
    # is dt timezone aware?
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        if assume_local:
            # convert local time to tz aware utc
            dt.astimezone(datetime.timezone.utc)
        else:
            # asume dt is in UTC, add timezone
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    # convert to utc timezone
    return dt.astimezone(datetime.timezone.utc)

def _jsonConverter(o):
    if isinstance(o, datetime.datetime):
        return datetimeToJsonStr(o)
    return o.__str__()


def generateDayMatrix(tzones, for_date):
    t0 = for_date.astimezone()
    row = ['Local', ]
    for hr in range(0,24):
        dt = datetime.timedelta(hours=hr)
        t1 = t0 + dt
        row.append(t1)
    res = [row, ]
    for z in tzones:
        t0 = for_date
        t0 = t0.replace(minute=0, second=0, microsecond=0)
        row = [z.zone, ]
        for hr in range(0, 24):
            td = datetime.timedelta(hours=hr)
            t1 = t0 + td
            t2 = t1.astimezone(z)
            row.append(t2)
        res.append(row)
    return res

def _stripper(s):
    try:
        return s.strip()
    except:
        pass
    return s


def guessLocation():
    '''Guess location from external ip
    '''
    service = "http://radio.garden/api/geo"
    res = requests.get(service, timeout=5)
    data = res.json()
    return data


def solarInfo(dt, longitude, latitude):
    udt = utcFromDateTime(dt, assume_local=True)
    info = suncalc.getTimes(dt, latitude, longitude)
    moon = suncalc.getMoonIllumination(udt)
    info.update(moon)
    return info

def moonInfo(dt):
    udt = utcFromDateTime(dt, assume_local=True)
    return suncalc.getMoonIllumination(udt)

def moonPhase(frac):
    '''
    0 - 0.07
    0.12 -0.19
    0.25 -0.31
    0.37 -0.45
    0.50 -0.55
    0.62 -0.69
    0.75 -0.81
    0.87 -0.93
    1.0
    '''
    if frac < 0.07:
        return "🌑"
    if frac < 0.19:
        return "🌒"
    if frac < 0.31:
        return "🌓"
    if frac < 0.45:
        return "🌔"
    if frac < 0.55:
        return "🌕"
    if frac < 0.69:
        return "🌖"
    if frac < 0.81:
        return "🌗"
    if frac < 0.93:
        return "🌘"
    return "🌑"
