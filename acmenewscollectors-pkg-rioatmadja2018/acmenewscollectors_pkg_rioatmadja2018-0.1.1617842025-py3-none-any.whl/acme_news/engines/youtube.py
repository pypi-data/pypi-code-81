#!/usr/bin/env python
import json
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize
import re

class YoutubeEngine(ACMEBrowser):
    def __init__(self, search_query: str):
        self.results: List = []
        self.url: str = ""
        self.__set_search_query(search_query=search_query)
        self.youtube_driver = self.browser(url=self.url)
        super(YoutubeEngine, self).__init__()

    def __set_search_query(self, search_query: str):
        if not search_query:
            raise ValueError("Please provide the right search query.")

        self.url = f'https://www.youtube.com/results?search_query={search_query}'

    def load_results(self) -> List:
        soup = BeautifulSoup(self.youtube_driver.page_source, 'html.parser')
        for tag in soup.find_all('script'):
            script = str(tag)
            if script.find("responseContext") != -1:
                self.results.append(script)

        if self.results:
            youtube_content = json.loads(re.sub("<script.*.Data =", "", self.results[0].replace("<script>", "").replace("</script>", "").rstrip(";"))).get('contents').get('twoColumnSearchResultsRenderer').get('primaryContents').get('sectionListRenderer').get('contents')[0].get('itemSectionRenderer').get('contents')
            df = json_normalize(youtube_content)
            results = [attr.get('thumbnailOverlayToggleButtonRenderer', {}).get('untoggledServiceEndpoint', {}).get('signalServiceEndpoint',{}) for youtube_attr in df['videoRenderer.thumbnailOverlays'].values.tolist() if isinstance(youtube_attr, List) for attr in youtube_attr]
            return results


