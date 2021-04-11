import numpy as np

from flask_scenario_testing.analysis.CpuBucket import CpuBucket
from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.segmenters.Segmenter import Segmenter
from flask_scenario_testing.analysis.support.ServiceTime import ServiceTime
from flask_scenario_testing.support.pick import pick


class ComputeTransactionSignature(object):
    def __init__(self, results: Results, segmenter: Segmenter):
        self.results = results
        self.segmenter = segmenter

    def table(self, headers, data):
        print('| ' + ' | '.join(headers) + ' | ')
        print('| ' + ' | '.join(['-' * max(1, len(header)) for header in headers]) + ' | ')

        for row in data:
            print('| ' + ' | '.join([str(item) for item in row]) + ' | ')

        print()

    def compute_signature(self, scenario):
        signature = []

        for endpoint in self.results.endpoints():
            cpu_bucket = CpuBucket()

            latency_measurements = self.results.latency_measurements(
                endpoint['name'],
                scenario.started_at(),
                scenario.ended_at()
            )

            if len(latency_measurements) == 0:
                continue

            segments = self.segmenter.segment(latency_measurements)

            for segment in segments:
                cpu_measurements_in_window = [
                    c.value for c in self.results.cpu_usage_measurements()
                    if segment.start <= c.time < segment.end
                ]

                if len(cpu_measurements_in_window) == 0:
                    print('Skipping segment {} - {}'.format(segment.start, segment.end))
                    continue

                average_cpu_in_monitoring_window = float(np.mean(cpu_measurements_in_window))
                average_rounded_cpu_usage = round(average_cpu_in_monitoring_window)

                latency_measurements = pick(segment.measurements, 'value')

                if len(latency_measurements) == 0:
                    continue

                mean_measurement = float(np.mean(latency_measurements))

                for i in range(len(segment.measurements)):
                    cpu_bucket.add(average_rounded_cpu_usage, mean_measurement)

            cpu_usages, averages_arr = cpu_bucket.contents()

            service_times = []

            print('Endpoint: {}'.format(endpoint['name']))

            data = []
            for cpu_usage, average_latency in zip(cpu_usages, averages_arr):
                if cpu_usage > 80:
                    continue

                service_time = average_latency * (1 - cpu_usage / 100)

                data.append([
                    '{}ms'.format(average_latency),
                    '{}%'.format(cpu_usage),
                    '{}ms'.format(service_time)
                ])

                service_times.append(service_time)

            # self.table(['Latency', 'CPU%', 'Service Time'], data)
            # exit(-1)

            signature.append(ServiceTime(
                endpoint_name=endpoint['name'],
                value=np.median(service_times)
            ))

        return signature

    def scenarios(self):
        return self.results.scenarios()
