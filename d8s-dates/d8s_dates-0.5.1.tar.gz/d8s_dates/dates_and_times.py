"""Democritus functions for working with dates and times in Python."""

import datetime
import functools
import re
import time

import dateutil.parser
import maya
import parsedatetime
from d8s_hypothesis import hypothesis_get_strategy_results
from d8s_timezones import pytz_timezone_object
from hypothesis.strategies import dates, datetimes, timedeltas, times

from d8s_dates.dates_and_times_temp_utils import number_zero_pad, string_remove_from_end

DAY_NAMES = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
DAY_ABBREVIATIONS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
MONTH_NAMES = (
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
)
MONTH_ABBREVIATIONS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

STRF_DATA = (
    {'patterns': DAY_ABBREVIATIONS, 'replacement': '%a'},
    {'patterns': DAY_NAMES, 'replacement': '%A'},
    {'patterns': MONTH_ABBREVIATIONS, 'replacement': '%b'},
    {'patterns': MONTH_NAMES, 'replacement': '%B'},
    {'regex': r'[0123]?[0-9]/%b/[0-9]{4}', 'replacement': '%d/%b/%Y'},
    {'regex': r'[0-9]?[0-9]:[0-9]{2}:[0-9]{2}', 'replacement': '%X'},
    {'regex': r'[01]?[0-9]/[0123]?[0-9]/[0-9]{3,4}', 'replacement': '%-m/%-d/%Y'},
    {'regex': r'[01]?[0-9]/[0123]?[0-9]/[0-9]{2}', 'replacement': '%x'},
    {'regex': r'[0-9]{4}-[01]?[0-9]-[0123]?[0-9]', 'replacement': '%Y-%-m-%-d'},
    {'regex': r'\*[0-9]{3,6}', 'replacement': '*%f'},
    {'regex': r'\.[0-9]{3,6}', 'replacement': '.%f'},
    {'regex': r'\,[0-9]{3,6}', 'replacement': ',%f'},
    {'patterns': [f'-{number_zero_pad(i, 4)}' for i in range(1200, -1, -100)], 'replacement': '%z'},
    {'patterns': [f'+{number_zero_pad(i, 4)}' for i in range(1200, -1, -100)], 'replacement': '%z'},
    {'patterns': [str(i) for i in range(3000, 1600, -1)], 'replacement': '%Y'},
    {'patterns': [number_zero_pad(i, 2) for i in range(1, 31)], 'replacement': '%d'},
    {'patterns': [str(i) for i in range(31, 0, -1)], 'replacement': '%-d'},
    {'patterns': [number_zero_pad(i, 2) for i in range(0, 12)], 'replacement': '%m'},
    {'patterns': [str(i) for i in range(12, 0, -1)], 'replacement': '%-m'},
    {'patterns': [number_zero_pad(i, 2) for i in range(99, 0, -1)], 'replacement': '%y'},
    {'patterns': ["AM", "PM"], 'replacement': '%p'},
)


def date_string_to_strftime_format(date_string):
    """Predict the strftime format from the given date_string."""
    for data in STRF_DATA:
        for pattern in data.get('patterns', []):
            if pattern in date_string:
                date_string = date_string.replace(pattern, data['replacement'])
                break
        else:
            if data.get('regex'):
                date_string = re.sub(data['regex'], data['replacement'], date_string)
                # matches = find()
                # if any(matches):
                #     date_string = date_string.replace(matches[0], data['replacement'])

    return date_string


def date_parse(date, *, convert_to_current_timezone: bool = False):
    """Parse the given date (can parse dates in most formats) (returns a datetime object)."""
    if isinstance(date, (datetime.date, datetime.time, datetime.datetime)):
        return date

    # try to parse the date as an epoch datetime...
    # we start with epoch datetime as it is the most discrete form of a date
    try:
        date = epoch_to_date(date)
    except ValueError:
        # try to parse the given date with the dateutil module
        try:
            date = _dateutil_parser_parse(date)
        # if the given date could not be parsed by the dateutil module, try to parse the date using parsedatetime
        except ValueError as e:
            parsed_time_struct, parse_status = _parsedatetime_parse(date)

            # convert the parsed_time_struct to a datetime object and return it
            if parse_status > 0:
                date = time_struct_to_datetime(parsed_time_struct)
            else:
                message = f'Unable to convert the date "{date}" into a standard date format.'
                raise RuntimeError(message) from e

    if convert_to_current_timezone:
        date = date_make_timezone_aware(date)

    return date


def date_now(*, convert_to_current_timezone: bool = False, utc: bool = False):
    """Get the current date.

    If convert_to_current_timezone is True, convert the date to the current timezone.
    If utc is True, convert the date to UTC.
    """
    now = datetime.datetime.now()

    if convert_to_current_timezone and utc:
        raise ValueError("Only one input parameter from utc and convert_to_current_timezone can be true.")

    if convert_to_current_timezone:
        now = date_make_timezone_aware(now)

    if utc:
        now = date_to_utc(now)

    return now


def date_parse_first_argument(func):
    """."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        date_arg = args[0]
        other_args = args[1:]

        parsed_date_arg = date_parse(date_arg)
        return func(parsed_date_arg, *other_args, **kwargs)

    return wrapper


@date_parse_first_argument
def date_2_string(date, date_format_string: str):
    """."""
    formatted_date_string = date.strftime(date_format_string)
    return formatted_date_string


@date_parse_first_argument
def date_hour(date):
    """Find the hour from the given date."""
    return date.hour


@date_parse_first_argument
def date_minute(date):
    """Find the minute from the given date."""
    return date.minute


@date_parse_first_argument
def date_second(date):
    """Find the second from the given date."""
    return date.second


@date_parse_first_argument
def date_day(date):
    """Find the day of the month from the given date."""
    return date_day_of_month(date)


@date_parse_first_argument
def date_day_of_month(date):
    """Find the day of the month from the given date."""
    return date.day


@date_parse_first_argument
def date_month(date):
    """Find the month from the given date."""
    return date.month


@date_parse_first_argument
def date_year(date):
    """Find the year from the given date."""
    return date.year


@date_parse_first_argument
def date_convert_to_timezone(date, timezone_string):
    """Convert the given date to the given timezone_string.

    This will actually **convert** time given date; it will change the hour/day of the date to the given timezone).
    """
    # if the given date does not have a timezone, use the system's timezone
    if date.tzinfo is None:
        date = date_make_timezone_aware(date)

    timezone_object = pytz_timezone_object(timezone_string)
    converted_date = date.astimezone(timezone_object)
    return converted_date


def date_make_timezone_aware(datetime_object, timezone_string=None):
    """Make the given datetime_object timezone aware.

    This function does NOT convert the datetime_object.
    It will never change the hour/day or any value of the datetime...
      it will simply make the given datetime timezone aware.
    """
    if timezone_string:
        # make the date timezone aware using the given timezone_string
        timezone_object = pytz_timezone_object(timezone_string)
        timezone_aware_datetime_object = timezone_object.localize(datetime_object)
    else:
        # make the date timezone aware using the timezone of the current system
        timezone_aware_datetime_object = datetime_object.astimezone()

    return timezone_aware_datetime_object


def time_delta_examples(n=10, *, time_deltas_as_strings: bool = True):
    """Return n time deltas."""
    time_delta_objects = hypothesis_get_strategy_results(timedeltas, n=n)
    if time_deltas_as_strings:
        return [str(time_delta) for time_delta in time_delta_objects]
    else:
        return time_delta_objects


def time_examples(n=10, *, times_as_strings: bool = True):
    """Return n times."""
    time_objects = hypothesis_get_strategy_results(times, n=n)
    if times_as_strings:
        return [str(time) for time in time_objects]
    else:
        return time_objects


def date_examples(n=10, *, dates_as_strings: bool = True, date_string_format: str = None):
    """Return n dates."""
    date_objects = hypothesis_get_strategy_results(dates, n=n)
    if dates_as_strings:
        if date_string_format is None:
            return [str(date) for date in date_objects]
        else:
            return [date_2_string(date, date_string_format) for date in date_objects]
    else:
        return date_objects


def datetime_examples(n=10, *, datetimes_as_strings: bool = True, datetime_string_format: str = None):
    """Return n datetimes."""
    datetime_objects = hypothesis_get_strategy_results(datetimes, n=n)
    if datetimes_as_strings:
        if datetime_string_format is None:
            return [str(datetime) for datetime in datetime_objects]
        else:
            return [date_2_string(datetime, datetime_string_format) for datetime in datetime_objects]
    else:
        return datetime_objects


def time_struct_to_datetime(struct_time_object):
    """Convert a python time.struct_time object into a datetime object."""
    return datetime.datetime(*struct_time_object[:6])


def _parsedatetime_parse(date_string):
    """Parse the given date_string using the parsedatetime module."""
    # for more details on how the parsedatetime.Calendar.parse function works, see:
    # https://github.com/bear/parsedatetime/blob/830775dc5e36395622b41f12317f5e10c303d3a2/parsedatetime/__init__.py#L1779
    cal = parsedatetime.Calendar()
    parsed_date = cal.parse(date_string)
    return parsed_date


def _dateutil_parser_parse(date_string):
    """Parse the given date_string using the dateutil.parser module."""
    parsed_date = dateutil.parser.parse(date_string)
    return parsed_date


def _maya_time_parse(date_object, *, convert_to_utc: bool = True):
    """Parse the given date_object using maya (see https://github.com/timofurrer/maya).

    By default, the given date_object is converted to UTC because maya will assume that any given date is in UTC.
    """
    if convert_to_utc:
        # convert the given date to UTC (this is necessary b/c maya will assume that the given date is in UTC)
        date = date_to_utc(date_object)

    maya_date = maya.parse(date)
    return maya_date


def date_read(date_string, *, convert_to_current_timezone: bool = False):
    """Read the given date (if possible)."""
    return date_parse(date_string, convert_to_current_timezone=convert_to_current_timezone)


def epoch_time_now():
    """Get the current epoch time."""
    return int(time.time())


def is_date(possible_date_string):
    """Determine if the given possible_date_string can be processed as a date."""
    try:
        date_parse(possible_date_string)
    except Exception:  # pylint: disable=broad-except
        return False
    else:
        return True


def time_now():
    """Return the current, epoch time."""
    return time.time()


@date_parse_first_argument
def time_since(date):
    """Return a time of the time since the given date."""
    now = date_now()
    return now - date


@date_parse_first_argument
def time_until(date):
    """Return an English description of the time since the given date."""
    now = date_now()
    return date - now


@date_parse_first_argument
def time_since_slang(date):
    """Return an English description of the time since the given date."""
    maya_date = _maya_time_parse(date)
    slang_time = maya_date.slang_time()
    return slang_time


@date_parse_first_argument
def time_until_slang(date):
    """Return an English description of the time until the given date."""
    maya_date = _maya_time_parse(date)
    slang_time = maya_date.slang_time()
    return slang_time


@date_parse_first_argument
def date_to_utc(date):
    """Convert the given date to UTC. Assume that the given date is in the system's timezone and convert it to UTC."""
    utc_date = date_convert_to_timezone(date, 'utc')
    return utc_date


def time_after(time_a, time_b=None) -> bool:
    """Check if one time is before the other."""
    if time_b is None:
        time_b = time_now()

    # make sure both times are floats
    time_a = float(date_to_epoch(time_a))
    time_b = float(date_to_epoch(time_b))
    return time_a > time_b


def time_before(time_a, time_b=None) -> bool:
    """Check if one time is before the other."""
    if time_b is None:
        time_b = time_now()

    # make sure both times are floats
    time_a = float(date_to_epoch(time_a))
    time_b = float(date_to_epoch(time_b))
    return time_a < time_b


@date_parse_first_argument
def date_in_future(date) -> bool:
    """Return whether or not the given date is in the future."""
    is_in_the_future = time_after(date)
    return is_in_the_future


def time_is() -> str:
    """Time and money spent in helping men to do more for themselves is far better than mere giving. -Henry Ford"""
    return '$'


@date_parse_first_argument
def date_to_iso(date, *, timezone_is_utc: bool = False, use_trailing_z: bool = False):
    """Return the ISO 8601 version of the given date as a string (see https://en.wikipedia.org/wiki/ISO_8601)."""
    if timezone_is_utc:
        # replace any timezones on the date with UTC - this is not a conversion - it is a hard-replace...
        # if there is a timezone on the given date, it will NOT be *converted* to UTC...
        # the time will remain the same, but the timezone will change to UTC
        date = date.replace(tzinfo=datetime.timezone.utc)

    iso_format_date = date.isoformat()

    if use_trailing_z and iso_format_date.endswith('+00:00'):
        # remove the timezone from the end
        iso_format_date = string_remove_from_end(iso_format_date, '+00:00')
        # add a 'Z'
        iso_format_date = iso_format_date + 'Z'

    return iso_format_date


def epoch_time_standardization(epoch_time):
    """Convert the given epoch time to an epoch time in seconds."""
    epoch_time_string = str(epoch_time)
    # if the given epoch time appears to include milliseconds (or some other level of precision)...
    # and does not have a decimal in it, add a decimal point
    if len(epoch_time_string) > 10 and '.' not in epoch_time_string:
        epoch_time = f'{epoch_time_string[:10]}.{epoch_time_string[10:]}'
    return epoch_time


def epoch_to_date(epoch_time):
    """Convert the epoch_time into a datetime."""
    epoch_time = float(epoch_time_standardization(epoch_time))
    return datetime.datetime.fromtimestamp(epoch_time)


@date_parse_first_argument
def date_day_of_week(date):
    """Return the day of the week on which the given date occurred."""
    day_of_week = date.strftime('%A')
    return day_of_week


@date_parse_first_argument
def date_week_of_year(date, *, sunday_is_first_day_of_week: bool = False):
    """Find the week of the year for the given date. If no date is given, return the week of the current date."""
    if sunday_is_first_day_of_week:
        return date.strftime("%U")
    else:
        return date.strftime("%V")


@date_parse_first_argument
def date_to_epoch(date):
    """Convert a datetime stamp to epoch time."""
    epoch_time = date.strftime('%s')
    return int(epoch_time)


def chrome_timestamp_to_epoch(chrome_timestamp):
    """Convert the given Chrome timestamp to epoch time.

    For more information, see: https://stackoverflow.com/questions/20458406/what-is-the-format-of-chromes-timestamps.
    """
    return (chrome_timestamp / 1000000) - 11644473600


def time_waste(n=3):
    """If time be of all things the most precious, wasting time must be the greatest prodigality. -Benjamin Franklin"""
    time.sleep(n)
    message = f'I just wasted {n} seconds of your life.'
    print(message)


def time_as_float(time_string: str) -> float:
    """converts a given HH:MM time string to float"""
    try:
        hours, minutes = list(map(int, time_string.split(":")))  # parse given time string
    except ValueError as e:
        message = f"Invalid time string, ensure that the argument is in HH:MM format. Provided value: {time_string}"
        raise ValueError(message) from e

    if hours > 23 or minutes > 59:
        message = f"Invalid time string, should be between 00:00 and 23:59. Provided value: {time_string}"
        raise ValueError(message)

    return hours + (minutes / 60)
