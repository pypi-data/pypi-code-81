from datetime import datetime


def invert_dates(dates_list, delimiter="/"):
    """
    Returns dates of type dd-mmy-yyy into yyyymmdd

    :param dates_list: List of dates to invert, a string of a date to invert, or a datetime to invert
    :type dates_list: list[str] | str | datetime

    :param delimiter: The delimiter to split the string into [dd, mm, yyyy] if date is a str
    :type delimiter: str

    :return: list of inverted dates, or a string of an inverted date
    :rtype: list[str] | str
    """

    if isinstance(dates_list, str):
        day, month, year = [time.zfill(2) for time in dates_list.split(delimiter)]
        return year + month + day

    elif isinstance(dates_list, (list, tuple)):
        split_dates = [[time.zfill(2) for time in date.split(delimiter)] for date in dates_list]
        return [year + month + day for day, month, year in split_dates]

    elif isinstance(dates_list, datetime):
        return str(dates_list.year) + str(dates_list.month).zfill(2) + str(dates_list.day).zfill(2)

    else:
        raise TypeError(f"invert_dates expects a str, list, or tuple yet found {type(dates_list)}")


def restore_dates(inverted_dates):
    """
    This restores dates back to a datetime date from yyyymmdd.
    """
    if isinstance(inverted_dates, (str, int)):
        inverted_dates = str(inverted_dates)
        year, month, day = int(inverted_dates[:4]), int(inverted_dates[4:6]), int(inverted_dates[6:])
        return datetime(year, month, day)

    elif isinstance(inverted_dates, (list, tuple)):
        return [datetime(int(str(date)[:4]), int(str(date)[4:6]), int(str(date)[6:])) for date in inverted_dates]

    else:
        raise TypeError(f"restores_dates expects a str, list or tuple yet found {type(inverted_dates)}")


def terminal_time():
    """
    A way to remember when you initialised a cell by return the current hour and minute as a string
    """
    return f"{datetime.now().time().hour}:{datetime.now().time().minute}"
