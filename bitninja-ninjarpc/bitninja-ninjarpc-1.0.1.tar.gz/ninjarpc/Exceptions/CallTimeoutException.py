class CallTimeoutException(BaseException):

    def __init__(self, call=None):
        self.call = call
