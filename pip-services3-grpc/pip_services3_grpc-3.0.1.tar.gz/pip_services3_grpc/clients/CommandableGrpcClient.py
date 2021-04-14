# -*- coding: utf-8 -*-

import json

from .GrpcClient import GrpcClient

from ..protos import commandable_pb2
from ..protos import commandable_pb2_grpc

from pip_services3_commons.errors.ApplicationExceptionFactory import ApplicationExceptionFactory
from pip_services3_commons.errors.ApplicationException import ApplicationException
from pip_services3_commons.errors.ErrorDescription import ErrorDescription


class CommandableGrpcClient(GrpcClient):
    """
    Abstract client that calls commandable GRPC service.

    Commandable services are generated automatically for :func:`link`
    Each command is exposed as Invoke method that receives all parameters as args.

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

    TODO: description
    """

    # The service name
    __service_name = None

    # Instanco of client
    __client = None

    def __init__(self, name):
        """
        Creates a new instance of the client.

        :param name: a service name.
        """
        super().__init__('commandable.Commandable')
        self.__service_name = name
        self.__client = commandable_pb2_grpc.CommandableStub

    def call_command(self, name, correlation_id, params):
        """
        Calls a remote method via GRPC commadable protocol.
        The call is made via Invoke method and all parameters are sent in args object.
        The complete route to remote method is defined as serviceName + '.' + name.

        :param name: a name of the command to call.
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param params: command parameters.
        :return: Future that receives result
        """

        method = self.__service_name + '.' + name
        timing = self._instrument(correlation_id, method)

        request = commandable_pb2.InvokeRequest()

        request.method = method
        request.correlation_id = correlation_id
        request.args_empty = params is None

        for key in params.keys():
            if hasattr(params[key], '__dict__'):
                params.update({key: params[key].__dict__})

        request.args_json = json.dumps(params) if params is not None else ''

        try:
            response = self.call('invoke', self.__client, request)
            timing.end_timing()
            # Handle error response
            if response.error is not None and response.error.code != '':
                err = ErrorDescription()
                err.category = response.error.category
                err.code = response.error.code
                err.correlation_id = response.error.correlation_id
                err.status = response.error.status
                err.message = response.error.message
                err.cause = response.error.cause
                err.stack_trace = response.error.stack_trace
                err.details = response.error.details
                raise ApplicationExceptionFactory.create(err)

            if response.result_empty or response.result_empty == '' or response.result_empty is None:
                return None

            # Handle regular response
            return response.result_json

        except Exception as ex:
            timing.end_timing()
            # Handle unexpected error
            err = ex
            if not (type(ex) is ApplicationException):
                err = ApplicationException().wrap(ex)
            self._instrument_error(correlation_id, method, err, True)
