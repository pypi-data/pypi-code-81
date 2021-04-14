class FunctionRequest:
    def __init__(self, payload, headers):
        self.payload = payload
        self.headers = headers


class FunctionResponse:
    def __init__(self, payload, status, headers):
        self.payload = payload
        self.status = status
        self.headers = headers
