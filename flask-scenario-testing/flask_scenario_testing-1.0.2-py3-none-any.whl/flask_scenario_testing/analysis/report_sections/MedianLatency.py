import numpy as np

from flask_scenario_testing.analysis.Results import Results

from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection
from flask_scenario_testing.support.pick import pick


class MedianLatency(ReportSection):
    def print(self, results: Results):
        endpoints = results.endpoints()

        data = []
        for endpoint in endpoints:
            measurements = pick(endpoint['latency_measurements'], 'measurement')

            data.append([
                endpoint['name'],
                np.median(measurements) if len(measurements) > 0 else 'N/A'
            ])

        self.table(['Endpoint', 'Measurement'], data)
