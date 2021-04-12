from jsonschema import validate

from tinkoff_voicekit_client.STT import config_schema
from tinkoff_voicekit_client.STT.helper_stt import (
    get_proto_request,
    get_proto_longrunning_request,
    create_stream_requests
)
from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import BaseClient
from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.stt.v1.stt_pb2_grpc import SpeechToTextStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config, aud
from tinkoff_voicekit_client.speech_utils.infrastructure import get_buffer, dict_generator, response_format
from tinkoff_voicekit_client.speech_utils.metadata import Metadata
from tinkoff_voicekit_client.Uploader.uploader import Uploader


class ClientSTT(BaseClient):

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_stt"],
            port: int = client_config["port"],
            ssl_channel: bool = True,
            ca_file: str = None,
            uploader_config: dict = None
    ):
        """
        Create client for speech recognition.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech recognition host url
            :param port: Tinkoff Voicekit speech recognition port, default value: 443
            :param ca_file: optional certificate file
            :uploader_config: config for Uploader
        """
        super().__init__(host, port, ssl_channel, ca_file)
        self._metadata = Metadata(api_key, secret_key, aud=aud["stt"])
        self._api_key = api_key
        self._secret_key = secret_key
        self._stub = SpeechToTextStub(self._channel)

        uploader_config = {} if uploader_config is None else uploader_config
        self._uploader = Uploader(self._api_key, self._secret_key, **uploader_config)

    def recognize(self, source, config, metadata=None, dict_format=True, with_response_meta=False):
        """
        Recognize whole audio and then return all responses.
            :param source: path to audio file or buffer with audio
            :param config: dict conforming to recognition_config_schema
            :param dict_format: dict response instead of proto object
            :param with_response_meta: return response with metadata
            :param metadata: configure own metadata
        """
        validate(config, config_schema.recognition_config_schema)
        buffer = get_buffer(source)

        response, unary_obj = self._stub.Recognize.with_call(
            get_proto_request(buffer, config),
            metadata=metadata if metadata else self._metadata.metadata
        )

        response_meta = unary_obj.initial_metadata() if with_response_meta else None
        return response_format(response, dict_format, response_meta)

    def streaming_recognize(
            self,
            source,
            config,
            metadata=None,
            dict_format=True,
            with_response_meta=False,
            rps=20,
    ):
        """
        Recognize audio in streaming mode.
        Stream audio chunks to server and get streaming responses.
            :param source: path to audio file or audio stream
            :param config: dict conforming to streaming_recognition_config_schema
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
            :param with_response_meta: return response with metadata
            :param rps: configure rps for streaming requests
        """
        validate(config, config_schema.streaming_recognition_config_schema)
        buffer = get_buffer(source)

        responses = self._stub.StreamingRecognize(
            create_stream_requests(buffer, rps, config),
            metadata=metadata if metadata else self._metadata.metadata
        )

        if with_response_meta:
            return dict_generator(responses, dict_format), responses.initial_metadata()
        return dict_generator(responses, dict_format)

    def longrunning_recognize(self, source, config, dict_format=True, metadata=None, with_response_meta=False):
        """
        Recognize audio in long running mode.
            :param source: uri or buffer source
            :param config: dict conforming to long_running_recognition_schema
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
            :param with_response_meta: return response with metadata

        """
        validate(config, config_schema.long_running_recognition_config_schema)
        if self._uploader.is_storage_uri(source):
            buffer = source
        else:
            buffer = get_buffer(source)

        response, unary_obj = self._stub.LongRunningRecognize.with_call(
            get_proto_longrunning_request(buffer, config),
            metadata=metadata if metadata else self._metadata.metadata
        )

        response_meta = unary_obj.initial_metadata() if with_response_meta else None
        return response_format(response, dict_format, response_meta)

    def longrunning_recognize_with_uploader(
            self,
            source,
            config: dict,
            object_name: str = None,
            dict_format=True, metadata=None,
            with_response_meta=False,
    ):
        """
        Recognize audio in long running mode.
            :param source: path to audio or fileobj
            :param config: dict conforming to long_running_recognition_schema
            :param object_name: name for object in storage (default: 'default_name_<utcnow>')
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
            :param with_response_meta: return response with metadata
        """
        validate(config, config_schema.long_running_recognition_config_schema)
        uri = self._uploader.upload(source, object_name)

        response, unary_obj = self._stub.LongRunningRecognize.with_call(
            get_proto_longrunning_request(uri, config),
            metadata=metadata if metadata else self._metadata.metadata
        )
        if with_response_meta:
            response_meta = unary_obj.initial_metadata()
            return (*response_format(response, dict_format, response_meta), uri)
        else:
            return response_format(response, dict_format), uri
