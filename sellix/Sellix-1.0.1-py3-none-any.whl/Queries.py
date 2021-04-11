import requests

class Queries():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/queries/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/queries?page=" + str(Page), headers=self.Headers).json()

    def Reply(self, ID : str, Message : str):
        PostData = {"reply" : Message}
        return requests.post(self.URL + "/queries/reply/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Close(self, ID : str):
        return requests.post(self.URL + "/queries/close/" + ID, headers=self.Headers).json()

    def Reopen(self, ID : str):
        return requests.post(self.URL + "/queries/reopen/" + ID, headers=self.Headers).json()
