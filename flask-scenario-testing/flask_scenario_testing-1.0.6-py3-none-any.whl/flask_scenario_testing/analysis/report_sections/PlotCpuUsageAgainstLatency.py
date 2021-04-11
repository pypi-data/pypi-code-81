from matplotlib.ticker import FuncFormatter

from flask_scenario_testing.analysis.Results import Results
import matplotlib.pyplot as plt

from flask_scenario_testing.analysis.services.ComputeCpuUsageAgainstLatency import ComputeCpuUsageAgainstLatency
from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection


class PlotCpuUsageAgainstLatency(ReportSection):

    def __init__(self, endpoint_name: str, service: ComputeCpuUsageAgainstLatency):
        self.service = service
        self.endpoint_name = endpoint_name

    def print(self, results: Results):
        figure = plt.figure()

        ax = plt.gca()
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{}%'.format(x)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{} ms'.format(x)))

        for scenario in results.scenarios():
            cpu_usages, latencies = self.service.get_data(scenario, self.endpoint_name)
            plt.plot(cpu_usages, latencies, '--*', label=scenario.name())

            # plt.plot(trend['x'], trend['y'], 'r--', label='Trend line')

        plt.ylabel('Latency')
        plt.xlabel('CPU Usage')
        plt.legend()

        # max_y_value = max(latencies)

        # Set CPU usage limit to [0, 100]
        ax.set_xlim([0, 100])

        plt.title('CPU Usage vs average latency ({})'.format(self.endpoint_name))

        self.add_figure(figure)
