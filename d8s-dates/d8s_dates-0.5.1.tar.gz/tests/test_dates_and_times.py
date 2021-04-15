import datetime
import time

import pytest

from d8s_dates import (
    chrome_timestamp_to_epoch,
    date_2_string,
    date_convert_to_timezone,
    date_day,
    date_day_of_month,
    date_day_of_week,
    date_examples,
    date_hour,
    date_in_future,
    date_make_timezone_aware,
    date_minute,
    date_month,
    date_now,
    date_parse,
    date_parse_first_argument,
    date_second,
    date_string_to_strftime_format,
    date_to_epoch,
    date_to_iso,
    date_week_of_year,
    date_year,
    datetime_examples,
    epoch_time_now,
    epoch_time_standardization,
    epoch_to_date,
    is_date,
    time_after,
    time_as_float,
    time_before,
    time_delta_examples,
    time_examples,
    time_is,
    time_now,
    time_since,
    time_since_slang,
    time_until,
    time_until_slang,
    time_waste,
)

"""NOTE: WE ASSUME THAT THE SYSTEM RUNNING THE TESTS IS SET TO THE UTC TIMEZONE (BECAUSE THESE TESTS ARE RUNNING IN DOCKER (OR A CI SYSTEM))."""


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 12),
    ],
)
def test_date_hour_1(date, expected_output):
    assert date_hour(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 30),
    ],
)
def test_date_minute_1(date, expected_output):
    assert date_minute(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 22),
    ],
)
def test_date_second_1(date, expected_output):
    assert date_second(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 13),
    ],
)
def test_date_day_1(date, expected_output):
    assert date_day(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 13),
    ],
)
def test_date_day_of_month_1(date, expected_output):
    assert date_day_of_month(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 1),
    ],
)
def test_date_month_1(date, expected_output):
    assert date_month(date) == expected_output


@pytest.mark.parametrize(
    "date,expected_output",
    [
        ('2022-01-13 12:30:22', 2022),
    ],
)
def test_date_year_1(date, expected_output):
    assert date_year(date) == expected_output


def test_time_until_1():
    result = time_until('2222-02-22')
    assert result.days < 73522


def test_time_since_1():
    result = time_since('2002-01-22')
    assert result.days > 6860


def test_is_date_1():
    assert is_date('2 days ago')
    assert is_date('1970-01-01 12:34:42')
    assert not is_date('foo bar')


def test_time_delta_examples_1():
    result = time_delta_examples()
    assert len(result) == 10
    assert isinstance(result[0], str)

    result = time_delta_examples(n=100)
    assert len(result) == 100
    assert isinstance(result[0], str)

    result = time_delta_examples(time_deltas_as_strings=False)
    assert len(result) == 10
    assert not isinstance(result[0], str)
    assert isinstance(result[0], datetime.timedelta)


def test_date_examples_1():
    date_format = '%-m/%-d/%Y'
    results = date_examples(date_string_format=date_format)
    for i in results:
        inferred_format = date_string_to_strftime_format(i)
        # sometimes a date format like '%-m/%-d/%Y' may be interpretted as '%x' (e.g. 1/1/78)
        assert inferred_format == date_format or inferred_format == '%x'


def test_datetime_examples_1():
    datetime_format = '%-m/%-d/%Y'
    results = datetime_examples(datetime_string_format=datetime_format)
    for i in results:
        inferred_format = date_string_to_strftime_format(i)
        # sometimes a date format like '%-m/%-d/%Y' may be interpretted as '%x' (e.g. 1/1/78)
        assert inferred_format == datetime_format or inferred_format == '%x'


def test_date_2_string_1():
    date_string = 'Fri, 20 Nov 1998 20:04:56 -0500'
    results = date_2_string(date_string, '%a, %d %b %Y %X %z')
    assert results == date_string

    results = date_2_string(date_string, '%m/%d/%Y')
    assert results == '11/20/1998'


def test_date_string_to_strftime_format_1():
    test_data = {
        # '2018-08-20"T"13:20:10*633+0000': '%Y-%m-%-d"T"%X*%f%z',
        '2017 Mar 03 05:12:41.211 PDT': '%Y %b %d %X.%f PDT',
        'Jan 21 18:20:11 +0000 2017': '%b %d %X %z %Y',
        '19/Apr/2017:06:36:15 -0700': '%d/%b/%Y:%X %z',
        'Dec 2, 2017 2:39:58 AM': '%b %-d, %Y %X %p',
        'Jun 09 2018 15:28:14': '%b %d %Y %X',
        'Apr 20 00:00:35 2010': '%b %d %X %Y',
        'Sep 28 19:00:00 +0000': '%b %d %X %z',
        'Mar 16 08:12:04': '%b %d %X',
        # '2017-10-14T22:11:20+0000': '%Y-%m-%-dT%X%z',
        # '2017-08-19 12:17:55 -0400': '%Y-%m-%-d %X %z',
        # '2017-08-19 12:17:55-0400': '%Y-%m-%-d %X%z',
        # '2017-06-26 02:31:29,573': '%Y-%m-%-d %X,%f',
        '2017/04/12*19:37:50': '%d%x*%X',
        # '2018 Apr 13 22:08:13.211*PDT': '%Y %b %-d %X.%f*PDT',
        '2017 Mar 10 01:44:20.392': '%Y %b %d %X.%f',
        # '2017-03-10 14:30:12,655+0000': '%Y-%m-%-d %X,%f%z',
        # '2018-02-27 15:35:20.311': '%Y-%m-%-d %X.%f',
        # '2017-03-12 13:11:34.222-0700': '%Y-%m-%-d %X.%f%z',
        # '2017-07-22"T"16:28:55.444': '%Y-%m-%-d"T"%X.%f',
        # '2017-09-08"T"03:13:10': '%Y-%m-%-d"T"%X',
        # '2017-03-12"T"17:56:22-0700': '%Y-%m-%-d"T"%X%z',
        '2017-11-22"T"10:10:15.455': '%Y-%-m-%-d"T"%X.%f',
        # '2017-02-11"T"18:31:44': '%Y-%m-%-d"T"%X',
        # '2017-10-30*02:47:33:899': '%Y-%-m-%-d*%X:%-d%-m%-m',
        # '2017-07-04*13:23:55': '%Y-%m-%-d*%X',
        # '11-02-11 16:47:35,985 +0000': '%-m-%d-%y %X,%f %z',
        '10-06-26 02:31:29,573': '%m-%d-%-d %X,%f',
        '10-04-19 12:00:17': '%m-%d-%-d %X',
        '06/01/22 04:11:05': '%x %X',
        # '150423 11:42:35': '%-d%-m%d%-d %X',
        '20150423 11:42:35.173': '%Y%d%-d %X.%f',
        '08/10/11*13:33:56': '%x*%X',
        '11/22/2017*05:13:11': '%-m/%-d/%Y*%X',
        # '05/09/2017*08:22:14*612': '%m/%-d/%Y*%X*%f',
        '04/23/17 04:34:22 +0000': '%x %X %z',
        '10/03/2017 07:29:46 -0700': '%-m/%-d/%Y %X %z',
        '11:42:35': '%X',
        '11:42:35.173': '%X.%f',
        '11:42:35,173': '%X,%f',
        # '23/Apr 11:42:35,173': '%-d/%b %X,%f',
        # '23/Apr/2017:11:42:35': '%-d/%b/%d%X:%-d%-m',
        '23/Apr/2017 11:42:35': '%d/%b/%Y %X',
        '23-Apr-2017 11:42:35': '%d-%b-%Y %X',
        '23-Apr-2017 11:42:35.883': '%d-%b-%Y %X.%f',
        '23 Apr 2017 11:42:35': '%d %b %Y %X',
        # '23 Apr 2017 10:32:35*311': '%-d %b %Y %X*%f',
        '0423_11:42:35': '%d%-d_%X',
        '0423_11:42:35.883': '%d%-d_%X.%f',
        '8/5/2011 3:31:18 AM:234': '%-m/%-d/%Y %X %p:%d%-d',
        '9/28/2011 2:23:15 PM': '%-m/%-d/%Y %X %p',
    }

    failure_count = 0

    for k, v in test_data.items():
        try:
            result = date_string_to_strftime_format(k)
            assert result == v
        except AssertionError:
            print(f'input:\t\t{k}\nexpected:\t{v}\nactual:\t\t{result}\n\n')
            failure_count += 1

    if failure_count > 0:
        raise AssertionError(f'{failure_count} failures')


def test_time_waste_1():
    a = time_now()
    time_waste()
    b = time_now()
    assert 3 < b - a < 4.5

    n = 1
    a = time_now()
    time_waste(n=n)
    b = time_now()
    assert n < b - a < n + 1


def test_time_is_1():
    assert time_is() == '$'


def test_epoch_time_now_1():
    epoch_now = epoch_time_now()
    standardized_date = epoch_to_date(epoch_now)
    now = date_now()
    assert standardized_date.year == now.year
    assert standardized_date.month == now.month
    assert standardized_date.day == now.day


def test_chrome_timestamp_to_epoch_1():
    # this is based on the example here: https://stackoverflow.com/a/26118615
    assert chrome_timestamp_to_epoch(13029358986442901) == 1384885386.4429016
    standardized_date = epoch_to_date(1384885386.4429016)
    assert standardized_date.year == 2013
    assert standardized_date.month == 11
    assert standardized_date.day == 19


def test_date_day_of_week_1():
    assert date_day_of_week('January 1, 2019') == 'Tuesday'
    assert date_day_of_week('January 11, 2010') == 'Monday'


def test_date_in_future_1():
    assert date_in_future('2200/01/13')
    assert not date_in_future('2000/01/13')
    assert not date_in_future('1990/01/13')


def test_date_convert_to_timezone_1():
    now = date_now(utc=True)
    assert now.tzinfo is not None
    utc_date = date_convert_to_timezone(now, 'utc')
    # make sure the hour is not changed when making the date timezone aware
    assert utc_date.hour == now.hour
    assert utc_date.tzinfo is not None

    now = date_now()
    pst_timezone_date = date_convert_to_timezone(now, 'America/Los_Angeles')
    # make sure the hour is changed when making the date timezone aware
    assert pst_timezone_date.hour != now.hour
    assert pst_timezone_date.tzinfo is not None


def test_date_make_timezone_aware_1():
    now = date_now()
    assert now.tzinfo is None
    timezone_aware_datetime = date_make_timezone_aware(now)
    # make sure the hour is not changed when making the date timezone aware
    assert timezone_aware_datetime.hour == now.hour
    assert timezone_aware_datetime.tzinfo is not None

    utc_timezone_date = date_make_timezone_aware(now, timezone_string='utc')
    assert utc_timezone_date.hour == now.hour

    pst_timezone_date = date_make_timezone_aware(now, timezone_string='America/Los_Angeles')
    assert pst_timezone_date.hour == now.hour


def test_date_to_iso_1():
    iso_date = date_to_iso('2018/01/13')
    assert iso_date == '2018-01-13T00:00:00'

    iso_date = date_to_iso('2018/01/13', timezone_is_utc=True)
    assert iso_date == '2018-01-13T00:00:00+00:00'

    iso_date = date_to_iso('2018/01/13', timezone_is_utc=True, use_trailing_z=True)
    assert iso_date == '2018-01-13T00:00:00Z'

    # make sure that setting the use_trailing_z argument doesn't affect dates that are not UTC
    iso_date = date_to_iso('2018/01/13', use_trailing_z=True)
    assert iso_date == '2018-01-13T00:00:00'


def test_time_since_slang_1():
    since = time_since_slang('2018/01/13')
    assert since == '3 years ago'

    since = time_since_slang('2000/08/30')
    print(since)
    assert 'years ago' in since

    since = time_since_slang('11 hours from now')
    assert since == 'in 10 hours'


def test_time_until_slang_1():
    since = time_until_slang('11 hours from now')
    assert since == 'in 10 hours'


def test_epoch_to_date_1():
    standardized_date = epoch_to_date('1564765879')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = epoch_to_date('1564765879000')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = epoch_to_date('1564765879000000')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = epoch_to_date('1564765879.314159')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2


def test_date_parse_1():
    standardized_date = date_parse('2019/12/13')
    assert standardized_date.year == 2019
    assert standardized_date.month == 12
    assert standardized_date.day == 13

    # find yesterday's date using the date standardization function
    standardized_date = date_parse('yesterday')
    # find yesterday's date using another function so that we can compare the two
    yesterday = date_now() - datetime.timedelta(days=1)
    assert standardized_date.year == yesterday.year
    assert standardized_date.month == yesterday.month
    assert standardized_date.day == yesterday.day

    # find a previous date using the date standardization function
    standardized_date = date_parse('3 days ago')
    # find a previous date using another function so that we can compare the two
    past_date = date_now() - datetime.timedelta(days=3)
    assert standardized_date.year == past_date.year
    assert standardized_date.month == past_date.month
    assert standardized_date.day == past_date.day

    # find a future date using the date standardization function
    standardized_date = date_parse('3 days from now')
    # find a previous date using another function so that we can compare the two
    future_date = date_now() + datetime.timedelta(days=3)
    assert standardized_date.year == future_date.year
    assert standardized_date.month == future_date.month
    assert standardized_date.day == future_date.day

    standardized_date = date_parse('Sat Oct 11 17:13:46 -1 2003')
    assert standardized_date.year == 2003
    assert standardized_date.month == 10
    assert standardized_date.day == 11
    assert standardized_date.hour == 17
    assert standardized_date.minute == 13

    # test the same date as above, but convert the time to the current timezone (which is assumed to be UTC)
    standardized_date = date_parse('Sat Oct 11 17:13:46 -1 2003', convert_to_current_timezone=True)
    assert standardized_date.hour == 18

    standardized_date = date_parse('Sat, Oct 11, 2003')
    assert standardized_date.year == 2003
    assert standardized_date.month == 10
    assert standardized_date.day == 11

    standardized_date = date_parse('1564765879')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = date_parse('1564765879000')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = date_parse('1564765879000000')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = date_parse('last friday')
    today = date_now()
    diff = today - standardized_date
    assert diff.days <= 7

    standardized_date = date_parse('2018-11-08T16:52:42Z')
    assert standardized_date.year == 2018
    assert standardized_date.month == 11
    assert standardized_date.day == 8

    standardized_date = date_parse('2019 12 25')
    assert standardized_date.year == 2019
    assert standardized_date.month == 12
    assert standardized_date.day == 25

    standardized_date = date_parse('1564765879.3141592')
    assert standardized_date.year == 2019
    assert standardized_date.month == 8
    assert standardized_date.day == 2

    standardized_date = date_parse('2018-11-08T22:52:42-05:00')
    assert standardized_date.year == 2018
    assert standardized_date.month == 11
    assert standardized_date.day == 8

    # this is the same date as above, but convert the time to the current timezone (which is assumed to be UTC)
    standardized_date = date_parse('2018-11-08T22:52:42-05:00', convert_to_current_timezone=True)
    # the day should be the next day UTC
    assert standardized_date.day == 9

    standardized_date = date_parse('2018-01-13T11:11:11Z')
    assert standardized_date.year == 2018
    assert standardized_date.month == 1
    assert standardized_date.day == 13
    assert standardized_date.hour == 11
    assert standardized_date.minute == 11
    assert str(standardized_date) == '2018-01-13 11:11:11+00:00'


def test_time_examples_1():
    result = time_examples(n=1, times_as_strings=False)
    assert len(result) == 1
    assert isinstance(result[0], datetime.time)


def test_date_parse_2_fuzzing():
    """Create a number of test dates/datetimes and run them through the standardization function to make sure it doesn't crash when given odd values."""
    # test a number of times
    example_dates = time_examples(n=100)
    for i in example_dates:
        try:
            standardized_date = date_parse(i)
        except ValueError:
            print(f'Unable to convert the date: {i}')
            raise
        assert standardized_date

    # test a number of datetimes
    example_datetimes = datetime_examples(n=100)
    for i in example_datetimes:
        try:
            standardized_date = date_parse(i)
        except ValueError:
            print(f'Unable to convert the date: {i}')
            raise
        assert standardized_date

    # test a number of dates
    example_dates = date_examples(n=100)
    for i in example_dates:
        try:
            standardized_date = date_parse(i)
        except ValueError:
            print(f'Unable to convert the date: {i}')
            raise
        assert standardized_date


def test_epoch_time_standardization_1():
    assert epoch_time_standardization('1563478212873') == '1563478212.873'
    assert epoch_time_standardization(1563478212873) == '1563478212.873'
    assert epoch_time_standardization('1563478212873000') == '1563478212.873000'
    assert epoch_time_standardization(1563478212873000) == '1563478212.873000'


def test_date_week_of_year_1():
    import datetime

    d = datetime.date(2010, 6, 16)
    assert date_week_of_year(d) == '24'
    d = datetime.date(2019, 6, 29)
    assert date_week_of_year(d) == '26'
    assert date_week_of_year(d, sunday_is_first_day_of_week=True) == '25'


def test_date_now_1():
    a = date_now()
    b = date_now()
    assert a < b


def test_date_now_convert_timezone():
    a = date_now()
    assert '+00:00' not in str(a)

    a = date_now(convert_to_current_timezone=True)
    assert '+00:00' in str(a)


def test_time_after_1():
    a = date_now()
    time.sleep(1)
    b = date_now()
    time.sleep(1)
    assert time_after(b, a)
    assert not time_after(a, b)
    assert not time_after(a)
    assert not time_after(b)


def test_time_before_1():
    a = date_now()
    time.sleep(1)
    b = date_now()
    time.sleep(1)
    assert time_before(a, b)
    assert not time_before(b, a)
    assert time_before(a)
    assert time_before(b)


def test_time_now_1():
    a = time_now()
    time.sleep(1)
    b = time_now()
    time.sleep(1)
    assert time_before(a, b)
    assert time_after(b, a)


def test_date_to_epoch_1():
    assert isinstance(date_to_epoch(date_now()), int)
    assert float(date_to_epoch(date_now())) > 1540000000
    assert date_to_epoch('January 1, 2010') < date_to_epoch('January 1, 2011')


@date_parse_first_argument
def date_parse_first_argument_test_func(date):
    return date


def test_date_parse_first_argument_1():
    import datetime

    date = date_parse_first_argument_test_func('3 days ago')
    assert isinstance(date, datetime.datetime)


def test_time_as_float_1():
    assert time_as_float("12:00") == 12.0
    assert time_as_float("12:10") == 12.166666666666666
    assert time_as_float("12:15") == 12.25
    assert time_as_float("12:30") == 12.5
    assert time_as_float("12:45") == 12.75
