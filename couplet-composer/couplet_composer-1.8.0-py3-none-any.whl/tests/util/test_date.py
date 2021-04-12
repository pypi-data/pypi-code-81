# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This module defines the tests for the date utilities."""

from datetime import datetime

from couplet_composer.util import date


def test_date_difference():
    first = datetime.strptime("1990-07-27 00:00:00", "%Y-%m-%d %H:%M:%S")
    second = datetime.strptime("2011-11-11 00:00:00", "%Y-%m-%d %H:%M:%S")
    assert date.date_difference(first, second) == 671932800


def test_to_days():
    s = 1432604
    (days, hours, minutes, seconds) = date.to_days(s)
    assert days == 16
    assert hours == 13
    assert minutes == 56
    assert seconds == 44


class TestToDateString:
    def test_to_date_string_basic(self):
        s = 2742513
        expected = "31 days, 17 hours, 48 minutes, and 33 seconds"
        assert date.to_date_string(s) == expected

    def test_to_date_string_one_day(self):
        s = 142513
        expected = "1 day, 15 hours, 35 minutes, and 13 seconds"
        assert date.to_date_string(s) == expected

    def test_to_date_string_one_hour(self):
        s = 259200 + 4352
        expected = "3 days, 1 hour, 12 minutes, and 32 seconds"
        assert date.to_date_string(s) == expected

    def test_to_date_string_one_minute(self):
        s = 259200 + 72082
        expected = "3 days, 20 hours, 1 minute, and 22 seconds"
        assert date.to_date_string(s) == expected

    def test_to_date_string_one_second(self):
        s = 259200 + 61921
        expected = "3 days, 17 hours, 12 minutes, and 1 second"
        assert date.to_date_string(s) == expected
