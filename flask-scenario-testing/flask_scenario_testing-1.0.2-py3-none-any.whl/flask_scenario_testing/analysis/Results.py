import json
from datetime import datetime

from flask_scenario_testing.analysis.Scenario import Scenario
from flask_scenario_testing.analysis.support.Measurement import Measurement


class Results(object):

    def __init__(self, results):
        self._results = results

    @staticmethod
    def from_json(absolute_file_name: str):
        with open(absolute_file_name, 'r') as f:
            configuration = json.load(f)

            return Results(configuration)

    def get_total_request_count(self):
        total_count = 0

        for endpoint in self.endpoints():
            endpoint_request_count = len(endpoint['latency_measurements'])

            total_count += endpoint_request_count

        return total_count

    def endpoints(self):
        return self._results['endpoints']

    def started_at(self):
        return self._results['started_at']

    def stopped_at(self):
        return self._results['stopped_at']

    def scenarios(self):
        return [
            Scenario(
                name=r['name'],
                started_at=datetime.fromisoformat(r['start']),
                ended_at=datetime.fromisoformat(r['end'])
            ) for idx, r in enumerate(self._results['scenarios'])
        ]

    def cpu_usage_measurements(self) -> [Measurement]:
        results = self._results['cpu_usage_measurements']

        return [Measurement(value=c['measurement'], time=datetime.fromisoformat(c['time'])) for c in results]

    def _get_endpoint(self, endpoint_name):
        filtered = list(filter(lambda x: x['name'] == endpoint_name, self.endpoints()))

        if len(filtered) == 0:
            return None

        return filtered[0]

    def latency_measurements(self, endpoint_name: str, start: datetime = None, end: datetime = None) -> [Measurement]:
        endpoint = self._get_endpoint(endpoint_name)

        if not endpoint:
            raise ValueError('Endpoint not found')

        if start and end:
            return [
                Measurement(time=measurement_time, value=m['measurement'])
                for m in endpoint['latency_measurements']
                if start <= (measurement_time := datetime.fromisoformat(m['time'])) <= end
            ]
        else:
            return [
                Measurement(time=datetime.fromisoformat(m['time']), value=m['measurement'])
                for m in endpoint['latency_measurements']
            ]