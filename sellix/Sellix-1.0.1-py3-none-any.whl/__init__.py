from .Blacklists import *
from .Categories import *
from .Coupons import *
from .Feedback import *
from .Orders import *
from .Products import *
from .Queries import *
from .Payments import *

__Name__ = "Sellix"
__Author__ = "xFueY"
__AuthorMail__ = "xFueY@protonmail.com"
__Version__ = "1.0.1"
__Description__ = "Python Sellix Wrapper"
__URL__ = "https://github.com/xFueY/Sellix/"
__License__ = "MIT"

class Sellix():
    def __init__(self, Authorization : str, URL : str = "https://dev.sellix.io/v1"):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = {"Authorization" : f"Bearer {Authorization}", "User-Agent" : f"Python Sellix v{__Version__}"}

        self.Orders = Orders(self.Authorization, self.URL, self.Headers)
        self.Blacklists = Blacklists(self.Authorization, self.URL, self.Headers)
        self.Categories = Categories(self.Authorization, self.URL, self.Headers)
        self.Coupons = Coupons(self.Authorization, self.URL, self.Headers)
        self.Feedback = Feedback(self.Authorization, self.URL, self.Headers)
        self.Products = Products(self.Authorization, self.URL, self.Headers)
        self.Queries = Queries(self.Authorization, self.URL, self.Headers)
        self.Payments = Payments(self.Authorization, self.URL, self.Headers)
