# -*- coding: utf-8 -*-

import json

from pip_services3_commons.data.DataPage import DataPage
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams

from ..protos import dummies_pb2_grpc
from ..protos import dummies_pb2

from pip_services3_grpc.clients.GrpcClient import GrpcClient
from pip_services3_grpc.clients.CommandableGrpcClient import CommandableGrpcClient

from .IDummyClient import IDummyClient
from ..Dummy import Dummy


class DummyCommandableGrpcClient(CommandableGrpcClient, IDummyClient):

    def __init__(self):
        super().__init__('dummy')

    def get_dummies(self, correlation_id, filter, paging):
        response = self.call_command('get_dummies', correlation_id, {'filter': filter, 'paging': paging})
        if response is None:
            return None

        response = json.loads(response)

        return DataPage.from_json(response)

    def get_dummy_by_id(self, correlation_id, dummy_id):
        response = self.call_command('get_dummy_by_id', correlation_id, {'dummy_id': dummy_id})
        if response is None:
            return None

        response = json.loads(response)

        return Dummy(response['id'], response['key'], response['content'])

    def create_dummy(self, correlation_id, dummy):
        response = self.call_command('create_dummy', correlation_id, {'dummy': dummy})
        if response is None:
            return None

        response = json.loads(response)

        return Dummy(response['id'], response['key'], response['content'])

    def update_dummy(self, correlation_id, dummy):
        response = self.call_command('update_dummy', correlation_id, {'dummy': dummy})
        if response is None:
            return None

        response = json.loads(response)

        return Dummy(response['id'], response['key'], response['content'])

    def delete_dummy(self, correlation_id, dummy_id):
        response = self.call_command('delete_dummy', correlation_id, {'dummy_id': dummy_id})
        if response is None:
            return None

        response = json.loads(response)

        return Dummy(response['id'], response['key'], response['content'])
