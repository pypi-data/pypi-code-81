import requests

class Payments():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Create(self, *args, **kwargs):
        PostData = {}
        for x, y in kwargs.items():
            PostData[x] = y
        return requests.post(self.URL + "/payments", headers=self.Headers).json()

    def Delete(self, ID : str):
        return requests.delete(self.URL + "/payments/" + ID, headers=self.Headers).json()
