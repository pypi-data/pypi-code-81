from benchmark.config.report_config import ReportConfig


class LineChartConfig(ReportConfig):
    def get_template(self):
        return self._get_option('reporting.line-chart', 'template')


class ColumnChartConfig(ReportConfig):
    def get_template(self):
        return self._get_option('reporting.column-chart', 'template')


class HistogramConfig(ReportConfig):
    def get_template(self):
        return self._get_option('reporting.histogram', 'template')
