from WebSonar.SearchEnginesProvider import BaseSearchEngine
from WebSonar.Common import Consts
from WebSonar.Common.Exceptions import RetrievingSearchResultsException
from typing import List
from bs4 import BeautifulSoup

import requests

class GoogleEngine(BaseSearchEngine):
    def _divToLink(self, d) -> str:
        try:
            return d.div.div.a["href"]
        except:
            #TODO: log exception
            pass

    def search(self, query: str, number: int = 10) -> List[str]:
        res = []
        start = 0
        while (start < number):
            r = requests.get(
                Consts.Urls.GoogleQuery.format(query=query, start=start), 
                headers=Consts.Soup.HEADERS, 
                timeout=Consts.Soup.TIMEOUT)
            soup = BeautifulSoup(r.content, features="html.parser")
            elts = soup.find_all(name="div", attrs={"class": Consts.Soup.GoogleResultClass})
            res_page = list(filter(lambda x: x is not None, map(self._divToLink, elts)))
            res += res_page
            if len(res_page) == 0:
                raise RetrievingSearchResultsException()
            start += len(res_page)
        return res[:number]