# -*- coding: utf-8 -*-

import json
import time
import grpc

import requests
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor
from pip_services3_commons.run import Parameters
from pip_services3_commons.data import IdGenerator

import pip_services3_grpc.protos.commandable_pb2_grpc as commandable_pb2_grpc
import pip_services3_grpc.protos.commandable_pb2 as commandable_pb2

from ..Dummy import Dummy
from ..DummyController import DummyController
from .DummyCommandableGrpcService import DummyCommandableGrpcService

port = 3001
grpc_config = ConfigParams.from_tuples(
    'connection.protocol',
    'http',
    'connection.host',
    'localhost',
    'connection.port',
    port
)

DUMMY1 = Dummy('1', 'Key 1', 'Content 1')
DUMMY2 = Dummy('2', 'Key 2', 'Content 2')


class TestDummyCommandableGrpcService():
    controller = None
    service = None
    client = None
    chanel = None

    @classmethod
    def setup_class(cls):
        cls.controller = DummyController()

        cls.service = DummyCommandableGrpcService()
        cls.service.configure(grpc_config)

        cls.references = References.from_tuples(
            Descriptor('pip-services-dummies', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-services-dummies', 'service', 'grpc', 'default', '1.0'), cls.service
        )

        cls.service.set_references(cls.references)
        cls.service.open(None)

    @classmethod
    def teardown_class(cls, method=None):
        cls.service.close(None)

    def setup_method(self, method=None):
        self.chanel = grpc.insecure_channel('localhost:' + str(port))
        self.client = commandable_pb2_grpc.CommandableStub(self.chanel)

    def teardown_method(self, method=None):
        self.chanel.close()

    def test_crud_operations(self):
        # Create one dummy
        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.create_dummy'
        request.args_empty = False
        request.args_json = json.dumps({'dummy': {'id': DUMMY1.id, 'key': DUMMY1.key, 'content': DUMMY1.content}})

        response = self.client.invoke(request)

        assert response.result_empty is False
        assert response.result_json is not None
        response_obj = json.loads(response.result_json)
        assert response_obj is not None
        assert response_obj['content'] == DUMMY1.content
        assert response_obj['key'] == DUMMY1.key

        # Create another dummy
        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.create_dummy'
        request.args_empty = False
        request.args_json = json.dumps({'dummy': {'id': DUMMY2.id, 'key': DUMMY2.key, 'content': DUMMY2.content}})

        response = self.client.invoke(request)

        assert response.result_empty is False
        assert response.result_json is not None
        response_obj = json.loads(response.result_json)
        assert response_obj is not None
        assert response_obj['content'] == DUMMY2.content
        assert response_obj['key'] == DUMMY2.key

        # Get all dummies
        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.get_dummies'
        request.args_empty = False
        request.args_json = json.dumps({})

        response = self.client.invoke(request)

        assert response.result_empty is False
        assert response.result_json is not None
        dummies = json.loads(response.result_json)

        assert dummies is not None
        assert len(dummies['data']) == 2

        # Update the dummy
        dummy = DUMMY1
        dummy.content = 'Updated Content 1'

        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.update_dummy'
        request.args_empty = False
        request.args_json = json.dumps({'dummy': {'id': dummy.id, 'key': dummy.content, 'content': dummy.content}})

        response = self.client.invoke(request)

        assert response.result_empty is False
        assert response.result_json is not None

        response_obj = json.loads(response.result_json)
        dummy = Dummy(response_obj['id'], response_obj['key'], response_obj['content'])

        assert dummy is not None
        assert dummy.content == response_obj['content']
        assert dummy.key == response_obj['key']

        # Delete the dummy
        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.delete_dummy'
        request.args_empty = False
        request.args_json = json.dumps({'dummy_id': dummy.id})
        response = self.client.invoke(request)

        assert response.error.code is ''
        assert response.error.message is ''
        assert response.error.stack_trace is ''
        assert response.error.status == 0

        # Try to get deleted dummy
        request = commandable_pb2.InvokeRequest()
        request.correlation_id = '123'
        request.method = 'dummy.get_dummy_by_id'
        request.args_empty = False
        request.args_json = json.dumps({'dummy_id': dummy.id})

        response = self.client.invoke(request)

        assert response.error.code is ''
        assert response.error.message is ''
        assert response.error.stack_trace is ''
        assert response.error.status == 0
        assert response.result_empty is True

# if __name__ == '__main__':
#     test = TestDummyCommandableGrpcService()
#     test.setup_class()
#     test.setup_method()
#     test.test_crud_operations()
#     test.teardown_class()
