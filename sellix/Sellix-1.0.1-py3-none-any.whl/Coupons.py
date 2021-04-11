import requests

class Coupons():
    def __init__(self, Authorization, URL, Headers):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = Headers

    def Get(self, ID : str):
        return requests.get(self.URL + "/coupons/" + ID, headers=self.Headers).json()

    def List(self, Page : int = 0):
        return requests.get(self.URL + "/coupons?page=" + str(Page), headers=self.Headers).json()

    def Create(self, Code : str, DiscountValue : float, MaxUses : int = -1, ProductsBound : list = []):
        PostData = {"code" : Code, "discount_value" : DiscountValue, "max_uses" : MaxUses, "products_bound" : ProductsBound}
        return requests.post(self.URL + "/coupons", headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Edit(self, ID : str, Code : str, DiscountValue : float, MaxUses : int = -1, ProductsBound : list = []):
        PostData = {"code" : Code, "discount_value" : DiscountValue, "max_uses" : MaxUses, "products_bound" : ProductsBound}
        return requests.put(self.URL + "/coupons/" + ID, headers=self.Headers, data=str(PostData).replace("'", '"')).json()

    def Delete(self, ID : str):
        return requests.delete(self.URL + "/coupons/" + ID, headers=self.Headers).json()
