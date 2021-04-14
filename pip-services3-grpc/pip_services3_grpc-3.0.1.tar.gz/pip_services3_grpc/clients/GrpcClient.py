# -*- coding: utf-8 -*-

from concurrent import futures
import grpc

from pip_services3_commons.run.IOpenable import IOpenable
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.refer.IReferences import IReferences
from pip_services3_commons.refer.IReferenceable import IReferenceable
from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_components.log.CompositeLogger import CompositeLogger
from pip_services3_components.count.CounterTiming import CounterTiming
from pip_services3_components.count.CompositeCounters import CompositeCounters
from pip_services3_commons.errors.ConnectionException import ConnectionException
from pip_services3_rpc.connect.HttpConnectionResolver import HttpConnectionResolver
from pip_services3_commons.data.StringValueMap import StringValueMap
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams

from ..protos import commandable_pb2
from ..protos import commandable_pb2_grpc


class GrpcClient(IOpenable, IReferenceable, IConfigurable):
    """
    Abstract client that calls remove endpoints using GRPC protocol.

    ### Configuration parameters ###
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :func:`link`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - options:
          - retries:               number of retries (default: 3)
          - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
          - timeout:               invocation timeout in milliseconds (default: 10 sec)
    # TODO description
    """

    _default_config = ConfigParams.from_tuples(
        "connection.protocol", "http",
        "connection.host", "0.0.0.0",
        "connection.port", 3000,

        "options.request_max_size", 1024 * 1024,
        "options.connect_timeout", 10000,
        "options.timeout", 10000,
        "options.retries", 3,
        "options.debug", True
    )

    __client = None
    __client_name = None

    # The GRPC client chanel
    __channel = None

    # The connection resolver.
    __connetction_resolver = HttpConnectionResolver()

    # The logger.
    __logger = CompositeLogger()

    # The performance counters.
    __counters = CompositeCounters()

    # The configuration options.
    __options = ConfigParams()

    # The connection timeout in milliseconds.
    __connection_timeout = 100000

    # The invocation timeout in milliseconds.
    __timeout = 100000

    # The remote service uri which is calculated on open.
    __uri = None

    def __init__(self, client_name):
        self.__client_name = client_name

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(GrpcClient._default_config)
        self.__connetction_resolver.configure(config)
        self.__options = self.__options.override(config.get_section('options'))

        self.__connection_timeout = config.get_as_integer_with_default('options.connect_timeout',
                                                                       self.__connection_timeout)
        self.__timeout = config.get_as_integer_with_default('options.timeout', self.__timeout)

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self.__logger.set_references(references)
        self.__counters.set_references(references)
        self.__connetction_resolver.set_references(references)

    def _instrument(self, correlation_id, name):
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: CounterTiming object to end the time measurement.
        """
        self.__logger.trace(correlation_id, 'Executing {} method'.format(name))
        self.__counters.increment_one(name + '.call_count')
        return self.__counters.begin_timing(name + '.call_time')

    def _instrument_error(self, correlation_id, name, err, reerror=False):
        """
        Adds instrumentation to error handling.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :param err: an occured error
        :param reerror: if true - throw error
        """
        if err is not None:
            self.__logger.error(correlation_id, err, 'Failed to call {} method'.format(name))
            self.__counters.increment_one(name + '.call_errors')
            if reerror is not None and reerror is True:
                raise err

    def is_open(self):
        """
        Checks if the component is opened.

        :return: Returns true if the component has been opened and false otherwise.
        """
        return self.__channel is not None

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: Future that receives error or null no errors occured.
        """
        if self.is_open():
            return None

        try:
            connection = self.__connetction_resolver.resolve(correlation_id)
            self.__uri = connection.get_uri()

            options = [('grpc.max_connection_idle_ms', self.__connection_timeout),
                       ('grpc.client_idle_timeout_ms', self.__timeout)]

            if connection.get_protocol_with_default('http') == 'https':
                ssl_ca_file = connection.get_as_nullable_string('ssl_ca_file')
                with open(ssl_ca_file, 'rb') as file:
                    trusted_root = file.read()
                credentials = grpc.ssl_channel_credentials(trusted_root)
                channel = grpc.secure_channel(str(connection.get_host()) + ':' +
                                              str(connection.get_port()), credentials=credentials, options=options)
            else:
                channel = grpc.insecure_channel(str(connection.get_host()) + ':' +
                                                str(connection.get_port()), options=options)
            self.__channel = channel

        except Exception as ex:
            raise ConnectionException(
                correlation_id, 'CANNOT_CONNECT', 'Opening GRPC client failed'
            ).wrap(ex).with_details('url', self.__uri)

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: Future that receives error or null no errors occured.
        """
        if self.__channel is not None:
            # Eat exceptions
            try:
                self.__logger.debug(correlation_id, 'Closed GRPC service at {}'.format(self.__uri))
            except Exception as ex:
                self.__logger.warn(correlation_id, 'Failed while closing GRPC service: {}'.format(ex))
            # if self.__client is not None:
            #     self.__client = None
            self.__channel.close()
            self.__channel = None
            self.__uri = None
            GrpcClient.__connetction_resolver = HttpConnectionResolver()

    def call(self, method, client, request):
        """
        Calls a remote method via GRPC protocol.

        :param client: current client
        :param request: (optional) request object.
        :return: (optional) Future that receives result object or error.
        """

        client = client(self.__channel)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        response = executor.submit(client.__dict__[method], request).result()
        # TODO: check this realization

        return response

    def add_filter_params(self, params, filter):
        """
        AddFilterParams method are adds filter parameters (with the same name as they defined)
        to invocation parameter map.

        :param params: invocation parameters.
        :param filter: (optional) filter parameters
        :return: invocation parameters with added filter parameters.
        """
        params = StringValueMap() if params is None else params

        if filter is not None:
            for k in filter.keys():
                params.put(k, filter[k])

        return params

    def add_paging_params(self, params, paging):
        """
        AddPagingParams method are adds paging parameters (skip, take, total) to invocation parameter map.
        :param params: invocation parameters.
        :param paging: (optional) paging parameters
        :return: invocation parameters with added paging parameters.
        """
        params = StringValueMap() if params is None else params

        if paging is not None:
            params.put('total', paging.total)
            if paging.skip is not None:
                params.put('skip', paging.skip)
            if paging.take is not None:
                params.put('take', paging.take)

        return params
