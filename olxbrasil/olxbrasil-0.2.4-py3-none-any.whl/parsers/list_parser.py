import contextlib
from math import ceil
from typing import Any, Dict

from bs4 import BeautifulSoup

from olxbrasil.parsers.base import OlxBaseParser
from olxbrasil.utils import format_price


class ListParser(OlxBaseParser):
    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)
        self.page_limit = self.__get_page_limit()
        self.current_page = self.__get_current_page()
        self.page_size = self.__get_page_size()

    def __get_page_limit(self) -> int:
        return min(
            ceil(self.__get_items_total() / self.__get_page_size()), 100
        )

    def __get_current_page(self) -> int:
        return self.initial_data["listingProps"]["pageIndex"]

    def __get_page_size(self) -> int:
        return self.initial_data["listingProps"]["pageSize"]

    def _get_ad_data(self):
        return self.initial_data["listingProps"]["adList"]

    def __get_items_total(self):
        return self.initial_data["listingProps"]["totalOfAds"]

    @property
    def items(self) -> Dict[str, Any]:
        ads = []
        for item in self.ad_data:
            with contextlib.suppress(KeyError):
                title = item.get("subject", "").strip()
                price = format_price(item.get("price"))
                url = item["url"]

                ads.append(
                    {
                        "title": title,
                        "price": float(price),
                        "url": url,
                        "is_professional": item["professionalAd"],
                    }
                )

        return {
            "ads": ads,
            "page": self.current_page,
            "total": self.page_size,
            "page_limit": self.page_limit,
        }
