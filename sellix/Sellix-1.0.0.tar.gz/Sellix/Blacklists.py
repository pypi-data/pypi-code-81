import requests

class Blacklists():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/blacklists/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/blacklists?page=" + str(Page), headers=self.Headers).json()

    def Create(self, Type : str, Data : str, Note : str = "None"):
        PostData = {"type" : Type, "data" : Data, "note" : Note}
        return requests.post(self.URL + "/blacklists", headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Edit(self, ID : str, Type : str, Data : str, Note : str = "None"):
        PostData = {"type" : Type, "data" : Data, "note" : Note}
        return requests.put(self.URL + "/blacklists/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Delete(self, ID : str):
        return requests.delete(self.URL + "/blacklists/" + ID, headers=self.Headers).json()
