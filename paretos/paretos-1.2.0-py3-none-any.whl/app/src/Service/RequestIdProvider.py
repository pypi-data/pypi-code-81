import uuid


class RequestIdProvider:
    def __init__(self):
        self.__request_id: str = ""
        self.update()

    def update(self):
        self.__request_id = str(uuid.uuid4())

    def get_request_id(self) -> str:
        return self.__request_id
