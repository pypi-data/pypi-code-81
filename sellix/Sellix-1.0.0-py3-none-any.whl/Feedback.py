import requests

class Feedback():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/feedback/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/feedback?page=" + Page, headers=self.Headers).json()

    def Reply(self, ID : str, Message : str):
        PostData = {"reply" : Message}
        return requests.post(self.URL + "/feedback/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()
