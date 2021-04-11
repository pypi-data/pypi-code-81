import requests

class Categories():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/categories/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/categories?page=" + str(Page), headers=self.Headers).json()

    def Create(self, Title : str, Unlisted : int, SortPriority : str, ProductsBound : list):
        PostData = {"title" : Title, "unlisted" : Unlisted, "sort_priority" : SortPriority, "products_bound" : ProductsBound}
        return requests.post(self.URL + "/categories", headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Edit(self, ID : str, Title : str, Unlisted : int, SortPriority : str, ProductsBound : list):
        PostData = {"title" : Title, "unlisted" : Unlisted, "sort_priority" : SortPriority, "products_bound" : ProductsBound}
        return requests.put(self.URL + "/categories/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Delete(self, ID : str):
        return requests.delete(self.URL + "/categories/" + ID, headers=self.Headers).json()
