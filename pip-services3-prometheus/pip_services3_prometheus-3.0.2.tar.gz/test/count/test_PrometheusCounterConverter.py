# -*- coding: utf-8 -*-
from datetime import datetime

from pip_services3_commons.random import RandomDateTime
from pip_services3_components.count import Counter, CounterType

from pip_services3_prometheus.count.PrometheusCounterConverter import PrometheusCounterConverter


class TestPrometheusCounterConverter:

    def test_known_counter_exec_service_metrics_good(self):
        known_counter_exec_service_metrics_good_test_cases = [
            {'counter_name': "MyService1.MyCommand1.exec_count", 'expected_name': "exec_count"},
            {'counter_name': "MyService1.MyCommand1.exec_time", 'expected_name': "exec_time"},
            {'counter_name': "MyService1.MyCommand1.exec_errors", 'expected_name': "exec_errors"}
        ]

        for test_data in known_counter_exec_service_metrics_good_test_cases:
            counter_name = test_data['counter_name']
            expected_name = test_data['expected_name']

            counters = []

            counter1 = Counter(counter_name, CounterType.Increment)
            counter1.count = 1
            counter1.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter1)

            counter2 = Counter(counter_name, CounterType.Interval)
            counter2.count = 11
            counter2.max = 13
            counter2.min = 3
            counter2.average = 3.5
            counter2.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter2)

            counter3 = Counter(counter_name, CounterType.LastValue)
            counter3.last = 2
            counter3.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter3)

            counter4 = Counter(counter_name, CounterType.Statistics)
            counter4.count = 111
            counter4.max = 113
            counter4.min = 13
            counter4.average = 13.5
            counter4.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter4)

            body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")

            expected = f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 1\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 13\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 3\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 3.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 11\n' \
                       + f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 113\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 13\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 13.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 111\n'

            assert expected == body

    def test_known_counter_exec_client_metrics_good(self):
        known_counter_exec_service_metrics_good_test_cases = [
            {'counter_name': "MyTarget1.MyService1.MyCommand1.call_count", 'expected_name': "call_count"},
            {'counter_name': "MyTarget1.MyService1.MyCommand1.call_time", 'expected_name': "call_time"},
            {'counter_name': "MyTarget1.MyService1.MyCommand1.call_errors", 'expected_name': "call_errors"}
        ]

        for test_data in known_counter_exec_service_metrics_good_test_cases:
            counter_name = test_data['counter_name']
            expected_name = test_data['expected_name']

            counters = []

            counter1 = Counter(counter_name, CounterType.Increment)
            counter1.count = 1
            counter1.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter1)

            counter2 = Counter(counter_name, CounterType.Interval)
            counter2.count = 11
            counter2.max = 13
            counter2.min = 3
            counter2.average = 3.5
            counter2.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter2)

            counter3 = Counter(counter_name, CounterType.LastValue)
            counter3.last = 2
            counter3.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter3)

            counter4 = Counter(counter_name, CounterType.Statistics)
            counter4.count = 111
            counter4.max = 113
            counter4.min = 13
            counter4.average = 13.5
            counter4.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter4)

            body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")

            expected = f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 1\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 13\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 3\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 3.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 11\n' \
                       + f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 2\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 113\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 13\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 13.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\",target=\"MyTarget1\"} 111\n'

            assert expected == body

    def test_known_counter_exec_queue_metrics_good(self):
        known_counter_exec_service_metrics_good_test_cases = [
            {'counter_name': "queue.default.sent_messages", 'expected_name': "queue_sent_messages"},
            {'counter_name': "queue.default.received_messages", 'expected_name': "queue_received_messages"},
            {'counter_name': "queue.default.dead_messages", 'expected_name': "queue_dead_messages"}
        ]

        for test_data in known_counter_exec_service_metrics_good_test_cases:
            counter_name = test_data['counter_name']
            expected_name = test_data['expected_name']

            counters = []

            counter1 = Counter(counter_name, CounterType.Increment)
            counter1.count = 1
            counter1.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter1)

            counter2 = Counter(counter_name, CounterType.Interval)
            counter2.count = 11
            counter2.max = 13
            counter2.min = 3
            counter2.average = 3.5
            counter2.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter2)

            counter3 = Counter(counter_name, CounterType.LastValue)
            counter3.last = 2
            counter3.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter3)

            counter4 = Counter(counter_name, CounterType.Statistics)
            counter4.count = 111
            counter4.max = 113
            counter4.min = 13
            counter4.average = 13.5
            counter4.time = RandomDateTime.next_datetime(datetime.now())
            counters.append(counter4)

            body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")

            expected = f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 1\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 13\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 3\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 3.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 11\n' \
                       + f'# TYPE {expected_name} gauge\n{expected_name}' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 2\n' \
                       + f'# TYPE {expected_name}_max gauge\n{expected_name}_max' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 113\n' \
                       + f'# TYPE {expected_name}_min gauge\n{expected_name}_min' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 13\n' \
                       + f'# TYPE {expected_name}_average gauge\n{expected_name}_average' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 13.5\n' \
                       + f'# TYPE {expected_name}_count gauge\n{expected_name}_count' + '{source=\"MyApp\",instance=\"MyInstance\",queue=\"default\"} 111\n'

            assert expected == body

    def test_empty_counters(self):
        counters = []
        body = PrometheusCounterConverter.to_string(None, '', '')
        assert '' == body

    def test_null_values(self):
        body = PrometheusCounterConverter.to_string(None, '', '')
        assert '' == body

    def test_single_increment_no_labels(self):
        counters = []

        counter = Counter("MyCounter", CounterType.Increment)
        counter.average = 2
        counter.min = 1
        counter.max = 3
        counter.count = 2
        counter.last = 3
        counter.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter)

        body = PrometheusCounterConverter.to_string(counters, None, None)
        expected = "# TYPE mycounter gauge\nmycounter 2\n"

        assert body == expected

    def test_single_increment_source_instance(self):
        counters = []

        counter = Counter("MyCounter", CounterType.Increment)
        counter.average = 2
        counter.min = 1
        counter.max = 3
        counter.count = 2
        counter.last = 3
        counter.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE mycounter gauge\nmycounter{source=\"MyApp\",instance=\"MyInstance\"} 2\n"

        assert body == expected

    def test_multi_increment_source_instance(self):
        counters = []

        counter1 = Counter("MyCounter1", CounterType.Increment)
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyCounter2", CounterType.Increment)
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE mycounter1 gauge\nmycounter1{source=\"MyApp\",instance=\"MyInstance\"} 2\n" \
                   + "# TYPE mycounter2 gauge\nmycounter2{source=\"MyApp\",instance=\"MyInstance\"} 5\n"

        assert body == expected

    def test_multi_increment_exec_with_only_two_source_instance(self):
        counters = []

        counter1 = Counter("MyCounter1.exec_time", CounterType.Increment)
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyCounter2.exec_time", CounterType.Increment)
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE mycounter1_exec_time gauge\nmycounter1_exec_time{source=\"MyApp\",instance=\"MyInstance\"} 2\n" \
                   + "# TYPE mycounter2_exec_time gauge\nmycounter2_exec_time{source=\"MyApp\",instance=\"MyInstance\"} 5\n"

        assert body == expected

    def test_multi_increment_exec_source_instance(self):
        counters = []

        counter1 = Counter("MyService1.MyCommand1.exec_time", CounterType.Increment)
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyService2.MyCommand2.exec_time", CounterType.Increment)
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE exec_time gauge\nexec_time{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n" \
                   + "# TYPE exec_time gauge\nexec_time{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 5\n"

        assert body == expected

    def test_multi_interval_exec_source_instance(self):
        counters = []

        counter1 = Counter("MyService1.MyCommand1.exec_time", CounterType.Interval)
        counter1.min = 1
        counter1.max = 3
        counter1.average = 2
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyService2.MyCommand2.exec_time", CounterType.Interval)
        counter2.min = 2
        counter2.max = 4
        counter2.average = 3
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE exec_time_max gauge\nexec_time_max{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 3\n" \
                   + "# TYPE exec_time_min gauge\nexec_time_min{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 1\n" \
                   + "# TYPE exec_time_average gauge\nexec_time_average{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n" \
                   + "# TYPE exec_time_count gauge\nexec_time_count{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n" \
                   + "# TYPE exec_time_max gauge\nexec_time_max{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 4\n" \
                   + "# TYPE exec_time_min gauge\nexec_time_min{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 2\n" \
                   + "# TYPE exec_time_average gauge\nexec_time_average{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 3\n" \
                   + "# TYPE exec_time_count gauge\nexec_time_count{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 5\n"

        assert body == expected

    def test_multi_statistics_exec_source_instance(self):
        counters = []

        counter1 = Counter("MyService1.MyCommand1.exec_time", CounterType.Statistics)
        counter1.min = 1
        counter1.max = 3
        counter1.average = 2
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyService2.MyCommand2.exec_time", CounterType.Statistics)
        counter2.min = 2
        counter2.max = 4
        counter2.average = 3
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE exec_time_max gauge\nexec_time_max{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 3\n" \
                   + "# TYPE exec_time_min gauge\nexec_time_min{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 1\n" \
                   + "# TYPE exec_time_average gauge\nexec_time_average{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n" \
                   + "# TYPE exec_time_count gauge\nexec_time_count{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 2\n" \
                   + "# TYPE exec_time_max gauge\nexec_time_max{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 4\n" \
                   + "# TYPE exec_time_min gauge\nexec_time_min{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 2\n" \
                   + "# TYPE exec_time_average gauge\nexec_time_average{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 3\n" \
                   + "# TYPE exec_time_count gauge\nexec_time_count{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 5\n"

        assert body == expected

    def test_multi_last_value_exec_source_instance(self):
        counters = []

        counter1 = Counter("MyService1.MyCommand1.exec_time", CounterType.LastValue)
        counter1.count = 2
        counter1.last = 3
        counter1.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter1)

        counter2 = Counter("MyService2.MyCommand2.exec_time", CounterType.LastValue)
        counter2.count = 5
        counter2.last = 10
        counter2.time = RandomDateTime.next_datetime(datetime.now())
        counters.append(counter2)

        body = PrometheusCounterConverter.to_string(counters, "MyApp", "MyInstance")
        expected = "# TYPE exec_time gauge\nexec_time{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService1\",command=\"MyCommand1\"} 3\n" \
                   + "# TYPE exec_time gauge\nexec_time{source=\"MyApp\",instance=\"MyInstance\",service=\"MyService2\",command=\"MyCommand2\"} 10\n"

        assert body == expected
