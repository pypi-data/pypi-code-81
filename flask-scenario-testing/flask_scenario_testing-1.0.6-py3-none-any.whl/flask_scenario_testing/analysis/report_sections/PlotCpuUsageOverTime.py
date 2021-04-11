import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from flask_scenario_testing.analysis.services.ComputeCpuUsageOverTime import ComputeCpuUsageOverTime
from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection


class PlotCpuUsageOverTime(ReportSection):
    def __init__(self, service: ComputeCpuUsageOverTime):
        ReportSection.__init__(self)
        self.service = service

    def print(self, _) -> None:
        times, cpu_values = self.service.cpu_usages_over_time()

        figure = plt.figure()
        plt.plot(times, cpu_values, label='CPU Usage', color=self.next_color())

        if self.service.has_averages():
            times, cpu_values = self.service.average_cpu_usages_over_time()

            plt.plot(times, cpu_values, label='CPU Usage (average)', color=self.next_color())

        self.draw_scenario_vlines()

        plt.title('CPU Usage over time')
        plt.xticks(rotation=45)

        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{}%'.format(x)))
        ax.set_ylim([0, 110])

        plt.legend()
        plt.gcf().subplots_adjust(bottom=0.2)

        self.add_figure(figure)

    def draw_scenario_vlines(self):
        for scenario in self.service.scenarios():
            label = "Start '{}'".format(scenario.name())

            plt.axvline(x=scenario.started_at(), color=self.next_color(), linestyle='--', label=label)
