import numpy as np

from flask_scenario_testing.analysis.CpuBucket import CpuBucket
from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.Scenario import Scenario

from flask_scenario_testing.analysis.support.Averager import Averager
from flask_scenario_testing.analysis.support.Measurement import Measurement


class ComputeCpuUsageAgainstLatency(object):
    def __init__(self, averager: Averager, results: Results):
        self.results = results
        self.averager = averager

    def get_data(self, scenario: Scenario, endpoint_name: str):
        cpu_usage_groups = self.averager.average(self.results.cpu_usage_measurements())

        latency_measurements = self.results.latency_measurements(
            endpoint_name,
            scenario.started_at(),
            scenario.ended_at()
        )

        bucket = CpuBucket()

        for latency_measurement in latency_measurements:
            cpu_measurement = self.find_nearby_cpu_measurement(cpu_usage_groups, latency_measurement.time)

            bucket.add(cpu_measurement.value, latency_measurement.value)

        cpu_usages, average_latencies = bucket.contents()

        # trend = self.compute_trend(cpu_usages, average_latencies)

        return cpu_usages, average_latencies

    def find_nearby_cpu_measurement(self, cpu_usage_groups, time) -> Measurement:
        diffs = [(idx, abs((c.time - time).total_seconds())) for idx, c in enumerate(cpu_usage_groups)]
        idx, smallest_value = sorted(diffs, key=lambda d: d[1])[0]

        return cpu_usage_groups[idx]

    def compute_trend(self, cpu_usages, average_latencies):
        z = np.polyfit(cpu_usages, average_latencies, 1)
        p = np.poly1d(z)

        return dict(x=cpu_usages, y=p(cpu_usages))
