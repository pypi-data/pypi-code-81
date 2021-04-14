# -*- coding: utf-8 -*-

from pip_services3_commons.refer.Descriptor import Descriptor
from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_commons.refer.References import References

from ..DummyController import DummyController
from ..services.DummyGrpcService import DummyGrpcService
from .DummyGrpcClient import DummyGrpcClient
from .DummyClientFixture import DummyClientFixture

grpc_config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost",
    "connection.port", 3000
)


class TestDummyGrpcClient:
    service = None
    client = None
    fixture = None

    @classmethod
    def setup_class(cls):
        ctrl = DummyController()

        cls.service = DummyGrpcService()
        cls.service.configure(grpc_config)

        references = References.from_tuples(
            Descriptor(
                'pip-services-dummies', 'controller', 'default', 'default', '1.0'),
            ctrl,
            Descriptor('pip-services-dummies', 'service', 'grpc', 'default', '1.0'),
            cls.service
        )

        cls.service.set_references(references)

        cls.service.open(None)

    @classmethod
    def teardown_class(cls):
        cls.service.close(None)

    def setup_method(self, method=None):
        self.client = DummyGrpcClient()
        self.fixture = DummyClientFixture(self.client)

        self.client.configure(grpc_config)
        self.client.set_references(References())
        self.client.open(None)

    def teardown_method(self, method=None):
        self.client.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
