from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.Scenario import Scenario
from flask_scenario_testing.analysis.support.Averager import Averager


class ComputeCpuUsageOverTime(object):
    def __init__(self, results: Results, averager: Averager):
        self.results = results
        self.averager = averager

    def has_averages(self):
        return self.averager is not None

    def cpu_usages_over_time(self):
        cpu_usage_measurements = self.results.cpu_usage_measurements()

        return zip(*cpu_usage_measurements)

    def average_cpu_usages_over_time(self):
        cpu_usage_measurements = self.results.cpu_usage_measurements()

        times, average_cpu_values = zip(*self.averager.average(cpu_usage_measurements))

        return times, average_cpu_values

    def scenarios(self) -> [Scenario]:
        return self.results.scenarios()
