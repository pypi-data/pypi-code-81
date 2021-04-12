import time
from threading import Lock
from .base_metric import BaseMetric
from ..stats.samples import SlidingTimeWindowSample


class Summary(BaseMetric):

    """
    A metric which calculates the distribution of a value.
    """

    def __init__(
        self,
        key,
        clock=time,
        sample=None,
        tags=None
    ):
        """
        Creates a new instance of a L{Summary}.
        """
        super(Summary, self).__init__(key, tags)
        self.lock = Lock()
        self.clock = clock
        self.sample = sample or SlidingTimeWindowSample(clock=clock)
        self.clear()

    def add(self, value):
        """
        Add value to histogram

        :type value: float
        """
        with self.lock:
            self.sample.update(value)
            self.counter = self.counter + 1
            self.sum = self.sum + value

    def clear(self):
        "reset histogram to initial state"
        with self.lock:
            self.sample.clear()
            self.counter = 0
            self.sum = 0.0

    def get_count(self):
        "get number of values observed by summary"
        return self.counter

    def get_sum(self):
        "get sum of values of summary"
        return self.sum

    def get_snapshot(self):
        "get snapshot instance which holds the percentiles"
        return self.sample.get_snapshot()
