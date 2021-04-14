from __future__ import print_function

import hashlib
import os
import struct
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from copy import copy
from uuid import uuid4

import SharedArray as sa
import grpc
import numpy as np
import requests
import urllib3

from deci_client.rtic import InferencerApi, DefaultApi
from deci_client.rtic import __version__ as RTIC_CLIENT_VERSION
from deci_client.rtic.api_client import ApiClient
from deci_client.rtic.configuration import Configuration
from deci_client.rtic.exceptions import ApiException
from deci_client.rtic.serialization.numpy_serializer import ClientNumpySerializer
from deci_client.rtic.serialization.protobuf.rtic_server_pb2_grpc import RTiCStub
from deci_client.rtic.serialization.protobuf_serializer import NumpyProtobufSerializer


def get_docstring_from(original_function):
    """
    A decorator that attaches the docstring one function to another function in real time (for transparent auto completion).
    """

    def doc_wrapper(target):
        target.__doc__ = original_function.__doc__
        return target

    return doc_wrapper


def md5(value):
    encoded_utf_8_val = value.encode('utf-8')
    h = hashlib.md5(encoded_utf_8_val).hexdigest()
    return h[:8]


class InferenceResponse(object):
    def __init__(self, model_forward_pass_time_ms, server_process_time_ms, data):
        """
        An inference response.
        :param model_forward_pass_time_ms: The time it took for the model forward pass.
        :type model_forward_pass_time_ms: str
        :param server_process_time_ms: The time it took for the http server to process, analyze and return the response (EXCLUDING network latency).
        :type server_process_time_ms: str
        :param data: A list of the model outputs.
        :type data: list
        """
        self.model_forward_pass_time_ms = model_forward_pass_time_ms
        self.server_process_time_ms = server_process_time_ms
        self.data = data


class SharedMemoryTensorsProvider(object):
    def _change_shm_file_ownership(self, result_ipc_path):
        # Making the ipc path available to other machines/containers/namespaces
        try:
            if sys.platform.startswith('linux'):
                os_shm_absolute_path = result_ipc_path.split('file://')[1]
                os.chmod(os_shm_absolute_path, 0o777)
        except OSError as e:
            print('Failed to chmod the ipc path for the inference result: {}'.format(e))

    def initialize_shared_memory_inputs(self, model_name, model_inputs):
        """
        Initializes (creates) an shared input array for inference, with the specified name.
        If the shared array already exists, It is attached and returned without re-creation, as long as the batch size
        (dimensions) were not changed.
        :return: A tuple of the shared arrays (in the length of the input), and the shared array's absolute file path.
        :rtype: tuple
        """
        # Creating a unique shared resource for this inference call
        random_suffix = str(uuid4())[:8]
        inference_session_input_tensor_name = '-'.join([model_name, random_suffix])
        shared_tensors_paths = []
        shared_tensors = []
        models_to_copy_to_shm = model_inputs
        if not isinstance(model_inputs, list):
            models_to_copy_to_shm = [model_inputs]
        for i, tensor in enumerate(models_to_copy_to_shm):
            tensor_shm_name = inference_session_input_tensor_name + f'_{i}'
            shared_tensor_path = None
            # TODO: Replace md5 with something lighter and faster to gain more speed
            if sys.platform.startswith('linux'):
                shared_tensor_path = 'file:///dev/shm/deci/{}'.format(md5(tensor_shm_name))
            elif sys.platform == 'darwin':
                shared_tensor_path = 'shm://{}'.format(md5(tensor_shm_name))
            try:
                sa.delete(inference_session_input_tensor_name)
            except OSError:
                pass

            shared_tensor = sa.create(shared_tensor_path, tensor.shape, tensor.dtype)
            self._change_shm_file_ownership(shared_tensor_path)
            shared_tensors.append(shared_tensor)
            shared_tensors_paths.append(shared_tensor_path)
        return shared_tensors, shared_tensors_paths

    def initialize_shared_memory_outputs(self, output_tensors_paths):
        """
        Attaches a shared array from the specified path.
        If the array is already attached - It is returned without re-attachment.
        :rtype: sa.SharedArray
        """
        output_tensors_paths = output_tensors_paths.split(',')
        shared_tensors = []
        for output_tensor_name in output_tensors_paths:
            output_tensor = sa.attach(output_tensor_name)
            shared_tensors.append(output_tensor)
        return shared_tensors, output_tensors_paths

    def release_tensor(self, shared_tensor_path):
        """
        Releases (deleted) a tensor resource from the shared memory.
        """
        try:
            sa.delete(shared_tensor_path)
        except OSError as e:
            print('Failed to release a tensor resource on the shared memory: {}'.format(e))

    def is_ipc_supported(self):
        """
        Checks that the shared memory folder is readable and writable.
        return: True if /dev/shm has both read & write permissions,
                False otherwise.
        """
        return os.access('/dev/shm/deci/', os.W_OK) \
               and os.access('/dev/shm/deci/', os.R_OK) \
               and os.access('/dev/shm/deci/', os.X_OK)


class DeciRTICClient:
    """
    A wrapper for OpenAPI's generated client http library to deci's API.
    Extends the functionality of generated clients and eases their use.
    """

    def __init__(self, api_host='localhost', api_port=8000, grpc_port=8001, https=False, max_workers=None,
                 shared_tensor_provider=None):
        """
        :param api_host: The host of deci's inferencer HTTP API.
        :type api_host: str
        :param api_host: The port of deci's inferencer HTTP API.
        :type api_port: int
        :param https: Whether to use https instead of HTTP. Using https Will add latency.
        :type https: bool
        :param max_workers: The maximum amount of workers for the predict thread pool.
                            Larger numbers will allow more asynchronous predict requests to be sent to the server.
                            The requests are queued, and by that we to reduce network latency and keep the GPUs closer 100% capacity.
        """
        assert isinstance(api_port, int), 'The api_port must be an int object'
        endpoint_host = '{api_host}:{api_port}'.format(api_host=api_host, api_port=api_port)
        self._api_host = api_host
        self._endpoint_host = endpoint_host
        if https:
            base_url = 'https://{endpoint}'.format(endpoint=endpoint_host)
        else:
            base_url = 'http://{endpoint}'.format(endpoint=endpoint_host)

        self._base_url = base_url
        client_config = ApiClient(configuration=Configuration(host=base_url))
        self.__api = InferencerApi(client_config)

        # Checking the client version
        self._assert_server_version(client_config)
        self._inference_session = requests.Session()

        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

        # IPC Shared Memory tensors for predict async thread safety
        self._thread_pool_size = self._thread_pool._max_workers
        self._shared_tensors_provider = shared_tensor_provider or SharedMemoryTensorsProvider()

        # GRPC Initialization
        max_message_size = 2 ** (struct.Struct('i').size * 8 - 1) - 1
        channel_options = [('grpc.max_receive_message_length',
                            max_message_size),
                           ('grpc.max_send_message_length', max_message_size)]
        channel = grpc.insecure_channel(f'{api_host}:{grpc_port}', options=channel_options)
        stub = RTiCStub(channel)
        self._grpc_stub = stub

        # A cache for the chosen transport for inference (str), per model name (str, key);
        self._transport_mapping = {}

        # A dictionary that holds a method for inference (predict), per transport type (key).
        self._transport_inference_methods = {'http': self._run_predict_http,
                                             'ipc': self._run_predict_ipc,
                                             'grpc': self._run_predict_grpc}

    @get_docstring_from(DefaultApi().get_rtic_version_version_get)
    def _assert_server_version(self, client_config):
        """
        Checks the server version.
        If the server version is not compatible with the current client version, a warning will be logged.
        Major verisons are not backwards-compatible, and Minor versions are backwards-compatible for the same Major version.
        For instance, if the server version is 0.1.3 and the client version is v0.1.1, they are compatible.
        For instance, if the server version is 1.0.0 and the client version is 0.9.8, they are compatible.
        """
        try:
            rtic_version = DefaultApi(client_config).get_rtic_version_version_get().data
            rtic_major = rtic_version.split('.')[0]
            client_major = RTIC_CLIENT_VERSION.split('.')[0]
            supported_client_versions = '{0}.x.x'.format(rtic_major)
            if rtic_major != client_major:
                print(RuntimeWarning(
                    'The RTiC Server API Version: {rtic_version} is not compatible with the current client version: {RTIC_CLIENT_VERSION}. Please use a matching client version ({supported_client_versions}, prefferbly {rtic_version}) in order to experience consistent results.'.format(
                        rtic_version=rtic_version, RTIC_CLIENT_VERSION=RTIC_CLIENT_VERSION,
                        supported_client_versions=supported_client_versions
                    )))
        except urllib3.exceptions.HTTPError as e:
            print(RuntimeWarning(
                'The RTiC Server is not running, or it is unreachable: {base_url}: {e}'.format(base_url=self._base_url,
                                                                                               e=e)))

    @get_docstring_from(InferencerApi().register_model)
    def register_model(self,
                       model_name,
                       framework_type,
                       inference_hardware,
                       model_weights_source,
                       weights_path,
                       tensorflow_input_layer_name='',
                       tensorflow_output_layer_name='',
                       transport='http',
                       deploy_async=True,
                       **kwargs):
        """

        :param model_name: The name to give to the model.
        :type model_name: str
        :param framework_type: The framework type. To find which frameworks are supported on your inferencer, Please visit it's live documentation via http://<inference_host>:<inference_port>/redoc .
        :type framework_type: str
        :param inference_hardware: The Inference Hardware.
        :type framework_type: str
        :param model_weights_source: The source of the model weights.
        :type model_weights_source: str
        :param weights_path: The path (or link) to the weights.
        :type weights_path: str
        :param tensorflow_input_layer_name: The input layer name in tensorflow. Must be speficied only when using tensorflow as framework type. Must be None otherwise.
        :type tensorflow_input_layer_name: str
        :param tensorflow_output_layer_name: The output layer name in tensorflow. Must be speficied only when using tensorflow as framework type. Must be None otherwise.
        :type tensorflow_output_layer_name: str
        :param transport: The transport protocol that will be used for inference. For non-localhost deployments, The default is IPC. Otherwise the default is HTTP. Consider using IPC (Inner-Process-Communication using shared memory) for big batch sizes, to prevent network (TCP) overhead.
        :type transport: str
        :param deploy_async:
             Whether to wait for the model to be in state 'available' (sync), or deploy it in the background (async).
             If set to True (default) - The http response will be sent right away, with the state 'deploying'.
             If set to False, The response will return only when the model reaches 'available' state. Please take HTTP Timeouts into account when using this flag.
        :type deploy_async: bool
        :param shared_memory_inference: When set to True, if the inference
        :return: APIResponse
        :raises ApiException: If anything went wrong during the model registration.
        """
        if transport == 'ipc':
            if not self._shared_tensors_provider.is_ipc_supported():
                print('IPC transport will probably not work, because /dev/shm is not readable/writable.')
        response = self.__api.register_model(model_name=model_name,
                                             framework_type=framework_type,
                                             inference_hardware=inference_hardware,
                                             model_weights_source=model_weights_source,
                                             weights_path=weights_path,
                                             tensorflow_input_layer_name=tensorflow_input_layer_name,
                                             tensorflow_output_layer_name=tensorflow_output_layer_name,
                                             deploy_async=deploy_async,
                                             transport=transport,
                                             **kwargs)

        return response

    @get_docstring_from(InferencerApi().register_model_from_repository)
    def register_model_from_repository(self,
                                       model_name,
                                       model_id,
                                       deploy_async=True,
                                       **kwargs):
        response = self.__api.register_model_from_repository(model_id=model_id,
                                                             model_name=model_name,
                                                             deploy_async=deploy_async,
                                                             **kwargs)
        return response

    @get_docstring_from(InferencerApi().de_register_model)
    def deregister_model(self, model_name, **kwargs):
        return self.__api.de_register_model(model_name=model_name, **kwargs)

    @get_docstring_from(InferencerApi().list_registered_models)
    def get_all_models(self, **kwargs):
        return self.__api.list_registered_models(**kwargs)

    @get_docstring_from(InferencerApi().get_model)
    def get_model(self, model_name, **kwargs):
        return self.__api.get_model(model_name=model_name, **kwargs)

    @get_docstring_from(InferencerApi().measure)
    def measure(self, model_name, batch_size, input_dims, **kwargs):
        return self.__api.measure(model_name=model_name, batch_size=batch_size,
                                  input_dims=input_dims, **kwargs)

    def _run_predict_http(self, predict_endpoint_url, model_input, headers, **kwargs) -> InferenceResponse:
        try:
            http_response = self._inference_session.post(predict_endpoint_url,
                                                         headers=headers,
                                                         data=ClientNumpySerializer.serialize(model_input))
            http_response.raise_for_status()
            model_output = ClientNumpySerializer.deserialize(http_response.content)
            server_process_time_ms = http_response.headers['deci-server-process-time-ms']
            model_forward_pass_time_ms = http_response.headers['model-forward-pass-time-ms']
            inference_response = InferenceResponse(data=model_output,
                                                   # The time took for the model to process the np.array and predict the output.
                                                   model_forward_pass_time_ms=model_forward_pass_time_ms,
                                                   # The time took for the server to process the output np.array, deserialize it, and return a HTTP response with the outputs:
                                                   server_process_time_ms=server_process_time_ms)
            return inference_response
        except struct.error:
            # Numpy De-Serialization failed, therefore, the server sent a json response.
            print('Failed to deserialize output array - decoding as JSON')
            model_output = http_response.json()
            raise ApiException(status=http_response.status_code,
                               reason=model_output['message'],
                               http_resp=http_response)
        except requests.HTTPError:
            # Other HTTP Error codes (400, 404, 422, 500):
            # Converting the request response to ApiException (should be raised by the original unwrapped predict() function).
            raise ApiException(status=http_response.status_code, reason=http_response.reason, http_resp=http_response)

    def _run_predict_ipc(self, predict_endpoint_url, model_name, model_input, headers, **kwargs) -> InferenceResponse:
        try:
            if sys.platform == 'darwin':
                print('[WARNING] - IPC is not officially supported on Mac OS clients.')

            shared_input_tensors, shared_input_tensors_paths = self._shared_tensors_provider.initialize_shared_memory_inputs(
                model_name,
                model_input)
            headers['x-shared-memory-path'] = ','.join(shared_input_tensors_paths)

            # Copying (uploading) the tensors data to the shared arrays
            inputs_to_copy = model_input
            if not isinstance(model_input, list):
                inputs_to_copy = [model_input]
            for _input, shared_tensor in zip(inputs_to_copy, shared_input_tensors):
                shared_tensor[:] = _input

            # Running the http call with the shared tensors paths in the headers.
            http_response = self._inference_session.post(predict_endpoint_url,
                                                         headers=headers,
                                                         data=None)
            http_response.raise_for_status()

            # Getting the shared memory tensors names from the HTTP response header
            outputs_shared_memory_paths = http_response.headers.get('x-shared-memory-path')
            output_tensors, output_tensors_paths = self._shared_tensors_provider.initialize_shared_memory_outputs(
                outputs_shared_memory_paths)
            model_outputs = [copy(t) for t in output_tensors]

            # Deleting both input & output tensors from the SHM
            [self._shared_tensors_provider.release_tensor(tensor_path) for tensor_path in shared_input_tensors_paths]
            [self._shared_tensors_provider.release_tensor(tensor_path) for tensor_path in output_tensors_paths]

            # Creating the response model
            server_process_time_ms = http_response.headers['deci-server-process-time-ms']
            model_forward_pass_time_ms = http_response.headers['model-forward-pass-time-ms']
            inference_response = InferenceResponse(data=model_outputs,
                                                   # The time took for the model to process the np.array and predict the output.
                                                   model_forward_pass_time_ms=model_forward_pass_time_ms,
                                                   # The time took for the server to process the output np.array, deserialize it, and return a HTTP response with the outputs:
                                                   server_process_time_ms=server_process_time_ms)
            return inference_response
        except requests.HTTPError:
            # Other HTTP Error codes (400, 404, 422, 500):
            # Converting the request response to ApiException (should be raised by the original unwrapped predict() function).
            raise ApiException(status=http_response.status_code, reason=http_response.reason, http_resp=http_response)

    def _run_predict_grpc(self, model_name, model_input, **kwargs) -> InferenceResponse:
        tic = time.time()
        predict_request = NumpyProtobufSerializer.serialize_request(model_name=model_name,
                                                                    inputs=model_input)
        toc = time.time()
        print('Serialized protobuf in {}ms'.format((toc - tic) * 1000))
        grpc_response = self._grpc_stub.predict(predict_request)
        tic = time.time()
        # TODO: Update NumpyProtobufSerializer after deci2 tests
        model_output = NumpyProtobufSerializer.deserialize_from_response(message=grpc_response)
        toc = time.time()
        print('Deserialized protobuf in {}ms'.format((toc - tic) * 1000))
        model_forward_pass_time_ms = str(grpc_response.model_forward_pass_time_ms)
        server_process_time_ms = str(grpc_response.server_process_time_ms)
        inference_response = InferenceResponse(data=model_output,
                                               # The time took for the model to process the np.array and predict the output.
                                               model_forward_pass_time_ms=model_forward_pass_time_ms,
                                               # The time took for the server to process the output np.array, deserialize it, and return a HTTP response with the outputs:
                                               server_process_time_ms=server_process_time_ms)
        return inference_response

    def predict(self, model_name,
                model_input,
                transport=None,
                api_version='v1',
                **kwargs):
        """
        Predict - Performs inference on a loaded model with a given name.
        Predict - Classify (Infer) input tensors. The input is serialized and sent in different serializers/protocols, depending on the transport.
         Please use this endpoint for maximum results.
        :param model_name: The unique name of the model, that was specified in "register" api call.
        :type model_name: str
        :param model_input: In the shape of the model's input layer. For example, a numpy ndarray with shape (1, 3, 224, 224).
        :type model_input: np.ndarray
        :param transport: The transport protocol that will be used for inference. For non-localhost deployments, The default is IPC. Otherwise the default is HTTP. Consider using IPC (Inner-Process-Communication using shared memory) for big batch sizes, to prevent network (TCP) overhead.
        :type transport: str
        :param api_version: The api version to use.
        :raises ApiError: If the predict API Failed for any reason.
        """
        if not isinstance(model_input, np.ndarray):
            raise ValueError('Error - Model input must be a numpy ndarray')

        transport = self._choose_transport_protocol(model_name, transport)
        predict_endpoint_url = self.__api.api_client.configuration.host + '/{api_version}/predict/{model_name}'.format(
            api_version=api_version, model_name=model_name)
        headers = {'x-deci-transport': transport}

        # Invoking the inference request, depending on the pre-defined transport
        predict_method = self._transport_inference_methods.get(transport)
        if not predict_method:
            raise ValueError('Unsupported transport: {}'.format(transport))

        # Passing keyword arguments to the functions, to every function can define arguments that it really uses.
        inference_response = predict_method(predict_endpoint_url=predict_endpoint_url,
                                            model_name=model_name,
                                            model_input=model_input,
                                            headers=headers)
        return inference_response

    def _choose_transport_protocol(self, model_name, transport):
        """
        Assigns the DataTransportProtocol - If self._api_host is localhost, assigns IPC as default.
        :param transport: The pre-defined DataTransportProtocol Protocol
        :type transport: str
        :return:
        """
        if transport is None:
            if self._api_host in ['localhost', '127.0.0.1', '0.0.0.0']:
                transport = 'ipc'
            else:
                transport = self._transport_mapping.get(model_name)
                if not transport:
                    # Getting the transport from the model registration,
                    # and caching it as default when 'transport' is not specified.
                    model_metadata = self.get_model(model_name=model_name)
                    transport = model_metadata.data.transport
                    self._transport_mapping[model_name] = transport
        return transport

    def predict_async(self, model_name, model_input, transport=None, api_version='v1'):
        """
        Preforms a predict operation using async event loop, for concurrent execution.
        Classify (Infer) input tensors asynchronously. The HTTP request body sends the input tensor, serialized with deci's custom serialization.
        Please use this endpoint when working with asyncio, python3 async/await or other concurrent client libraries.

        :param model_name: The unique name of the model, that was specified in "register" api call.
        :type model_name: str
        :param model_input: A np.ndarray In the shape of the model's input layer. For example, a numpy ndarray with shape (1, 3, 224, 224).
        :type model_input: np.ndarray
        :param transport: The transport protocol that will be used for inference. For non-localhost deployments, The default is IPC. Otherwise the default is HTTP. Consider using IPC (Inner-Process-Communication using shared memory) for big batch sizes, to prevent network (TCP) overhead.
        :type transport: str
        :param api_version: The api version to use.
        :type api_version: str

        :returns: A concurrent.Future object of with the predict() operation. The result of the Future is an InferenceResponse object.
        :trype: InferenceResponse
        :example:
        >>> predict_job = client.predict_async(model_name='my_model', model_input=np.ones((3,224,224), dtype=np.float32, **kwargs)
        >>> prediction = predict_job.result(timeout=5)
        """
        predict_job = self._thread_pool.submit(self.predict,
                                               model_name=model_name,
                                               model_input=model_input,
                                               transport=transport,
                                               api_version=api_version)

        return predict_job

    @get_docstring_from(InferencerApi().set_platform_api_key)
    def set_platform_api_key(self, api_key):
        response = self.__api.set_platform_api_key(token=api_key)
        return response
