class SchedulerRunningError(BaseException):
    pass


class SchedulerExecutionError(TypeError):
    pass


class DuplicateJobError(BaseException):
    pass


class PrototypeFunctionError(BaseException):
    pass