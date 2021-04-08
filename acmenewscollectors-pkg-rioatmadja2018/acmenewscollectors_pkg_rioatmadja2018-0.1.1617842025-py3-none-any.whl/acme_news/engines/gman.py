#!/usr/bin/envp python
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict

class GMANEngine(ACMEBrowser):

    def __init__(self):
        self.search_query: str = ""
        self.page_size: int = 0
        self.page: int = 0
        self.gman_headers: Dict = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-GPC': '1'
        }
        super(ACMEBrowser).__init__()

    def get_pagesize(self) -> int:
        return self.page_size

    def get_page(self) -> int:
        return self.page

    def get_search_quer(self) -> str:
        return self.search_query

    def get_gman_reports(self, search_query: str, page: int = 1, page_size: int = 20, sort: str = "descending") -> List[Dict]:

        self.search_query = search_query.replace(" ", "+")
        self.page = page
        self.page_size = page_size

        if not self.search_query:
            raise ValueError("Please provide the right search query.")

        if not all([self.page, self.page_size]) and self.page <= 0 and self.page_size <= 0:
            raise ValueError("Please provide the right page and page_size")

        self.search_query: str = f"https://s.fbi.gov/?SearchableText={self.search_query}&searchHelpText=To+narrow+your+search%2C+select+a+content+type+option+listed+under+%E2%80%9CMore.%E2%80%9D+To+broaden+your+search+to+other+FBI+sites%2C+select+a+subdomain+listed+under+%E2%80%9CSource.%E2%80%9D&pageSize={self.page_size}&page={self.page}&sort_on=&sort_order={sort}&after="

        response: List[Dict] = self.transform_requests(response=self.fetch_api_request(api_endpoint=self.search_query, headers=self.gman_headers)).get('results', {})

        return self.normalize(response=response)

