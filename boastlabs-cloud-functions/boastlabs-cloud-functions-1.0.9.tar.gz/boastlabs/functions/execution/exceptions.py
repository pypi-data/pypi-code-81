class HandlerNotFoundException(Exception):

    def __init__(self, event_type):
        Exception.__init__(self, f'No handler found for event type <{event_type}>.')


class DocumentNotFoundException(Exception):

    def __init__(self, doc_path):
        Exception.__init__(self, f'No document found for path <{doc_path}>')


class IncompatibleApiVersionException(Exception):

    def __init__(self, found_api_version, current_api_version):
        Exception.__init__(self, f'Incompatible api version. Found <{found_api_version}>. '
                                 f'Current version: <{current_api_version}>')


class ExecutionNotAllowedException(Exception):
    pass


class SleepException(Exception):

    def __init__(self):
        super().__init__('Awaiting sleep!')


class RetryException(Exception):

    def __init__(self):
        super().__init__('Awaiting retry!')


class TimeoutException(RetryException):
    pass
