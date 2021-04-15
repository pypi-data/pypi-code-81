from .BaseDiscriminator import BaseDiscriminator
from WebSonar.Common import Consts

from bs4 import BeautifulSoup
import requests

class ShopifyDiscriminator(BaseDiscriminator):
    def match(self, url: str) -> bool:
        r = requests.get(
            url, 
            headers=Consts.Soup.HEADERS, 
            timeout=Consts.Soup.TIMEOUT)
        soup = BeautifulSoup(r.content, features="html.parser")
        elts = soup.find_all(name="head")
        for head in elts:
            if ("cdn.shopify.com" in str(head) is not None):
                return True
        return False
