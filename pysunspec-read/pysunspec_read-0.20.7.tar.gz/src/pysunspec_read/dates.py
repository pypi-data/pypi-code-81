from datetime import datetime
from os.path import splitext
from pathlib import Path

from pysunspec_read.output_options import OutputOptions


def add_timestamp_to_filename(output_options: OutputOptions, reading_time: datetime):
    if output_options.add_timestamp_to_filename:
        return add_date_and_epoch_to_path(output_options.output_file_path, reading_time)
    else:
        return output_options.output_file_path


def add_date_and_epoch_to_path(path, reading_time):
    path_without_extension = splitext(path)[0]
    date_and_epoch_str = to_date_and_epoch(reading_time)
    return Path(path_without_extension + "_" + date_and_epoch_str + ".json")


def to_date_and_epoch(reading_time):
    """A filesafe date string for both human and machine reading and sorting
    creates a string of the format
    d_<file safe date>_e_<seconds since epoch_>
    for example 'd_2020-11-08_01-15-59_e_1604798159'"""
    epoch_seconds = to_epoch_seconds(reading_time)
    file_date_str = to_file_safe_date_time(reading_time)
    date_and_epoch_str = "d_" + file_date_str + "_e_" + str(epoch_seconds)
    return date_and_epoch_str


def to_file_safe_date_time(reading_time: datetime) -> str:
    """convert a datetime object into a string that is safe to be used in a filename
    format is 24 hour time (excludes the quotes): '2020-11-08_01-15-59'"""
    file_date_str = reading_time.strftime("%Y-%m-%d_%H-%M-%S")
    return file_date_str


def to_epoch_seconds(reading_time: datetime) -> int:
    """converts a datetime object into an integer that can be used to order datetimes
    example: for the time '2020-11-08 01:15:59' would be 1604798159 see https://www.epochconverter.com/"""
    epoch_seconds = int(reading_time.timestamp())
    return epoch_seconds
