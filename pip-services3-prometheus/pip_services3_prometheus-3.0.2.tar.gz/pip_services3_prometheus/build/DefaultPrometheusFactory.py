# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_prometheus.count.PrometheusCounters import PrometheusCounters
from pip_services3_prometheus.services.PrometheusMetricsService import PrometheusMetricsService


class DefaultPrometheusFactory(Factory):
    """
    Creates Prometheus components by their descriptors.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`,
    :class:`PrometheusCounters <pip_services3_prometheus.count.PrometheusCounters.PrometheusCounters>`,
    :class:`PrometheusMetricsService <pip_services3_prometheus.services.PrometheusMetricsService.PrometheusMetricsService>`
    """
    descriptor = Descriptor("pip-services", "factory", "prometheus", "default", "1.0")
    prometheus_counters_descriptor = Descriptor("pip-services", "counters", "prometheus", "*", "1.0")
    prometheus_metrics_service_descriptor = Descriptor("pip-services", "metrics-service", "prometheus", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultPrometheusFactory, self).__init__()
        self.register_as_type(DefaultPrometheusFactory.prometheus_counters_descriptor, PrometheusCounters)
        self.register_as_type(DefaultPrometheusFactory.prometheus_metrics_service_descriptor, PrometheusMetricsService)
