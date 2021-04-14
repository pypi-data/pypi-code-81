from .Outcome import Outcome


class Failure(Outcome):
    uuid = "b3987c9b-02dc-4ae0-9548-0c963c16c937"
    message = "Generic failure."
    http_status_code = 200

    def __init__(self, details: dict = None):
        self.__details = {}

        if details is not None:
            self.__details = details

    @classmethod
    def get_id(cls) -> str:
        return cls.uuid

    @classmethod
    def get_message(cls) -> str:
        return cls.message

    @classmethod
    def get_http_status_code(self):
        return self.http_status_code

    def get_details(self) -> dict:
        return self.__details
