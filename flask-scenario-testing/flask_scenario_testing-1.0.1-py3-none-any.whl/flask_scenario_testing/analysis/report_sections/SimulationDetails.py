from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection


class SimulationDetails(ReportSection):
    def print(self, results: Results):
        self.table(
            headers=['', ''],
            data=[
                ['Total number of requests', results.get_total_request_count()],
                ['Simulation start', results.started_at()],
                ['Simulation start', results.stopped_at()],
            ]
        )

        rows = []

        for idx, scenario in enumerate(results.scenarios()):
            rows.append([str(idx + 1),  'Start',    scenario.started_at()])
            rows.append(['',            'End',      scenario.ended_at()])

        self.table(['Scemarop', '', ''], rows)
