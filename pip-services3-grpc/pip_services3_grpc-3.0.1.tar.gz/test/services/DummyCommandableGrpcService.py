# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_grpc.services.CommandableGrpcService import CommandableGrpcService


class DummyCommandableGrpcService(CommandableGrpcService):

    def __init__(self):
        super().__init__('dummy')
        self._dependency_resolver.put('controller', Descriptor('pip-services-dummies', 'controller', '*', '*', '*'))
