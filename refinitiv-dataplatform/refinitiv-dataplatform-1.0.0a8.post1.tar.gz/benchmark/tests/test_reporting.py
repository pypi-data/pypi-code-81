from benchmark.reporting import LineChartReportPart
from benchmark.config import ConfigManager


def test_line_chart_report_part_empty_data():
    # Given
    manager = ConfigManager('./config.ini')
    report_part = LineChartReportPart(manager.report_config)
    data = [{}, {}, {}]

    # When
    s = report_part.convert_data_to_str(data=data)

    # Then
    assert s == "[\n]"


def test_line_chart_report_part_with_data():
    # Given
    manager = ConfigManager('./config.ini')
    report_part = LineChartReportPart(manager.report_config)
    data = [
        [{'h_axis': 0, 'v_axis': 1}, {'h_axis': 2, 'v_axis': 3}],
        [{'h_axis': 10, 'v_axis': 11}, {'h_axis': 12, 'v_axis': 13}]
    ]

    # When
    s = report_part.convert_data_to_str(data=data)
    s = s.replace("\n", "")
    # Then
    assert s == "[[new Date(0),1,new Date(2),3,],[new Date(10),11,new Date(12),13,]]"
