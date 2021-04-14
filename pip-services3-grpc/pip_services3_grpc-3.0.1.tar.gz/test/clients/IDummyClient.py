# -*- coding: utf-8 -*-

from abc import ABC


class IDummyClient(ABC):

    def get_dummies(self, correlation_id, filter, paging):
        raise NotImplementedError

    def get_dummy_by_id(self, correlation_id, dummy_id):
        raise NotImplementedError

    def create_dummy(self, correlation_id, dummy):
        raise NotImplementedError

    def update_dummy(self, correlation_id, dummy):
        raise NotImplementedError

    def delete_dummy(self, correlation_id, dummy_id):
        raise NotImplementedError
