# -*- coding: utf-8 -*-

import json

from pip_services3_commons.data.DataPage import DataPage
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams

from ..protos import dummies_pb2_grpc
from ..protos import dummies_pb2

from pip_services3_grpc.clients.GrpcClient import GrpcClient
from .IDummyClient import IDummyClient
from ..Dummy import Dummy


class DummyGrpcClient(GrpcClient, IDummyClient):
    __client = None

    def __init__(self):
        super().__init__('dummies.Dummies')
        self.__client = dummies_pb2_grpc.DummiesStub

    def get_dummies(self, correlation_id, filter, paging):
        request = dummies_pb2.DummiesPageRequest()
        request.correlation_id = correlation_id
        if filter is not None:
            request.filter.update(filter.values())

        if paging is not None:
            request.paging.total = paging.total
            request.paging.skip += paging.skip
            request.paging.take = paging.take

        response = self.call('get_dummies', self.__client, request)
        self._instrument(correlation_id, 'dummy.get_page_by_filter')
        items = []
        for item in response.data:
            items.append(item)

        return DataPage(items, int(response.total))

    def get_dummy_by_id(self, correlation_id, dummy_id):
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        response = self.call('get_dummy_by_id', self.__client, request)
        self._instrument(correlation_id, 'dummy.get_one_by_id')
        result = Dummy(response.id, response.key, response.content)
        if response is not None and response.id == '' and response.key == '':
            result = None

        return result

    def create_dummy(self, correlation_id, dummy):
        request = dummies_pb2.DummyObjectRequest()
        request.correlation_id = correlation_id

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        response = self.call('create_dummy', self.__client, request)

        self._instrument(correlation_id, 'dummy.create')

        result = Dummy(response.id, response.key, response.content)
        if response is not None and response.id == '' and response.key == '':
            result = None

        return result

    def update_dummy(self, correlation_id, dummy):
        request = dummies_pb2.DummyObjectRequest()
        request.correlation_id = correlation_id

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        response = self.call('update_dummy', self.__client, request)

        self._instrument(correlation_id, 'dummy.update')
        result = Dummy(response.id, response.key, response.content)
        if response is not None and response.id == '' and response.key == '':
            result = None

        return result

    def delete_dummy(self, correlation_id, dummy_id):
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        response = self.call('delete_dummy_by_id', self.__client, request)

        self._instrument(correlation_id, 'dummy.delete')

        result = Dummy(response.id, response.key, response.content)
        if response is not None and response.id == '' and response.key == '':
            result = None

        return result
