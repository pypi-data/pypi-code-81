import abc
import functools
from string import Template

from lazy import lazy

from benchmark.reporting.base_report_part import BaseReportPart


class BaseChartReportPart(BaseReportPart):

    @lazy
    def template(self):
        template_path = self.config.get_template()
        return self.env.get_template(template_path)

    def render(self, *args, **kwargs):
        data = kwargs.get('data')
        title = kwargs.get('title')
        chart_id = kwargs.get('chart_id')
        return self.template.render(
            array=self.convert_data_to_str(data),
            title=title,
            chart_id=chart_id
        )

    def dump(self, fp, *args, **kwargs):
        data = kwargs.get('data')
        title = kwargs.get('title')
        chart_id = kwargs.get('chart_id')
        stream = self.template.stream(
            array=self.convert_data_to_str(data),
            title=title,
            chart_id=chart_id
        )
        stream.dump(fp)
        return stream

    @abc.abstractmethod
    def convert_data_to_str(self, data):
        pass


class ColumnChartReportPart(BaseChartReportPart):
    def convert_data_to_str(self, data):
        result = '[\n\t["Date", "Time, ms"],\n'
        template = Template("new Date($date).toUTCString(),$time")
        for datum in data:
            substitute = template.substitute(date=datum.get('start_benchmark_time') * 1000,
                                             time=datum.get('median_sec') * 1000)
            result += f"\t[{substitute}],\n"

        if len(result) > 2:
            result = result[:-1]

        result += "\n]"
        return result


class HistogramReportPart(ColumnChartReportPart):
    pass


class LineChartReportPart(BaseChartReportPart):
    def convert_data_to_str(self, data):
        result = "[['Date','Memory, mib'],\n"
        template = Template("new Date($h_axis),$v_axis,")
        for datum in data:
            if datum and isinstance(datum, list):
                result += functools.reduce(lambda acc, item: acc + template.substitute(item), datum, "\n[") + "],"

            elif datum:
                result += f"\t[{template.substitute(datum)}],\n"

        if len(result) > 2:
            result = result[:-1]

        result += "\n]"
        return result
