import requests

class Products():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/products/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/products?page=" + str(Page), headers=self.Headers).json()

    def Create(self, Title : str, Description : str, Price : float, Gateways : list, Type : str, DiscountValue : float, **kwargs):
        PostData = {"title" : Title, "description" : Description, "price" : Price, "gateways" : Gateways, "type" : Type, "discount_value" : DiscountValue}
        for x, y in kwargs.items():
            PostData[x] = y
        return requests.post(self.URL + "/products", headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Edit(self, ID : str, Title : str, Description : str, Price : float, Gateways : list, Type : str, DiscountValue : float, **kwargs):
        PostData = {"title" : Title, "description" : Description, "price" : Price, "gateways" : Gateways, "type" : Type, "discount_value" : DiscountValue}
        for x, y in kwargs.items():
            PostData[x] = y
        return requests.put(self.URL + "/products/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Delete(self, ID : str):
        return requests.delete(self.URL + "/products/" + ID, headers=self.Headers).json()
