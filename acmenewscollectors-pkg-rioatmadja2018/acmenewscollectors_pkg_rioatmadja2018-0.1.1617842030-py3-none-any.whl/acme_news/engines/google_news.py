#!/usr/bin/env python
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict

class GoogleNewsEngine(ACMEBrowser):
    """
    DESCRIPTION
        This class inherit the web browser functionalities from the ACME Browser and responsible to collect news content from GOOGLE

    FUNCTIONS
        __init__
        parse_google_news_links
        parse_news_contents
    """
    def __init__(self, search_query: str = ""):
        self.google_news_url: str = ""
        self.search_query: str = search_query
        self.google_driver = None
        super(GoogleNewsEngine, self).__init__()

    def parse_google_news_links(self) -> List[Dict]:
        results: List = []

        if not self.search_query:
            raise RuntimeError("Please provide the right query.")

        self.google_news_url = f"https://news.google.com/search?q={self.search_query}&hl=en-US&gl=US&ceid=US%3Aen"
        self.google_driver = self.browser(url=self.google_news_url)
        for tag in self.google_driver.find_elements_by_tag_name("article"):
            try:
                link_attributes: Dict = {'title': tag.find_element_by_tag_name('h3').text,
                                         'link': tag.find_element_by_tag_name('a').get_attribute("href"),
                                         'date': tag.find_element_by_tag_name('time').get_attribute("datetime"),
                                         'region_name': self.search_query
                }
                results.append(link_attributes)

            except:
                pass

        return results

    def parse_news_contents(self, url: str) -> Dict:
        if not url:
            raise ValueError("Please provide the right news URLs.")

        response: bytes = self.fetch_api_request(api_endpoint=url)

        return {'url': url,
                'content': response
                }