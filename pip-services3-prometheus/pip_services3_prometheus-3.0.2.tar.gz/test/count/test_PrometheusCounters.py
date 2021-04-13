# -*- coding: utf-8 -*-

import os

from pip_services3_commons.config import ConfigParams

from pip_services3_prometheus.count.PrometheusCounters import PrometheusCounters
from test.fixtures.CountersFixture import CountersFixture


class TestPrometheusCounters:
    __counters = None
    __fixture = None

    def setup_method(self, method=None):
        host = os.environ.get('PUSHGATEWAY_SERVICE_HOST') or 'localhost'
        port = os.environ.get('PUSHGATEWAY_SERVICE_PORT') or 9091

        self.__counters = PrometheusCounters()
        self.__fixture = CountersFixture(self.__counters)

        config = ConfigParams.from_tuples(
            'source', 'test',
            'connection.host', host,
            'connection.port', port
        )

        self.__counters.configure(config)

        self.__counters.open(None)

    def teardown_method(self, method=None):
        self.__counters.close(None)

    def test_simple_counters(self):
        self.__fixture.test_simple_counters()

    def test_measure_elapsed_time(self):
        self.__fixture.test_measure_elapsed_time()
