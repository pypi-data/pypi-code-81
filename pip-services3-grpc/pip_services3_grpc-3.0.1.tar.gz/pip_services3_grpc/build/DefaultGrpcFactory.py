# -*- coding: utf-8 -*-

from pip_services3_components.build.Factory import Factory
from pip_services3_commons.refer.Descriptor import Descriptor

from ..services.GrpcEndpoint import GrpcEndpoint


class DefaultGrpcFactory(Factory):
    """
    Creates GRPC components by their descriptors.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`, :class:`GrpcEndpoint <pip_services3_grpc.services.GrpcEndpoint.GrpcEndpoint>`, :class:`HeartbeatGrpcService <pip_services3_grpc.services.HeartbeatGrpcService.HeartbeatGrpcService>`, :class:`StatusGrpcService <pip_services3_grpc.services.StatusGrpcService.StatusGrpcService>`
    """
    DESCRIPTOR = Descriptor("pip-services", "factory", "grpc", "default", "1.0")
    GrpcEndpointDescriptor = Descriptor("pip-services", "endpoint", "grpc", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        self.register_as_type(DefaultGrpcFactory.GrpcEndpointDescriptor, GrpcEndpoint)
