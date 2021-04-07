# This file is part of PySunsSpec-Read
#
# PySunSpec-Read is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PySunSpec-Read is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PySunSpec-Read.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright 2020 David Smith applies to this and each file in this project

import json
import logging
from datetime import datetime

from .clean_dict import clean
from .connect_options import ConnectOptions
from .dates import add_timestamp_to_filename
from .device_reader import read
from .files import check_filename_ends_with_json
from .output_filter_predicates import is_zero, is_scale_factor, is_none, apply
from .output_options import OutputOptions

logger = logging.getLogger(__name__)


def read_with_clean(connect_options: ConnectOptions, output_options: OutputOptions) -> str:
    """Reads data from a SunSpec device and outputs it as json, for example from a solar inverter.

    :return: json string, and if output_options.save_reading is True,
        will save the output to a file specified by output_options.output_file_path
    """
    if output_options.save_reading:
        assert output_options.output_file_path
        check_filename_ends_with_json(output_options.output_file_path)
    reading_time = datetime.now()
    reading = read_from_device(connect_options, output_options, reading_time)
    cleaned_reading = clean_reading(output_options, reading, reading_time)
    reading_json = write_as_json(cleaned_reading, output_options, reading_time)
    return reading_json


def read_from_device(connect_options: ConnectOptions, output_options: OutputOptions, reading_time: datetime) -> dict:
    """Intention is that you would call read_with_clean"""
    logger.info("Reading time: " + reading_time.strftime("%Y-%m-%d %H:%M:%S"))
    with read(connect_options=connect_options) as device:
        reading = device.get_dict(computed=not output_options.scale)
    return reading


def write_as_json(cleaned_reading: dict, output_options: OutputOptions, reading_time: datetime) -> str:
    """Intention is that you would call read_with_clean"""
    reading_json = json.dumps(cleaned_reading, sort_keys=False, indent=3)
    if output_options.log_reading:
        logger.info("cleaned reading: " + reading_json)
    if output_options.save_reading:
        with open(add_timestamp_to_filename(output_options, reading_time), "w") as out:
            logger.info("writing reading to {}".format(out.name))
            out.write(reading_json)
    return reading_json


# This would probably be nicer with an interface for a predicate function
def curry_predicates(preds):
    def apply_predicates(key, value):
        return apply(preds, key, value)

    return apply_predicates


def clean_reading(output_options: OutputOptions, reading: dict, reading_time: datetime) -> dict:
    """Intention is that you would call read_with_clean"""

    list_of_predicate_funcs = create_predicates(output_options)
    predicate_list_applier = curry_predicates(list_of_predicate_funcs)
    cleaned_reading = clean(reading, predicate_list_applier)
    if output_options.add_timestamp_to_reading:
        iso_format = reading_time.isoformat()
        logger.info("adding reading_date to output ({})".format(iso_format))
        cleaned_reading["reading_date"] = iso_format
    return cleaned_reading


def create_predicates(output_options: OutputOptions):
    predicates = []
    if output_options.omit_zero_readings:
        predicates.append(is_zero)

    if output_options.omit_none_readings:
        predicates.append(is_none)

    if not output_options.scale:
        predicates.append(is_scale_factor)

    return predicates
