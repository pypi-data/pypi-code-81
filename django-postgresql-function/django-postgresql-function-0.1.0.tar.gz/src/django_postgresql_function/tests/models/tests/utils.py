
import random

from datetime import timedelta

from factory.fuzzy import BaseFuzzyAttribute


class FuzzyTimeStamp(BaseFuzzyAttribute):
    """Случайный timedelta в заданном промежутке"""

    def __init__(self, start_timestamp, end_timestamp=None):
        super().__init__()

        if end_timestamp is None:
            end_timestamp = start_timestamp
            start_timestamp = 0

        if start_timestamp > end_timestamp:
            raise ValueError(
                f'FuzzyTimeStamp should have start <= end;'
                f'got {start_timestamp} > {end_timestamp}'
            )

        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def fuzz(self):
        return timedelta(
            seconds=random.randint(
                self.start_timestamp,
                self.end_timestamp))
