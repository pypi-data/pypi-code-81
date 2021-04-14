class wTermException(BaseException):
    def __init__(self, message):
        self.message = "[wTermUi]: " + message
