# -*- coding: utf-8 -*-

import socket
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool

from pip_services3_commons.refer import IReferenceable, Descriptor
from pip_services3_commons.run import IOpenable
from pip_services3_components.count import CachedCounters
from pip_services3_components.log import CompositeLogger
from pip_services3_rpc.connect import HttpConnectionResolver

from pip_services3_prometheus.count.PrometheusCounterConverter import PrometheusCounterConverter


class PrometheusCounters(CachedCounters, IReferenceable, IOpenable):
    """
    Performance counters that send their metrics to Prometheus service.

    The component is normally used in passive mode conjunction with :class:`PrometheusMetricsService <pip_services3_prometheus.services.PrometheusMetricsService.PrometheusMetricsService>`.
    Alternatively when connection parameters are set it can push metrics to Prometheus PushGateway.

    ### Configuration parameters ###
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - options:
          - retries:               number of retries (default: 3)
          - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
          - timeout:               invocation timeout in milliseconds (default: 10 sec)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services to resolve connection

    See :class:`RestService <pip_services3_rpc.services.RestService.RestService>`, :class:`CommandableHttpService <pip_services3_rpc.services.CommandableHttpService.CommandableHttpService>`,

    Example:

    .. code-block:: python

        let counters = PrometheusCounters()
        counters.configure(ConfigParams.fromTuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ));

        counters.open("123")

        counters.increment("mycomponent.mymethod.calls")
        timing = counters.begin_timing("mycomponent.mymethod.exec_time")
        try:
            ...
        finally:
            timing.end_timing()

        counters.dump();
    """

    def __init__(self):
        """
        Creates a new instance of the performance counters.
        """
        self.__logger = CompositeLogger()
        self.__connection_resolver = HttpConnectionResolver()
        self.__opened = False
        self.__source = None
        self.__instance = None
        self.__push_enabled = None
        self.__client = None
        self.__request_route = None
        super(PrometheusCounters, self).__init__()

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        super().configure(config)

        self.__connection_resolver.configure(config)
        self.__source = config.get_as_float_with_default('source', self.__source)
        self.__instance = config.get_as_float_with_default('instance', self.__instance)
        self.__push_enabled = config.get_as_float_with_default('push_enabled', True)

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self.__logger.set_references(references)
        self.__connection_resolver.set_references(references)

        context_info = references.get_one_optional(Descriptor("pip-services", "context-info", "default", "*", "1.0"))
        if context_info is not None and self.__source is None:
            self.__source = context_info.name
        if context_info is not None and self.__instance is None:
            self.__instance = context_info.context_id

    def is_open(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self.__opened or not self.__push_enabled:
            return

        self.__opened = True

        try:
            connection = self.__connection_resolver.resolve(correlation_id)

            job = self.__source or 'unknown'
            instance = self.__instance or socket.gethostname()
            self.__request_route = "/metrics/job/" + job + "/instance/" + instance
            uri = connection.get_uri().split('://')[-1]
            if connection.get_protocol() == 'https':
                self.__client = HTTPSConnectionPool(uri)
            else:
                self.__client = HTTPConnectionPool(uri)

        except Exception as err:
            self.__client = None
            self.__logger.warn(correlation_id, "Connection to Prometheus server is not configured: " + str(err))
            return

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.__opened = False
        self.__request_route = None
        try:
            if self.__client:
                self.__client.close()
        finally:
            self.__client = None

    def _save(self, counters):
        """
        Saves the current counters measurements.

        :param counters: current counters measurements to be saves.
        """
        if self.__client is None or not self.__push_enabled: return

        body = PrometheusCounterConverter.to_string(counters, None, None)
        err = None
        response = None
        try:
            response = self.__client.request('PUT', self.__request_route, body=body)
        except Exception as ex:
            err = ex
        finally:
            if err or response.status >= 400:
                self.__logger.error("prometheus-counters", err, "Failed to push metrics to prometheus")
