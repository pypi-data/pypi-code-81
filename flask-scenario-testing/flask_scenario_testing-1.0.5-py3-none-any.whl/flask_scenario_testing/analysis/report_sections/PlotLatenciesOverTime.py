from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection
import matplotlib.pyplot as plt

from flask_scenario_testing.analysis.support.Averager import Averager
from flask_scenario_testing.support.pick import pick


class PlotLatenciesOverTime(ReportSection):
    def __init__(self, endpoint_names: [str], averager: Averager):
        ReportSection.__init__(self)
        self.endpoint_names = endpoint_names
        self.averager = averager

    def draw_scenario_vlines(self, results: Results):
        for scenario in results.scenarios():
            label = "Start '{}'".format(scenario.name())

            plt.axvline(x=scenario.started_at(), color=self.next_color(), linestyle='--', label=label)

    def print(self, results: Results):
        figure = plt.figure()

        for endpoint_name in self.endpoint_names:
            latency_measurements = results.latency_measurements(endpoint_name)

            avg_measurements = self.averager.average(latency_measurements)

            y_values = pick(avg_measurements, 'value')
            x_values = pick(avg_measurements, 'time')

            plt.ylabel('Latency')
            plt.xlabel('Time')

            plt.plot(x_values, y_values, label=endpoint_name)

        plt.title('Latency over time')

        self.draw_scenario_vlines(results)
        plt.legend()

        self.add_figure(figure)
