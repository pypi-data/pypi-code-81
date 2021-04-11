import argparse
import os
from datetime import timedelta

from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.report_sections.EndpointOverview import EndpointOverview
from flask_scenario_testing.analysis.report_sections.PlotLatenciesOverTime import PlotLatenciesOverTime
from flask_scenario_testing.analysis.report_sections.PlotTransactionSignatures import PlotTransactionSignatures
from flask_scenario_testing.analysis.report_sections.SimulationDetails import SimulationDetails
from flask_scenario_testing.analysis.segmenters.TimeWindowedSegmenter import TimeWindowedSegmenter
from flask_scenario_testing.analysis.services.ComputeCpuUsageAgainstLatency import ComputeCpuUsageAgainstLatency
from flask_scenario_testing.analysis.services.ComputeCpuUsageOverTime import ComputeCpuUsageOverTime
from flask_scenario_testing.analysis.report_sections.PlotCpuUsageOverTime import PlotCpuUsageOverTime
from flask_scenario_testing.analysis.report_sections.PlotCpuUsageAgainstLatency import PlotCpuUsageAgainstLatency
from flask_scenario_testing.analysis.services.ComputeTransactionSignature import ComputeTransactionSignature
from flask_scenario_testing.analysis.support.Averager import Averager
import psutil


def main():
    parser = argparse.ArgumentParser(description='Run a simulation')
    parser.add_argument('file', metavar='file', type=str, help='File to analyse')
    args = parser.parse_args()

    absolute_output_dir = os.path.abspath(args.file)

    psutil.cpu_percent()
    results = Results.from_json(absolute_output_dir)

    segmenter = TimeWindowedSegmenter(timedelta(seconds=30))
    averager = Averager(segmenter, should_round=False)
    rounding_averager = Averager(segmenter, should_round=True)

    summary_sections = [
        # EndpointOverview(),
        # SimulationDetails(),
        # PlotCpuUsageOverTime(service=ComputeCpuUsageOverTime(results, averager=averager)),
        PlotCpuUsageAgainstLatency('articles.articles_feed', service=ComputeCpuUsageAgainstLatency(
            results=results,
            averager=rounding_averager)
        ),
        PlotCpuUsageAgainstLatency('articles.make_article', service=ComputeCpuUsageAgainstLatency(
            results=results,
            averager=rounding_averager
        )),
        PlotLatenciesOverTime(['articles.get_articles', 'articles.favorite_an_article'], averager),
        PlotTransactionSignatures(ComputeTransactionSignature(results, segmenter))
    ]

    for section in summary_sections:
        section.print(results)
        print()


if __name__ == '__main__':
    main()
