"""
This module contains all custom exceptions raised by PyProcSync.
"""


class ProcSyncError(BaseException):
    """
    Base class for all exceptions in PyProcSync.
    """
    pass


class TooLateError(ProcSyncError):
    """
    This exception is raised when the announced continue time is already passed.
    That could be caused by high network latency or unsynchronized system clocks between nodes.
    """
    pass


class TimeOutError(ProcSyncError):
    """
    This exception is raised when the node is gave up waiting for other nodes.
    This could caused by other nodes crashed or bad configuration.
    """
    pass
