from WebSonar.Discriminators.ShopifyDiscriminator import ShopifyDiscriminator
from WebSonar.SearchEnginesProvider import GoogleEngine
from WebSonar.Common.Enums import SearchEngines, WebsiteType

from typing import Dict, List

class WebSonarEngine():
    def __init__(self):
        self._shopifyDiscriminator = ShopifyDiscriminator()
        self._googleEngine = GoogleEngine()

    def Identify(self, url: str) -> WebsiteType:
        try:
            if self._shopifyDiscriminator.match(url=url):
                return WebsiteType.Shopify
            else:
                return WebsiteType.Unknown
        except:
            # log exception
            return WebsiteType.Exception

    def ExtractLinksFromSearchEngine(
        self,
        query: str, 
        search_engine: SearchEngines = SearchEngines.Google,
        number: int = 10, 
        **kwargs) -> List[str]:

        if (search_engine == SearchEngines.Google):
            return self._googleEngine.search(query=query, number=number)
        else:
            # TODO: handle exception
            raise NotImplementedError(f"TODO: implement {search_engine} search")

    def IdentifySitesFromSearchQuery(
        self,
        query: str, 
        search_engines: List[SearchEngines], 
        number: int = 10) -> Dict[SearchEngines, Dict[str, WebsiteType]]:
        
        results = {}
        
        for se in search_engines:
            links = self.ExtractLinksFromSearchEngine(
                query=query, 
                search_engine=se,
                number=number,)
            results[se] = {l: self.Identify(l) for l in links}

        return results
