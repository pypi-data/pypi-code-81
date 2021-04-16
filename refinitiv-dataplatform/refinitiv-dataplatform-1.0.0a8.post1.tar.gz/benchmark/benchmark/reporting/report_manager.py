from pathlib import Path

import jinja2

import os

from benchmark.reporting.chart_report_part import LineChartReportPart, ColumnChartReportPart, HistogramReportPart


class ReportManager(object):

    @property
    def env(self):
        if self._env is None:
            templates_path = self.config.get_templates()
            self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path), trim_blocks=True,
                                           lstrip_blocks=True)

        return self._env

    @property
    def config(self):
        return self._config_manager.report_config

    @property
    def config_manager(self):
        return self._config_manager

    def __init__(self, config_manager) -> None:
        self._env = None
        self._config_manager = config_manager

    def dump_report(self, results):
        template_report_name = self.config.get_report_name()
        public_js = os.path.join(self.config.get_public(), "js")

        Path(public_js).mkdir(parents=True, exist_ok=True)

        reports = []
        line_chart = LineChartReportPart(self, self.config_manager.line_chart_config)
        column_chart = ColumnChartReportPart(self, self.config_manager.column_chart_config)
        for result in results:
            result_name = result.get('name')

            result['chart_id'] = result_name
            result['title'] = result.get('description') or result_name

            report_name = template_report_name.format(result_name, "js")
            report_js_path = os.path.join(public_js, report_name)
            reports.append({'src_js': os.path.join(".", "js", report_name)})

            if 'time' in result_name:
                column_chart.dump(report_js_path, **result)

            elif 'memory' in result_name:
                line_chart.dump(report_js_path, **result)

        index_path = os.path.join(self.config.get_public(), self.config.get_index_name())

        index_template = self.env.get_template(self.config.get_index_template())
        stream = index_template.stream(
            reports=reports,
            title="Report"
        )
        stream.dump(index_path)
