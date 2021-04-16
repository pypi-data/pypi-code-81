# -*- coding: utf-8 -*-
import re
from typing import List, Optional

import pendulum as p
import typer

app = typer.Typer(
    name="dates",
    add_completion=False,
    help="This is a cli that outputs dates.",
)


def is_weekend(day: Optional[str] = None) -> str:
    """
    Checks if the given date is a weekend.
    """
    if day is None:
        d = p.now(tz="US/Eastern")
        if d.weekday() > 4:
            return f"Yes! It's a {d.format('dddd')}."
        else:
            return f"No, it's {d.format('dddd')}."
    else:
        d = p.parse(day, strict=False, tz="US/Eastern")
        if d.weekday() > 4:
            return f"Yes! It's a {d.format('dddd')}."
        else:
            return f"No, it's {d.format('dddd')}."


def is_weekday(day: Optional[str] = None) -> str:
    if day is None:
        d = p.now(tz="US/Eastern")
        if d.weekday() <= 4:
            return f"It's a weekday. It's {d.format('dddd')}."
        else:
            return f"It's not a weekday. It's {d.format('dddd')}."
    else:
        d = p.parse(day, strict=False, tz="US/Eastern")
        if d.weekday() <= 4:
            return f"It's a weekday. It's a {d.format('dddd')}."
        else:
            return f"It's not a weekday. It's {d.format('dddd')}."


def days_diff(start: p.datetime, end: p.datetime):
    """
    Calculates the day difference between two dates.
    """
    st = p.parse(start, strict=False, tz="US/Eastern")
    en = p.parse(end, strict=False, tz="US/Eastern")
    return (en - st).days


def add_days(n, d: Optional[p.datetime] = None) -> str:
    """
    Calculates the date of n days from the given date.

    if no date is given, today's date will be used.

    """
    if d is None:
        day = p.now(tz="US/Eastern")
        days = day + p.duration(n)
        return days.to_day_datetime_string()
    else:
        day = p.parse(d, strict=False, tz="US/Eastern")
        days = day + p.duration(n)
        return days.to_day_datetime_string()


def days_from_now(n: int):
    """
    Calculates the date of n days from today.
    """
    now = p.now(tz="US/Eastern") + p.duration(n)
    return now.to_day_datetime_string()


def prange(start_date: str, end_date: str) -> List[str]:
    if (
        re.match(r"\d{1,2}-\d{1,2}-\d{1,2}", start_date) is None
        or re.match(r"\d{1,2}-\d{1,2}-\d{1,2}", end_date) is None
    ):
        raise Exception(
            "Date format must be MM-DD-YY e.g. 03-11-21.",
        )

    start, end = (
        p.parse(start_date, strict=False, tz="US/Eastern"),
        p.parse(end_date, strict=False, tz="US/Eastern"),
    )
    dates = [
        start + p.duration(days=n)
        for n in range((end.add(days=1) - start).days)
    ]
    return [_.format("dddd, MM-DD-YYYY") for _ in dates]


def days_ago(days: int) -> str:
    """
    Calculates the date of n days ago from today.
    """
    if days > 365:
        raise Exception(f"Max number of days is 365. {days} was entered")

    ago = p.now(tz="US/Eastern") - p.duration(days)
    return ago.to_day_datetime_string()


@app.command()
def daterange(
    start: str = typer.Argument(..., help="Enter the start date"),
    end: str = typer.Argument(..., help="Enter the end date"),
):
    """
    Enter a start date and end date to get a list of dates between.
    """
    if (
        re.match(r"\d{1,2}-\d{1,2}-\d{1,2}", start) is None
        or re.match(r"\d{1,2}-\d{1,2}-\d{1,2}", end) is None
    ):
        raise typer.BadParameter(
            "Format must be Month-Day-Year like so: 03-22-21",
        )
    days = prange(start, end)
    for day in days:
        typer.secho(day, fg=typer.colors.GREEN, bold=True)


@app.command()
def daysago(
    days: int = typer.Argument(
        ...,
        help="Number of days you want to go back to.",
        max=365,
    ),
):
    """
    Enther the number of days you want to go back to.
    """
    the_days = days_ago(days)
    typer.secho(the_days)


@app.command()
def daysfromnow(
    days: int = typer.Argument(
        ...,
        help="Get day from number of days given.",
    ),
):
    """
    Enter the number of days to get the date.
    """
    fromnow = days_from_now(days)
    typer.secho(fromnow)


@app.command()
def adddays(
    days: int = typer.Argument(
        ...,
        help="Number of days from date given.",
    ),
    date: str = typer.Option(
        None,
        "--date",
        "-d",
        help="Enter date in this format: MM-DD-YYYY",
    ),
):
    """
    Add number of days and date to get the number of days.

    If no date is given, then todays date will be used.

    """
    if date:
        dates = add_days(days, date)
        typer.echo(dates)
    else:
        day = add_days(days)
        typer.echo(day)


@app.command()
def diff(
    start: str = typer.Argument(
        ...,
        help="Start date. Format: MM-DD-YYYY",
    ),
    end: str = typer.Argument(
        ...,
        help="End date. Format: MM-DD-YYYY",
    ),
):
    """
    Calculates difference in days between two dates.
    """
    typer.echo(days_diff(start, end))


@app.command()
def isweekday(
    date: str = typer.Argument(
        ...,
        help="Enter date in this format: MM-DD-YYYY",
    ),
):
    """
    Find out if the date is a weekend or date.
    """
    typer.echo(is_weekday(date))


@app.command()
def isweekend(
    date: str = typer.Argument(
        ...,
        help="Enter date in this format: MM-DD-YYYY",
    ),
):
    """
    Check if given date is a weekend.
    """
    typer.echo(is_weekend(date))
