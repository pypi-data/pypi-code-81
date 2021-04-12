# -*- coding: utf-8 -*-
import logging
import os
import pytz
import re
import requests
import yaml

from icalendar import Calendar
from requests.auth import HTTPBasicAuth
from requests.exceptions import MissingSchema

from tracklr.vdir import Vdir

try:
    import appdirs
except ModuleNotFoundError:
    print(
        "appdirs missing - should the issue persists post install, "
        "run `pip install appdirs` manually"
    )

try:
    from pyfiglet import Figlet
except ModuleNotFoundError:
    Figlet = None


class Tracklr(object):
    """Tracklr loads events recorded in `iCalendar` feeds and
    uses them to create reports.
    """

    __version__ = "1.5.3"

    __config__ = """
---
# List of calendars
#
# calendar attributes:
# * location          - mandatory - ical calendar feed location - either URL or directory
# * name              - optional  - use `default` for your default calendar ie. useful for single calendar users
# * title/subtitle    - optional  - info used by `ls` and `pdf` commands
# * username/password - optional  - for BasicHTTPAuth protected feeds
#
calendars:
  # Tracklr demo calendar - simplest single calendar config v1
  #- https://calendar.google.com/calendar/ical/bdtrpfi80dtav668iqd38oqi7g%40group.calendar.google.com/public/basic.ics

  # Tracklr demo calendar - simplest single calendar config v2
  #- location: https://calendar.google.com/calendar/ical/bdtrpfi80dtav668iqd38oqi7g%40group.calendar.google.com/public/basic.ics

  # Tracklr demo calendar - simplest single calendar config v3
  # X-WR-TIMEZONE support for of the demo Google Calendar feed enabled
  # This fixes timezone issue because the demo calendar is in New Zealand timezone and reports
  # would be showing incorrect dates ie.
  # | 2019-03-29 - 2019-03-30 | @Tracklr #v0.7
  # instead of correct
  # | 2019-03-30 | @Tracklr #v0.7
  - location: https://calendar.google.com/calendar/ical/bdtrpfi80dtav668iqd38oqi7g%40group.calendar.google.com/public/basic.ics
    title: Tracklr
    subtitle: Demo Calendar
    timezone: True

  # Tracklr demo calendar - minimal default config
  #- name: minimal
  #  location: https://calendar.google.com/calendar/ical/bdtrpfi80dtav668iqd38oqi7g%40group.calendar.google.com/public/basic.ics

  # Tracklr demo calendar - full config
  #- name: full
  #  location: https://calendar.google.com/calendar/ical/bdtrpfi80dtav668iqd38oqi7g%40group.calendar.google.com/public/basic.ics
  #  title: Tracklr Demo
  #  subtitle: Report
  #  timezone: Pacific/Auckland

  # Example of vdir configuration
  #- name: demo
  #  location: ~/.calendars/ab14901f-017b-78df-28bc-92d9387e5cfb

  # 
  #- name: 
  #  location: 
  #  username: 
  #  password: 
        """

    def __init__(self):
        """Initializes Tracklr object with its configuration.
        """
        self.log = logging.getLogger(__name__)

        self.calendars = dict()

        self.report = []
        self.report_html = []

        self.matches = dict()

        self.total_seconds = 0.0
        self.total_hours = 0.0
        self.total_sum = 0.0

        self.pdf_template_file = "pdf.html"
        self.pdf_output_file = "report.pdf"

        self.local_path = os.getcwd()
        self.global_path = os.path.join(appdirs.user_config_dir(), "tracklr")

        self.template_path = [self.local_path, self.global_path]

        self.config_file = "tracklr.yml"
        self.config_dot_file = ".tracklr.yml"

        self.loaded_config_file = None

        self.config = None
        self.configure()

    def banner(self, kalendar, title=None, subtitle=None, use_figlet=True):
        """Displays base information about the Tracklr instance.
        """
        cal = self.get_calendar_config(kalendar)

        title = self.get_title(cal["name"], title)
        subtitle = self.get_subtitle(cal["name"], subtitle)

        tracklr_banner = "Tracklr"

        if Figlet is not None and use_figlet is True:
            banner = Figlet(font="fuzzy")
            tracklr_banner = banner.renderText(tracklr_banner).rstrip(" \n")

        banner = f"{tracklr_banner} v{self.__version__}\n"

        self.log.info(banner)
        self.log.info(f"Title: {title}")
        self.log.info(f"Subtitle: {subtitle}")
        self.log.info(f"Configuration: {self.loaded_config_file}")

        return banner

    def loadrc(self, config_file):
        self.config = yaml.safe_load(open(config_file, "r"))
        self.loaded_config_file = config_file

    def configure(self):
        """Tries to load Tracklr configuration from current working directory
        then user config directory and if none found it defaults to internal
        configuration stored in ``Tracklr.__config__``.

        Once config loaded, processes ``calendars`` list from the config and
        handles various configuration options.
        """
        try:
            self.loadrc(self.config_dot_file)
        except FileNotFoundError:
            try:
                self.loadrc(self.config_file)
            except FileNotFoundError:
                try:
                    self.loadrc(os.path.join(self.global_path, self.config_dot_file))
                except FileNotFoundError:
                    try:
                        self.loadrc(os.path.join(self.global_path, self.config_file))
                    except FileNotFoundError:
                        self.config = yaml.safe_load(self.__config__)
                        self.loaded_config_file = "default"

        for cal in self.config["calendars"]:
            try:
                name = cal["name"]
                self.calendars[name] = cal
            except KeyError:
                name = "default"
                self.calendars[name] = {
                    "name": name,
                    "location": cal["location"],
                }
            except TypeError:
                name = "default"
                self.calendars[name] = {"name": name, "location": cal}

    def get_calendar_config(self, calendar):
        """Returns given calendar config or
        raises exception if none found.
        """
        if not calendar:
            calendar = "default"
        calendars = "\n".join([cal for cal in self.calendars])
        if calendar not in self.calendars:
            self.log.error(
                f"calendar {calendar} not found "
                f"in the configured calendars:\n{calendars}"
            )
            raise
        return self.calendars[calendar]

    def get_title(self, calendar, title):
        """Handles title of the provided calendar.

        Title is optional in the configuration so default title is "Tracklr".
        """
        if "dir" in self.calendars[calendar]:
            if not title:
                self.calendars[calendar]["title"] = self.calendars[calendar][
                    "dir"
                ].get("displayname").strip()
        self.title = "Tracklr"
        if "title" in self.calendars[calendar]:
            self.title = self.calendars[calendar]["title"]
        if title:
            self.title = title
        return self.title

    def get_subtitle(self, calendar, subtitle):
        """Handles title of the provided calendar.

        Title is optional in the configuration so default title is
        "Command-line Productivity Toolset".
        """
        self.subtitle = "Command-line Productivity Toolset"
        if "subtitle" in self.calendars[calendar]:
            self.subtitle = self.calendars[calendar]["subtitle"]
        if subtitle:
            self.subtitle = subtitle
        return self.subtitle

    def get_titles(self, calendar, title, subtitle):
        """Returns "title - subtitle" string.
        """
        cal = self.get_calendar_config(calendar)
        title = self.get_title(cal["name"], title)
        subtitle = self.get_subtitle(cal["name"], subtitle)
        return f"{title} - {subtitle}"

    def parse_summary(self, key, summary):
        """Parses given event summary and returns all strings
        that begin with given key found.
        """
        if key is None:
            return []

        def find_matches(summary, pattern):
            if isinstance(summary, str):
                return pattern.findall(summary)
            if isinstance(summary, list):
                return pattern.findall(" ".join(summary))

        # 23g, 1024hPa, 30C, ...
        try:
            pattern = re.compile(r"([0-9\.]+){}".format(key))
            matches = find_matches(summary, pattern)
        except Exception:
            matches = None

        if matches:
            return matches

        # #hastags, $monies, @something, ...
        try:
            pattern = re.compile(r"{}([a-zA-Z0-9_\-\.]+)".format(key))
            return find_matches(summary, pattern)
        except Exception:
            return None

    def set_timezone(self, name):
        """Use this for feeds that use non-standard
        ``X-WR-TIMEZONE`` for timezones, or when a feed needs to apply specific
        timezone.

        TL;DR ``X-WR-TIMEZONE`` is NOT part of RFC 5545.

        For more info see:
        https://blog.jonudell.net/2011/10/17/x-wr-timezone-considered-harmful/
        """
        timezone = self.calendars[name].get("timezone", False)
        if timezone is not False:
            if timezone is True:
                try:
                    tz = pytz.timezone(
                        self.calendars[name]["calendar"].get("X-WR-TIMEZONE")
                    )
                except Exception:
                    tz = pytz.timezone("UTC")
            else:
                tz = pytz.timezone(self.calendars[name].get("timezone"))
        for component in self.calendars[name]["events"]:
            dtstart = component.get("DTSTART")
            dtend = component.get("DTEND")
            dtstamp = component.get("DTSTAMP")
            dtstart.dt = dtstart.dt.astimezone(tz)
            dtend.dt = dtend.dt.astimezone(tz)
            dtstamp.dt = dtstamp.dt.astimezone(tz)

    def get_auth(self, username, password):
        """Returns ``HTTPBasicAuth`` for provided ``username`` and
        ``password``.
        """
        return HTTPBasicAuth(username, password)

    def get_feed(
        self,
        name,
        location,
        username=None,
        password=None,
        title=None,
        subtitle=None,
    ):
        """Loads calendar URL which can use BasicHTTPAuth.
        """
        self.calendars[name]["events"] = []
        try:
            if username and password:
                self.calendars[name]["auth"] = self.get_auth(username, password)
                resp = requests.get(location, auth=self.calendars[name]["auth"])
            else:
                resp = requests.get(location)
            if resp.status_code == 200:
                self.calendars[name]["ics"] = resp.text
                self.calendars[name]["calendar"] = Calendar.from_ical(
                    self.calendars[name]["ics"]
                )
                for event in self.calendars[name]["calendar"].walk("vevent"):
                    self.calendars[name]["events"].append(event)
        except MissingSchema:
            try:
                self.calendars[name]["dir"] = Vdir(os.path.expanduser(location))
                for dir_event in self.calendars[name]["dir"].list():
                    event_ical = Calendar.from_ical(
                        self.calendars[name]["dir"].get(dir_event)
                    )
                    for event in event_ical.walk("vevent"):
                        self.calendars[name]["events"].append(event)
            except IOError:
                self.log.warning(f"No calendar found at {location}")

    def get_calendar(self, calendar):
        """Loads multiple calendars which can use BasicHTTPAuth.
        """
        cal = self.get_calendar_config(calendar)
        if "username" in cal and "password" in cal:
            self.get_feed(
                cal["name"], cal["location"], cal["username"], cal["password"]
            )
        else:
            self.get_feed(cal["name"], cal["location"])

        if cal.get("timezone", False) is not False:
            self.set_timezone(cal["name"])

    def get_event_length(self, event):
        """Calculates length of an event.
        """
        return event["DTEND"].dt - event["DTSTART"].dt

    def get_event_date(self, event, format="%Y-%m-%d"):
        """Returns dates(s) of given event.
        """
        s = event["DTSTART"].dt
        e = event["DTEND"].dt
        if s.year == e.year and s.month == e.month and s.day == e.day:
            return s.strftime(format)
        else:
            return f"{s.strftime(format)} - {e.strftime(format)}"

    def filter_event(self, key, event, date_pattern, include, exclude):
        """Decides whether the event should be included or excluded.
        """
        # abort if there is no summary
        try:
            summary = event["SUMMARY"].lower()
        except KeyError:
            return False
        # Filter by date pattern
        date = self.get_event_date(event)
        if date_pattern is not None and date_pattern not in date:
            return True
        # Filter by given include patterns
        if include is not None:
            for pattern in include:
                if pattern.lower() not in summary:
                    return True
            # Filter includes by key match
            filter_out = False
            matches = self.parse_summary(key, include)
            for t in matches:
                if f"{key}{t}" not in summary:
                    filter_out = True
            if filter_out:
                return True
        # Filter by given exclude patterns
        if exclude is not None:
            for pattern in exclude:
                # first check for direct match
                if pattern.lower() in summary:
                    return True
            # Filter excludes by key match
            filter_out = False
            matches = self.parse_summary(key, exclude)
            for t in matches:
                if f"{key}{t}" in summary:
                    filter_out = True
            if filter_out:
                return True
        return False

    def get_report(self, key, calendar, date_pattern, include, exclude):
        """Generates timesheet report in format:

            date, summary, description, hours
        """
        self.get_calendar(calendar)
        self.report = []
        self.report_html = []
        cal = self.get_calendar_config(calendar)

        for event in cal["events"]:

            if self.filter_event(key, event, date_pattern, include, exclude):
                continue

            try:
                matches_processed = []
                matches_result = ""

                summary = event["SUMMARY"].strip()
                matches = self.parse_summary(key, summary)

                for match in matches:
                    if match.replace(".", "", 1).isdigit():
                        matches_processed.append(float(match))
                    else:
                        matches_processed.append(str(match))

                if len(matches_processed) > 1:
                    matches_result = matches_processed

                if len(matches_processed) == 1:
                    matches_result = [
                        matches_processed[0],
                    ]

            except KeyError:
                summary = ""
                matches_result = []

            try:
                description = event["DESCRIPTION"].strip()
            except KeyError:
                description = ""

            date = self.get_event_date(event)
            lent = self.get_event_length(event)
            if key is not None:
                entry = (
                    date,
                    summary,
                    description,
                    round(lent.total_seconds() / 3600.0, 2),
                    matches_result,
                )
            else:
                entry = (
                    date,
                    summary,
                    description,
                    round(lent.total_seconds() / 3600.0, 2),
                )
            self.report.append(entry)

            entry_html = (
                date,
                str(summary).replace("\n", "<br />"),
                str(description).replace("\n", "<br />"),
                round(lent.total_seconds() / 3600.0, 2),
                matches_result,
            )
            self.report_html.append(entry_html)

            self.total_seconds = self.total_seconds + lent.total_seconds()
            self.total_hours = round(self.total_seconds / 3600.0, 2)
            for matched_item in matches_result:
                if isinstance(matched_item, float):
                    self.total_sum = self.total_sum + matched_item
        self.report = sorted(self.report)
        self.report_html = sorted(self.report_html)
        return self.report

    def get_matches(self, key, calendar, date_pattern, include, exclude):
        """Generates matches report in format:

            match, hours
        """
        self.get_calendar(calendar)
        self.report = []
        cal = self.get_calendar_config(calendar)

        for event in cal["events"]:

            if self.filter_event(key, event, date_pattern, include, exclude):
                continue

            try:
                summary = event["SUMMARY"]
                matches = self.parse_summary(key, summary)
                match_no = len(matches)
                if match_no == 0:
                    matches = ["No_Match"]
                    match_no = 1
                if matches:
                    lent = self.get_event_length(event)
                    for t in matches:
                        if t in self.matches:
                            self.matches[t] += round(
                                (lent.total_seconds() / 3600.0)
                                / float(match_no),
                                2,
                            )
                        else:
                            self.matches[t] = round(
                                (lent.total_seconds() / 3600.0)
                                / float(match_no),
                                2,
                            )
                    self.total_seconds = (
                        self.total_seconds + lent.total_seconds()
                    )
                    self.total_hours = round(self.total_seconds / 3600.0, 2)
            except KeyError:
                self.log.debug("No summary found")

        if self.matches:
            for t in self.matches:
                entry = (t, "{:.1f}".format(self.matches[t]))
                self.report.append(entry)
        else:
            self.log.info("No matches found")

        self.report = sorted(self.report)
        self.report_html = self.report
        return self.report

    def get_base_parser(self, parser):
        """Returns parser with base Tracklr's arguments:

        * ``-k`` ``--kalendar`` specify calendar to use.
          `default` calendar is used otherwise
        * ``-t`` ``--title`` report title,
          or title from the config is used
        * ``-s`` ``--subtitle`` report subtitle,
          or subtitle from the config is used
        """
        parser.add_argument("-k", "--kalendar")
        parser.add_argument("-t", "--title")
        parser.add_argument("-s", "--subtitle")
        return parser

    def get_parser(self, parser):
        """Returns parser with base Tracklr's arguments:

        * ``-k`` ``--kalendar`` specify calendar to use.
          `default` calendar is used otherwise
        * ``-t`` ``--title`` report title,
          or title from the config is used
        * ``-s`` ``--subtitle`` report subtitle,
          or subtitle from the config is used

        And with additional ls/pdf/group arguments:

        * ``-d`` ``--date`` date pattern eg. 2019, 2019-01
        * ``-g`` ``--group`` extracts groups of keywords from events that
          match given group identifier eg.
          -g @   for parsing out targets,
          -g #   for parsing out hastags,
          -g $   for parsing out monies.
        * ``-i`` ``--include`` include patterns. Tags need to be in quotes.
          Eg. -i @Tracklr "#v0.7"
        * ``-x`` ``--exclude`` exclude patterns. Tags need to be in quotes.
          Eg. -x "#hashtag"
        """
        parser = self.get_base_parser(parser)
        parser.add_argument("-d", "--date")
        parser.add_argument("-g", "--group")
        parser.add_argument("-i", "--include", nargs="*")
        parser.add_argument("-x", "--exclude", nargs="*")
        return parser
