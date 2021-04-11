from .Orders import *

__Name__ = "Sellix"
__Author__ = "xFueY"
__AuthorMail__ = "xFueY@protonmail.com"
__Version__ = "0.0.1_1"
__Description__ = "Python Sellix Wrapper"
__URL__ = "https://github.com/xFueY/Sellix/"
__License__ = "MIT"

class Sellix():
    def __init__(self, Authorization : str, URL : str = "https://dev.sellix.io/v1"):
        self.Authorization = Authorization
        self.URL = URL
        self.Headers = {"Authorization" : f"Bearer {Authorization}", "User-Agent" : f"Python Sellix v{__Version__}"}

        self.Orders = Orders(self.Authorization, self.URL, self.Headers)
