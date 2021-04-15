class wTermException(BaseException):
    """
    wTermException is a custom Exception
    created so try|except code can detect
    for specifically wTermUi errors.
    """
    def __init__(self, message):
        self.message = "[wTermUi]: " + message
