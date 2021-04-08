class HandlerNotFoundException(Exception):

    def __init__(self, event_type, known_events):
        Exception.__init__(self, f'No value specified for field "event_type" or handler unknown'
                                 f' for value <{event_type}>. Known events: {known_events}')


class DocumentNotFoundException(Exception):

    def __init__(self, doc_path):
        Exception.__init__(self, f'No document found for path <{doc_path}>')


class IncompatibleApiVersionException(Exception):

    def __init__(self, found_api_version, current_api_version):
        Exception.__init__(self, f'Incompatible api version. Found <{found_api_version}>. '
                                 f'Current version: <{current_api_version}>')


class ExecutionNotAllowedException(Exception):

    def __init__(self, status):
        super().__init__(f'Execution Not Allowed! Status is already <{status}>.')


class SleepException(Exception):

    def __init__(self):
        super().__init__('Awaiting sleep!')


class RetryException(Exception):

    def __init__(self):
        super().__init__('Awaiting retry!')


class TimeoutException(RetryException):
    pass
