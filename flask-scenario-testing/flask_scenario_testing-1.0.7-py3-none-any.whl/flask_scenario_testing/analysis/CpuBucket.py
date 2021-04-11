import numpy as np


class CpuBucket(object):
    def __init__(self):
        self.bucket_collection = {}
        self.counts = {}

        for i in range(0, 101):
            self.bucket_collection[i] = []
            self.counts[i] = 0

    def add(self, cpu_value: int, latency_measurement: float):
        assert 0 <= cpu_value <= 100

        self.bucket_collection[cpu_value].append(latency_measurement)
        self.counts[cpu_value] += 1

    def contents(self):
        averages_arr = []
        cpu_usages = []

        for i in range(0, 101):
            bucket = self.bucket_collection[i]

            if len(bucket) > 0:
                cpu_usages.append(i)
                averages_arr.append(np.mean(self.bucket_collection[i]))

        return cpu_usages, averages_arr
