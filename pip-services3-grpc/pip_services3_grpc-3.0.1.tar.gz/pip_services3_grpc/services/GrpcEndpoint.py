# -*- coding: utf-8 -*-

import json
import grpc
from concurrent import futures

from pip_services3_commons.run.IOpenable import IOpenable
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.refer.IReferenceable import IReferenceable
from pip_services3_commons.refer.IReferences import IReferences
from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_commons.run.Parameters import Parameters
from pip_services3_components.log.CompositeLogger import CompositeLogger
from pip_services3_components.count.CompositeCounters import CompositeCounters
from pip_services3_commons.errors.ErrorDescriptionFactory import ErrorDescriptionFactory
from pip_services3_commons.errors.ConnectionException import ConnectionException
from pip_services3_commons.errors.InvocationException import InvocationException
from pip_services3_commons.convert.JsonConverter import JsonConverter
from pip_services3_rpc.connect.HttpConnectionResolver import HttpConnectionResolver
from pip_services3_commons.validate.Schema import Schema
from pip_services3_commons.data.DataPage import DataPage

from .IRegisterable import IRegisterable

import pip_services3_grpc.protos.commandable_pb2 as commandable_pb2
import pip_services3_grpc.protos.commandable_pb2_grpc as commandable_pb2_grpc


class _CommandableMediator(commandable_pb2_grpc.CommandableServicer):
    def add_servicer_to_server(self, server):
        commandable_pb2_grpc.add_CommandableServicer_to_server(self, server)

    def __init__(self):
        self.__invoke = None

    def invoke(self, request, context):
        if self.__invoke is not None:
            return self.__invoke(request, context)

        return None

    # Sets invoke function
    def invoke_func(self, fn):
        self.__invoke = fn


class GrpcEndpoint(IOpenable, IConfigurable, IReferenceable):
    """
    Used for creating GRPC endpoints. An endpoint is a URL, at which a given service can be accessed by a client.

    ### Configuration parameters ###

    Parameters to pass to the :func:`configure` method for component configuration:

        - connection(s) - the connection resolver's connections:
            - "connection.discovery_key" - the key to use for connection resolving in a discovery service;
            - "connection.protocol" - the connection's protocol;
            - "connection.host" - the target host;
            - "connection.port" - the target port;
            - "connection.uri" - the target URI.
        - credential - the HTTPS credentials:
            - "credential.ssl_key_file" - the SSL private key in PEM
            - "credential.ssl_crt_file" - the SSL certificate in PEM
            - "credential.ssl_ca_file" - the certificate authorities (root cerfiticates) in PEM

    ### References ###
    
    A logger, counters, and a connection resolver can be referenced by passing the
    following references to the object's :func:`set_references` method:

        - logger: **\*:logger:\*:\*:1.0"**;
        - counters: **"\*:counters:\*:\*:1.0"**;
        - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver).

    ### Examples ###
        TODO!!!

    """

    __defaultConfig = ConfigParams.from_tuples(
        "connection.protocol", "http",
        "connection.host", "0.0.0.0",
        "connection.port", 3000,

        "credential.ssl_key_file", None,
        "credential.ssl_crt_file", None,
        "credential.ssl_ca_file", None,

        "options.maintenance_enabled", None,
        "options.request_max_size", 1024 * 1024,
        "options.file_max_size", 200 * 1024 * 1024,
        "options.connect_timeout", 60000,
        "options.debug", None
    )

    __server = None
    __connection_resolver = HttpConnectionResolver()
    __logger = CompositeLogger()
    __counters = CompositeCounters()
    __maintenance_enabled = False
    __file_max_size = 200 * 1024 * 1024
    __uri = None
    __registrations = []
    __commandable_methods = None
    __commandable_schemas = None
    __commandable_service = None
    __interceptors = []

    def configure(self, config):
        """
        Configures this HttpEndpoint using the given configuration parameters.
        
        ### Configuration parameters ###
            - connection(s) - the connection resolver's connections;
            - "connection.discovery_key" - the key to use for connection resolving in a dis
            - "connection.protocol" - the connection's protocol;
            - "connection.host" - the target host;
            - "connection.port" - the target port;
            - "connection.uri" - the target URI.
            - "credential.ssl_key_file" - SSL private key in PEM
            - "credential.ssl_crt_file" - SSL certificate in PEM
            - "credential.ssl_ca_file" - Certificate authority (root certificate) in PEM

        :param config: configuration parameters, containing a "connection(s)" section.
        """
        config = config.set_defaults(GrpcEndpoint.__defaultConfig)
        self.__connection_resolver.configure(config)

        self.__maintenance_enabled = config.get_as_boolean_with_default('options.maintenance_enabled',
                                                                        self.__maintenance_enabled)
        self.__file_max_size = ConfigParams().get_as_long_with_default(key='options.file_max_size',
                                                                       default_value=self.__file_max_size)

    def set_references(self, references):
        """
        Sets references to this endpoint's logger, counters, and connection resolver.

        __References:__
        - logger: **"\*:logger:\*:\*:1.0"**
        - counters: **"\*:counters:\*:\*:1.0"**
        - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver)

        :param references: an IReferences object, containing references to a logger, counters, and a connection resolver.
        """
        self.__logger.set_references(references)
        self.__counters.set_references(references)
        self.__connection_resolver.set_references(references)

    def is_open(self):
        """
        :return: whether or not this endpoint is open with an actively listening GRPC server.
        """
        return self.__server is not None

    def open(self, correlation_id, max_workers=15):
        """
        Opens a connection using the parameters resolved by the referenced connection
        resolver and creates a GRPC server (service) using the set options and parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param max_workers: max count of workers in thread pool.
        """
        if self.is_open():
            return

        connection = self.__connection_resolver.resolve(correlation_id)
        self.__uri = connection.get_uri()
        try:
            self.__connection_resolver.register(correlation_id)

            credentials = None

            if connection.get_protocol_with_default('http') == 'https':
                ssl_key_file = connection.get_as_nullable_string('ssl_key_file')
                ssl_crt_file = connection.get_as_nullable_string('ssl_crt_file')

                with open(ssl_key_file, 'rb') as file:
                    private_key = file.read()

                with open(ssl_crt_file, 'rb') as file:
                    certificate = file.read()

                credentials = grpc.ssl_server_credentials(((private_key, certificate),))

            # Create instance of express application
            if len(self.__interceptors) > 0:
                self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers),
                                            interceptors=self.__interceptors)
            else:
                self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

            if credentials:
                self.__server.add_secure_port(str(connection.get_host()) + ':' +
                                              str(connection.get_port()), credentials)
            else:
                self.__server.add_insecure_port(str(connection.get_host()) + ':' + str(connection.get_port()))
            # Start operations
            self.__server.start()
            self.__connection_resolver.register(correlation_id)
            self.__perform_registrations()
            self.__logger.debug(correlation_id, 'Opened GRPC service at {}'.format(self.__uri))

        except Exception as ex:
            self.__server = None
            err = ConnectionException(correlation_id, 'CANNOT_CONNECT', 'Opening GRPC service failed').wrap(
                ex).with_details('url', self.__uri)
            raise err

    def close(self, correlation_id):
        """
        Closes this endpoint and the GRPC server (service) that was opened earlier.
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self.__server is not None:
            self.__uri = None
            self.__commandable_methods = None
            self.__commandable_schemas = None
            self.__commandable_service = None

            # Eat exceptions
            try:
                self.__server.stop(None)
                self.__logger.debug(correlation_id, 'Closed GRPC service at {}'.format(self.__uri))
                self.__server = None
                GrpcEndpoint.__interceptors = []
                GrpcEndpoint.__registrations = []
                GrpcEndpoint.__connection_resolver = HttpConnectionResolver()
            except Exception as ex:
                self.__logger.warn(correlation_id, 'Failed while closing GRPC service: '.format(ex))

    def register(self, registration):
        """
        Registers a registerable object for dynamic endpoint discovery.

        :param registration: the registration to add.
        :return:
        """
        if registration is not None:
            self.__registrations.append(registration)

    def unregister(self, registration):
        """
        Unregisters a registerable object, so that it is no longer used in dynamic
        endpoint discovery.

        :param registration: the registration to remove.
        """
        self.__registrations = list(filter(lambda r: r == registration, self.__registrations))

    def __perform_registrations(self):
        for registration in self.__registrations:
            registration.register()

        self.__register_commandable_service()

    def __register_commandable_service(self):
        if self.__commandable_methods is None:
            return
        self.__commandable_service = _CommandableMediator()
        self.__commandable_service.invoke_func(self.__invoke_commandable_method)

        self.register_service(self.__commandable_service)

    def __invoke_commandable_method(self, request, context):
        method = request.method
        action = self.__commandable_methods[method] if self.__commandable_methods else None
        correlation_id = request.correlation_id
        response = commandable_pb2.InvokeReply()

        # Handle method not found
        if action is None:
            err = InvocationException(correlation_id, 'METHOD_NOT_FOUND',
                                      'Method ' + method + ' was not found').with_details('method', method)
            resp_err = ErrorDescriptionFactory.create(err)
            response.error = commandable_pb2.ErrorDescription()
            response.error.category = resp_err.category
            response.error.code = resp_err.code
            response.error.correlation_id = resp_err.correlation_id
            response.error.status = resp_err.status
            response.error.message = resp_err.message
            response.error.cause = resp_err.cause
            response.error.stack_trace = resp_err.stack_trace
            response.error.details.addAll(resp_err.details)
            response.resultEmpty = True
            response.resultJson = ''

            return response

        try:
            # Convert arguments
            args_empty = request.args_empty
            args_json = request.args_json
            args = Parameters.from_json(args_json) if not args_empty and args_json else Parameters()

            try:
                result = action(correlation_id, args, method)
                response.result_empty = result is None
                if type(result) is DataPage:
                    response.result_json = json.dumps(result.to_json())
                else:
                    response.result_json = json.dumps(result) if result is not None else ''

                # TODO: Validate schema
                schema = self.__commandable_schemas[method]
                if schema:
                    pass

            except Exception as ex:
                # Process result and generate response
                resp_err = ErrorDescriptionFactory.create(ex)
                response.error.category = resp_err.category
                response.error.code = resp_err.code
                response.error.correlation_id = resp_err.correlation_id
                response.error.status = resp_err.status
                response.error.message = resp_err.message
                response.error.cause = resp_err.cause
                response.error.stack_trace = resp_err.stack_trace
                response.error.details.update(resp_err.details)
                response.result_empty = True
                response.result_json = ''

        except Exception as ex:
            # Handle unexpected exception
            err = InvocationException(correlation_id, 'METHOD_FAILED', 'Method ' + method + ' failed').wrap(
                ex).with_details('method', method)
            resp_err = ErrorDescriptionFactory.create(err)
            response.error.category = resp_err.category
            response.error.code = resp_err.code
            response.error.correlation_id = resp_err.correlation_id
            response.error.status = resp_err.status
            response.error.message = resp_err.message
            response.error.cause = resp_err.cause
            response.error.stack_trace = resp_err.stack_trace
            response.error.details.update(resp_err.details)
            response.result_empty = True
            response.result_json = ''

        return response

    def register_service(self, service):
        """
        Registers a service with related implementation
        :param service: a GRPC service object.
        """
        service.add_servicer_to_server(self.__server)

    def register_commandable_method(self, method, schema, action):
        """
        Registers a commandable method in this objects GRPC server (service) by the given name.,

        :param method: the GRPC method name.
        :param schema: the schema to use for parameter validation.
        :param action: the action to perform at the given route.
        """
        self.__commandable_methods = self.__commandable_methods or {}
        self.__commandable_methods[method] = action

        self.__commandable_schemas = self.__commandable_schemas or {}
        self.__commandable_schemas[method] = schema

    def register_interceptor(self, interceptor):
        self.__interceptors.append(interceptor)
