# -*- coding: utf-8 -*-

from abc import ABC

from pip_services3_components.trace.TraceTiming import TraceTiming


class ITracer(ABC):
    """
    Interface for tracer components that capture operation traces.
    """

    def trace(self, correlation_id: str, component: str, operation: str, duration: int) -> None:
        """
        Records an operation trace with its name and duration

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :param duration: execution duration in milliseconds.
        """

    def failure(self, correlation_id: str, component: str, operation: str, error: [Exception, None], duration: int) -> None:
        """
        Records an operation failure with its name, duration and error

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :param error: an error object associated with this trace.
        :param duration: execution duration in milliseconds.
        """

    def begin_trace(self, correlation_id: str, component: str, operation: str) -> TraceTiming:
        """
        Begings recording an operation trace

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :return: a trace timing object.
        """
