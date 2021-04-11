from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection


class EndpointOverview(ReportSection):
    def print(self, results: Results):
        endpoints = results.endpoints()

        self.heading('Endpoint overview', 3)

        self.table(
            headers=['Name', 'Requests measured'],
            data=[
                [endpoint['name'], len(endpoint['latency_measurements'])] for endpoint in endpoints
            ]
        )
