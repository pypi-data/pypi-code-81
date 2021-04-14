# -*- coding: utf-8 -*-

from abc import ABC
import grpc

from pip_services3_commons.refer import DependencyResolver
from pip_services3_commons.run.IOpenable import IOpenable
from pip_services3_commons.refer.IReferences import IReferences
from pip_services3_commons.errors.InvalidStateException import InvalidStateException
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.refer.IUnreferenceable import IUnreferenceable
from pip_services3_commons.refer.IReferenceable import IReferenceable
from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_commons.refer.DependencyResolver import DependencyResolver
from pip_services3_components.log.CompositeLogger import CompositeLogger
from pip_services3_components.count.CompositeCounters import CompositeCounters
from pip_services3_components.count.CounterTiming import CounterTiming
from pip_services3_commons.validate.Schema import Schema

from .GrpcEndpoint import GrpcEndpoint
from .IRegisterable import IRegisterable

import pip_services3_grpc.protos.commandable_pb2_grpc as commandable_pb2_grpc
import pip_services3_grpc.protos.commandable_pb2 as commandable_pb2


class GrpcService(IOpenable, IConfigurable, IRegisterable, IUnreferenceable):
    """
    Abstract service that receives remove calls via GRPC protocol.

    ### Configuration parameters ###
        - dependencies:
          - endpoint:              override for GRPC Endpoint dependency
          - controller:            override for Controller dependency
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - credential - the HTTPS credentials:
          - ssl_key_file:         the SSL private key in PEM
          - ssl_crt_file:         the SSL certificate in PEM
          - ssl_ca_file:          the certificate authorities (root cerfiticates) in PEM


    ### Example ###
        TODO!!!

    """

    __default_config = ConfigParams.from_tuples("dependencies.endpoint", "*:endpoint:grpc:*:1.0")
    __service_name = None
    __config = None
    __references = None
    __local_endpoint = None
    __registrable = None
    __implementation = {}
    __interceptors = []
    __opened = None

    # The GRPC endpoint that exposes this service.
    _endpoint = None

    # The dependency resolver.
    _dependency_resolver = DependencyResolver(__default_config)

    # The logger.
    _logger = CompositeLogger()

    # The performance counters.
    _counters = CompositeCounters()

    def __init__(self, service_name=None):
        self.__service_name = service_name
        self.__registrable = lambda: self._register_service()

    def configure(self, config):
        """
        Configures component by passing configuration parameters.
        :param config: configuration parameters to be set.
        """

        config = config.set_defaults(GrpcService.__default_config)
        self.__config = config
        self._dependency_resolver.configure(config)

    def set_references(self, references):
        """
        Sets references to this endpoint's logger, counters, and connection resolver.
        
        ### References ###
            - logger: **"\*:logger:\*:\*:1.0"**
            - counters: **"\*:counters:\*:\*:1.0"**
            - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver)

        :param references: an IReferences object, containing references to a logger, counters, and a connection resolver.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._dependency_resolver.set_references(references)

        # Get endpoint
        self._endpoint = self._dependency_resolver.get_one_optional('endpoint')

        # Or create a local one
        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self.__local_endpoint = True
        else:
            self.__local_endpoint = False

        #  Add registration callback to the endpoint
        self._endpoint.register(self)

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        # Remove registration callback from endpoint
        if self._endpoint is not None:
            self._endpoint.unregister(self.__registrable)
            self._endpoint = None

    def __create_endpoint(self):
        endpoint = GrpcEndpoint()

        if self.__config:
            endpoint.configure(self.__config)
        if self.__references:
            endpoint.set_references(self.__references)

        return endpoint

    def _instrument(self, correlation_id, name):
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: CounterTiming object to end the time measurement.
        """
        self._logger.trace(correlation_id, 'Executing {} method'.format(name))
        self._counters.increment_one(name + '.exec_time')
        return self._counters.begin_timing(name + '.exec_time')

    def _instrument_error(self, correlation_id, name, err, reerror=False):
        if err is not None:
            self._logger.error(correlation_id, err, 'Failed to execute {} method'.format(name))
            self._counters.increment_one(name + '.exec_errors')

        if reerror:
            raise reerror

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
        :param callback: callback function that receives error or null no errors occured.
        """
        # TODO maybe need add async

        if self.__opened:
            return None

        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self._endpoint.register(self)
            self.__local_endpoint = True

        if self.__local_endpoint:
            try:
                self._endpoint.open(correlation_id)
                self.__opened = True
            except Exception as ex:
                self.__opened = False
                raise ex
        else:
            self.__opened = True

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param callback: callback function that receives error or null no errors occured.
        """
        if not self.__opened:
            return None

        if self._endpoint is None:
            raise InvalidStateException(correlation_id, 'NO_ENDPOINT', 'HTTP endpoint is missing')

        if self.__local_endpoint:
            self._endpoint.close(correlation_id)

        self.__opened = False

    def register_commadable_method(self, method, schema, action):
        self._endpoint.register_commandable_method(method, schema, action)

    def _register_interceptor(self, action):
        if self._endpoint is not None:
            self._endpoint.register_interceptor(action)

    def _register_service(self, implementation):
        # self.register()

        if self._endpoint is not None:
            self._endpoint.register_service(implementation)

    def register(self):
        """
        Registers all service routes in Grpc endpoint.
        This method is called by the service and must be overriden
        in child classes.
        """
