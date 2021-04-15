import csv
from io import StringIO


def csv_read_as_list(csv_data: str, **kwargs):
    """Read the csv_data as a list."""
    yield from csv.reader(StringIO(csv_data), **kwargs)


def csv_read_as_dict(csv_data: str, **kwargs):
    """Read the csv_data as a dict."""
    yield from csv.DictReader(StringIO(csv_data), **kwargs)
