# -*- coding: utf-8 -*-

import time

from pip_services3_grpc.services.GrpcEndpoint import GrpcEndpoint
from pip_services3_commons.config.ConfigParams import ConfigParams

grpc_config = ConfigParams.from_tuples(
    'connection.protocol',
    'http',
    'connection.host',
    'localhost',
    'connection.port',
    3000
)


class TestGrpcEndpoint:
    endpoint = None

    @classmethod
    def setup_class(cls):
        cls.endpoint = GrpcEndpoint()
        cls.endpoint.configure(grpc_config)
        cls.endpoint.open(None)

    def test_is_open(self):
        assert self.endpoint.is_open() is True

    @classmethod
    def teardown_class(cls):
        cls.endpoint.close(None)
