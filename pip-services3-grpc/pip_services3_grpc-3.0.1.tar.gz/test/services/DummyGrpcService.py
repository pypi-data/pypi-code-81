# -*- coding: utf-8 -*-

import json
import grpc

from pip_services3_commons.validate.PagingParamsSchema import PagingParamsSchema
from pip_services3_commons.refer.IReferences import IReferences
from pip_services3_commons.refer.Descriptor import Descriptor
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams
from pip_services3_commons.validate.ObjectSchema import ObjectSchema
from pip_services3_commons.convert.TypeCode import TypeCode
from pip_services3_commons.validate.FilterParamsSchema import FilterParamsSchema
from pip_services3_commons.errors.ApplicationException import ApplicationException

import pip_services3_grpc.protos.commandable_pb2_grpc as commandable_pb2_grpc
import pip_services3_grpc.protos.commandable_pb2 as commandable_pb2

from ..protos import dummies_pb2
from ..protos import dummies_pb2_grpc

from ..Dummy import Dummy
from ..DummySchema import DummySchema
from pip_services3_grpc.services.GrpcService import GrpcService

from ..IDummyController import IDummyController


class DummyGrpcService(GrpcService, dummies_pb2_grpc.DummiesServicer):
    __controller = None
    __number_of_calls = 0

    def add_servicer_to_server(self, server):
        dummies_pb2_grpc.add_DummiesServicer_to_server(self, server)

    def __init__(self):
        self.service_name = 'dummies.Dummies.service'
        super().__init__(self.service_name)
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))

    def set_references(self, references):
        super().set_references(references)
        self.__controller = self._dependency_resolver.get_one_required('controller')

    def get_number_of_calls(self):
        return self.__number_of_calls

    def __increment_number_of_calls(self, request, method):
        self.__number_of_calls += 1
        return None

    def register(self):
        self._register_interceptor(self.__increment_number_of_calls)
        self._register_service(self)

    def create_dummy(self, request, context):
        schema = ObjectSchema().with_required_property('dummy', DummySchema())
        correlation_id = request.correlation_id
        err = schema.validate_and_throw_exception(correlation_id, request, False)

        if err is not None:
            raise err

        response = dummies_pb2.Dummy()

        timing = self._instrument(correlation_id, 'create_dummy.call')
        try:
            dummy_json = Dummy.from_grpc_to_json(request.dummy)
            result = self.__controller.create(request.correlation_id, dummy_json)
            timing.end_timing()
            if result is not None:
                response.id = result['id']
                response.content = result['content']
                response.key = result['key']
        except Exception as ex:
            timing.end_timing()
            err = ApplicationException().wrap(ex)
            self._instrument_error(correlation_id, 'create_dummy.call', err, True)

        return response

    def delete_dummy_by_id(self, request, contest):
        # TODO: add TypeCode.String
        schema = ObjectSchema().with_required_property('dummy_id', None)
        correlation_id = request.correlation_id
        err = schema.validate_and_throw_exception(correlation_id, request, False)

        if err is not None:
            raise err

        response = dummies_pb2.Dummy()
        timing = self._instrument(correlation_id, 'delete_dummy_by_id.call')
        try:
            result = self.__controller.delete_by_id(request.correlation_id, request.dummy_id)

            timing.end_timing()
            if result is not None:
                response.id = result['id']
                response.content = result['content']
                response.key = result['key']
        except Exception as ex:
            timing.end_timing()
            err = ApplicationException().wrap(ex)
            self._instrument_error(correlation_id, 'delete_dummy_by_id.call', err, True)

        return response

    def get_dummies(self, request, context):
        correlation_id = request.correlation_id

        filter = FilterParams.from_value(request.filter)
        paging = PagingParams.from_value(request.paging)
        response = dummies_pb2.DummiesPage()

        timing = self._instrument(correlation_id, 'get_dummies.call')

        try:
            result = self.__controller.get_page_by_filter(correlation_id, filter, paging)

            for item in result.data:
                dummy = dummies_pb2.Dummy()
                dummy.id = item['id']
                dummy.key = item['key']
                dummy.content = item['content']
                response.data.append(dummy)

            timing.end_timing()
            # Hack for set total value
            response.total += result.total

        except Exception as ex:
            err = ApplicationException().wrap(ex)
            timing.end_timing()
            self._instrument_error(correlation_id, 'get_dummies.call', err, True)

        return response

    def get_dummy_by_id(self, request, context):
        # TODO: add TypeCode.String
        schema = ObjectSchema().with_required_property('dummy_id', None)
        correlation_id = request.correlation_id
        err = schema.validate_and_throw_exception(correlation_id, request, False)

        if err is not None:
            raise err

        response = dummies_pb2.Dummy()
        timing = self._instrument(correlation_id, 'get_dummy_by_id.call')
        try:
            result = self.__controller.get_one_by_id(request.correlation_id, request.dummy_id)
            timing.end_timing()
            if result is not None:
                response.id = result['id']
                response.content = result['content']
                response.key = result['key']

        except Exception as ex:
            err = ApplicationException().wrap(ex)
            timing.end_timing()
            self._instrument_error(correlation_id, 'get_dummy_by_id.call', err, True)

        return response

    def update_dummy(self, request, context):
        schema = ObjectSchema().with_required_property('dummy', DummySchema())
        correlation_id = request.correlation_id
        err = schema.validate_and_throw_exception(correlation_id, request, False)

        if err is not None:
            raise err

        response = dummies_pb2.Dummy()
        timing = self._instrument(correlation_id, 'update_dummy.call')
        try:
            dummy_json = Dummy.from_grpc_to_json(request.dummy)
            result = self.__controller.update(request.correlation_id, dummy_json)
            timing.end_timing()
            if result is not None:
                response.id = result['id']
                response.content = result['content']
                response.key = result['key']
            timing.end_timing()

        except Exception as ex:
            err = ApplicationException().wrap(ex)
            timing.end_timing()
            self._instrument_error(correlation_id, 'update_dummy.call', err, True)

        return response
