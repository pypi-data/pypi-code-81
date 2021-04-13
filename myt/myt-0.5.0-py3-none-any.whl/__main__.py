import sys
import os
import logging
import datetime
import json
import click
import pytz
import dateparser
import t
#import requests
#import ics

W = "\033[0m"  # white (normal)
R = "\033[31m"  # red
G = "\033[32m"  # green
O = "\033[33m"  # orange
B = "\033[34m"  # blue
P = "\033[35m"  # purple

DEFAULT_ZONES = [
    "UTC",
    "US/Eastern",
    "US/Central",
    "US/Mountain",
    "America/Phoenix",
    "US/Pacific",
    "US/Alaska",
    "Pacific/Tahiti",
    "Pacific/Auckland",
    "Australia/Sydney",
    "Australia/Darwin",
    "Asia/Hong_Kong",
    "Asia/Tokyo",
    "Asia/Kathmandu",
    "Europe/Riga",
    "Europe/Copenhagen",
]


def _dtDeltaHours(td):
    return td.seconds / 3600.0 + td.days * 24.0


def _hrsToHHMM(hrs):
    hh = int(hrs)
    mm = int(60 * abs(hrs - hh))
    return hh, mm


def _printRow(row, t_format):
    tz = row[0]
    line = f"{tz:17}"
    for v in row[1:]:
        if v.hour < 6 or v.hour > 18:
            sv = f" {B}{v.strftime(t_format)}{W}"
        else:
            sv = f" {O}{v.strftime(t_format)}{W}"
        line = line + sv
    line += W
    return line


@click.group()
@click.option(
    "-J",
    "--json",
    "json_format",
    is_flag = True,
    help="Output in JSON",
)
@click.pass_context
def main(ctx, json_format):
    ctx.ensure_object(dict)
    ctx.obj["json_format"] = json_format
    return 0


@main.command("zones", help="List common time zones and UTC offset (on date)")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.pass_context
def listTimeZones(ctx, date_str):
    if date_str is None:
        for_date = datetime.datetime.now()
    else:
        for_date = dateparser.parse(date_str)
    res = []
    for tz in pytz.common_timezones:
        z = pytz.timezone(tz)
        ofs = z.utcoffset(for_date)
        res.append((_dtDeltaHours(ofs), z.zone))
    res.sort()
    if ctx.obj["json_format"]:
        print(json.dumps(res))
        return 0
    for row in res:
        hh, mm = _hrsToHHMM(row[0])
        print(f"{hh:+03d}:{mm:02} {row[1]}")
    return 0


@main.command("z", help="24hrs in time zones (on date)")
@click.option("-f", "--format", "t_format", default="%H", help="Output time format")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.option(
    "-z",
    "--zones",
    "zone_list",
    default=",".join(DEFAULT_ZONES),
    help="Comma separated list of timezones",
)
@click.pass_context
def showZones(ctx, t_format, date_str, zone_list):
    if date_str is None:
        for_date = datetime.datetime.now().astimezone()
    else:
        for_date = dateparser.parse(
            date_str, settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
    zone_list = zone_list.split(",")
    t_zones = []
    for tz in zone_list:
        t_zones.append(pytz.timezone(tz.strip()))
    res = t.generateDayMatrix(t_zones, for_date)
    if ctx.obj["json_format"]:
        print(json.dumps(res, default=t._jsonConverter))
        return 0
    print(_printRow(res[0], t_format))
    for row in res[1:]:
        print(_printRow(row, t_format))
    return 0


@main.command("t", help="Time in different zones")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.option(
    "-z",
    "--zones",
    "zone_list",
    default=",".join(DEFAULT_ZONES),
    help="Comma separated list of timezones",
)
@click.pass_context
def showTimes(ctx, date_str, zone_list):
    if date_str is None:
        for_date = datetime.datetime.now().astimezone()
    else:
        for_date = dateparser.parse(
            date_str, settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
    zone_list = zone_list.split(",")
    res = [
        ("Local", for_date.astimezone()),
    ]
    for tzstr in zone_list:
        tz = pytz.timezone(tzstr.strip())
        dt = for_date.astimezone(tz)
        res.append((tz.zone, dt))
    if ctx.obj["json_format"]:
        print(json.dumps(res, default=t._jsonConverter))
        return 0
    for row in res:
        print(f"{row[0]:17} {t.datetimeToJsonStr(row[1])}")

def eventToJson(e):
    res = {}
    res['start'] = e.begin.astimezone(t.localTimezone())
    res['end'] = e.end.astimezone(t.localTimezone())
    res['summary'] = t._stripper(e.summary)
    res['description'] = t._stripper(e.description)
    res['location'] = e.location
    res['status'] = e.status
    res['duration'] = e.duration
    return res

# @main.command("c", short_help="Show calendar .ics")
# @click.argument("cal_file")
# @click.pass_context
# def showCalendar(ctx, cal_file):
#     cc = None
#     if not cal_file.startswith("http"):
#         if not os.path.exists(cal_file):
#             print(f"{R}Oops!{W} Can't find the .ics file: {cal_file}")
#             return 1
#         cc = ics.Calendar(open(cal_file, "r").read())
#     else:
#         cc = ics.Calendar(requests.get(cal_file, timeout=10).text)
#     if cc is None:
#         print(f"{R}Oops!{W} No calendar loaded")
#     n_events = len(cc.events)
#     print(f"{G}{len(cc.events)} event{'' if n_events ==0 else 's'}{W} in {cal_file}")
#     i = 1
#     while len(cc.events) > 0:
#         evnt = cc.events.pop()
#         ej = eventToJson(evnt)
#         if ctx.obj["json_format"]:
#             print(json.dumps(ej, indent=2, default=t._jsonConverter))
#         else:
#             print(f"Summary: {evnt.summary}")
#             print(f"Description: {evnt.description}")
#             print(f"Location: {evnt.location}")
#             print(f"URL: {evnt.url}")
#             print(f"Start: {evnt.begin}  {evnt.begin.astimezone(t.localTimezone())}")
#             print(f"End: {evnt.end}  {evnt.end.astimezone(t.localTimezone())}")
        

@main.command("s", short_help="Sun and moon")
@click.option("-l", "--location", default=None, help="Location as longitude,latitude (WGS84, dd)")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.option("-f", "--format", "t_format", default="%H:%M:%S", help="Output time format")
@click.pass_context
def getSolarInfo(ctx, location, date_str, t_format):
    for_date = None
    if date_str is None:
        for_date = datetime.datetime.now().astimezone()
    else:
        for_date = dateparser.parse(
            date_str, settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
    _location = {"latitude":0.0, "longitude":0.0}
    if location is not None:
        ltlg = location.strip().split(",")
        if len(ltlg) != 2:
            print("Location should be longitude,latitude")
            return 1
        _location["longitude"] = float(ltlg[0].strip())
        _location["latitude"] = float(ltlg[1].strip())
    else:
        _location = t.guessLocation()
    logging.debug(json.dumps(_location, indent=2))
    res = t.solarInfo(for_date, _location["longitude"], _location["latitude"])
    if ctx.obj["json_format"]:
        print(json.dumps(res, default=t._jsonConverter))
        return 0
    print(f"{G}Location: {_location['longitude']},{_location['latitude']}{W}")
    t3 = (
        res['dawn'].astimezone(t.localTimezone()).strftime(t_format),
        res['sunrise'].astimezone(t.localTimezone()).strftime(t_format),
        res['goldenHourEnd'].astimezone(t.localTimezone()).strftime(t_format),
    )
    print(f"Rise: {B}{t3[0]}{O}  {t3[1]}{W}  {t3[2]}")
    t3 = (
        res['goldenHour'].astimezone(t.localTimezone()).strftime(t_format),
        res['sunset'].astimezone(t.localTimezone()).strftime(t_format),
        res['dawn'].astimezone(t.localTimezone()).strftime(t_format),
    )
    print(f"Set:  {W}{t3[0]}{O}  {t3[1]}{B}  {t3[2]}{W}")
    print(f"{B}Moon: {t.moonPhase(res['phase'])} ({res['phase']:0.2f}){W}")


@main.command("m", short_help="Moon matrix")
@click.option("-y", "--year", "year_str", default=None, help="Year for calculation")
@click.pass_context
def getSolarInfo(ctx, location, year_str):
    cyear = 2021
    if year_str is None:
        cyear = datetime.datetime.now().astimezone().year
    else:
        cyear = int(year_str)
    print(f"     Moon phases for year: {cyear}")
    line = "    "
    for _day in range(1,32):
        line += f" {_day:02d}"
    print(line)
    for _month in range(1,13):
        line = f"{datetime.datetime(cyear,_month, 1).strftime('%b')} "
        for _day in range(1,32):
            try:
                dt = datetime.datetime(cyear,_month, _day)
                moon = t.moonInfo(dt)
                line += f" {t.moonPhase(moon['phase'])}"
            except ValueError:
                pass
        print(line)


if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix="T"))