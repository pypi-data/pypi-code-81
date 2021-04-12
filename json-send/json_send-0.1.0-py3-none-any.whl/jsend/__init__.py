from enum import Enum


class Status(Enum):
    SUCCESS = 1
    FAIL = 2
    ERROR = 3


class JSend:
    def __init__(self, status: Status, data=None, message=None, code=None):
        self._status: Status = status
        if data is None:
            data = {}
        self._data = data
        self._message = message
        self._code = code  # Error code

    def to_json(self):
        return {
            'status': self._status.name.lower(),
            'data': self._data,
            'message': self._message,
            'code': self._code,
        }


def success(data=None):
    return JSend(Status.SUCCESS, data=data)


def fail(data=None):
    return JSend(Status.FAIL, data=data)


def error(message, code=None, data=None):
    return JSend(Status.ERROR, data=data, message=message, code=code)


if __name__ == '__main__':
    success_message = success()
    print(success_message.to_json())
