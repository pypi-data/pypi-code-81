# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This support module helps to handle date and time objects."""


def date_difference(first, second):
    """
    Calculate the time between two dates and times in seconds.

    first -- The earlier point in time.

    second -- The later point in time.
    """
    d = second - first
    return d.days * 24 * 3600 + d.seconds


def to_days(s):
    """
    Converts seconds into days, hours, minutes, and seconds.

    s -- The time in seconds.
    """
    minutes, seconds = divmod(s, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds


def to_date_string(s):
    """
    Converts seconds into a string of days, hours, minutes, and
    seconds.

    s -- The time in seconds.
    """
    days, hours, minutes, seconds = to_days(s)

    if days == 1:
        days_str = "1 day"
    else:
        days_str = "{} days".format(days)

    if hours == 1:
        hours_str = "1 hour"
    else:
        hours_str = "{} hours".format(hours)

    if minutes == 1:
        minutes_str = "1 minute"
    else:
        minutes_str = "{} minutes".format(minutes)

    if seconds == 1:
        seconds_str = "1 second"
    else:
        seconds_str = "{} seconds".format(seconds)

    return "{}, {}, {}, and {}".format(
        days_str, hours_str, minutes_str, seconds_str
    )
