import requests

class Orders():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def FetchAll(self):
        return requests.get(self.URL + "/orders", headers=self.Headers).json()
