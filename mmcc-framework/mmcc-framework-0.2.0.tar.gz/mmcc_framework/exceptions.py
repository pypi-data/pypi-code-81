class DescriptionException(Exception):
    """ Exception raised when the check on the process description finds errors or incongruities.

    :ivar cause: the element that caused the error
    :ivar message: the message of this exception
    """

    def __init__(self, cause, message: str = "The process description caused an exception.") -> None:
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The cause of the exception was: {self.cause}"


class CallbackException(Exception):
    """ Exception raised when the check on the callbacks fails.

    :ivar cause: the parameter that caused the exception
    :ivar message: the message of this exception
    """

    def __init__(self, cause, message: str = "A callback caused an exception.") -> None:
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The parameter of the function was: {self.cause}"
