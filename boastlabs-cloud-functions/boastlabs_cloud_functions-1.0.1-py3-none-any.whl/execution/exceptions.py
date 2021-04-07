class ExecutionNotAllowed(Exception):

    def __init__(self):
        super().__init__('Execution Not Allowed!')


class SleepException(Exception):

    def __init__(self):
        super().__init__('Awaiting sleep!')


class RetryException(Exception):

    def __init__(self):
        super().__init__('Awaiting retry!')


class TimeoutException(RetryException):
    pass
