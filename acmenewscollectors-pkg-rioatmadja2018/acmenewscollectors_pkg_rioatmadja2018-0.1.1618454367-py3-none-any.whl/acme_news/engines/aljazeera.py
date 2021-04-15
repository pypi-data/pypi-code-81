#!/usr/bin/env python
from acme_news.browser.acme_browser import ACMEBrowser
from base64 import urlsafe_b64encode
import re
from typing import Dict, List
from bs4 import BeautifulSoup

class AljazeeraEngine(ACMEBrowser):

    def __init__(self,
                 search_query: str,
                 category: str = 'politics',
                 start: int = 1,
                 video: bool = False,
                 quantity: int = 10,
                 offset: int = 1
                 ):
        """
        DESCRIPTION
            Helper class to interact with the Aljazeera directly

        PARAMETERS
            :param search_query: given non empty search query
            :param start: an optional parameter with a default value of one

        FUNCTIONS
            __init__
            __set_api_endpoint__
            __set_video_endpoint
            __get_api_endpoint__
            __get_video_endpoint
            parse_alj_contents
            parse_video_links
        """

        if not search_query:
            raise ValueError("Please provide the right query.")

        self.query: str = search_query
        self.category: str = category
        self.alj_endpoint: str = ""
        self.alj_video_endpoint: str = ""
        self.__set_api_endpoint__(query=search_query, start_at=start)

        if video:
            self.quantity = quantity
            self.offset = offset
            self.__set_video_endpoint__(query=search_query)

        self.aljazeera_headers: Dict = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                                        'Accept': '*/*',
                                        'Accept-Language': 'en-US,en;q=0.5',
                                        'content-type': 'application/json',
                                        'wp-site': 'aje',
                                        'original-domain': 'www.aljazeera.com',
                                        'Connection': 'keep-alive',
                                        'Cookie': 'ak_bmsc=ECFEBE0F108325996DC0037A0FCA4095ACE82B1E6A680000FB6B5E60E94B395D~plr+cDZUlXGRvYJfW0Ra0hduGjwDtpELaVgJfd2swSvSB6S3hyHysEyX9GAsWQGzSJNd2Kq3T+Oc1d9IGxqoQqCVeN5rCp02ECxQx1EYhC/keGDCMrXwIYxBKHYMFtG14pTV/0OPBB2mONLgfbEmBsU+oFJSBRRLQsX1ZlPTY/WfYvtzhHkXBnWZjy6T6amoUtvUfC9lb5TDzE7xWAxJdY8tP0C7bkmKoBNdqGL2hfR40=; bm_sv=A53E066F23025A3FD5CE211F30D44E88~2u/43e10uUxo6rVZ2RUAC/C2LrweGrwjTNDWib2hApkSJ0A7P3XjzzzrgL5X3F6KXsWx1mWG9BsHpPG2lxjz6Aeuxixwy6B2zxqmO8ezsPqZz4Fr3oy1QGO+TQOJmLBJi7PRkXtEzQ0+IiWLPGSiJ62zwq8o1MYQp70zfjXIy1w=; ALJAZEERA_ENSIGHTEN_PRIVACY_BANNER_LOADED=1; ALJAZEERA_ENSIGHTEN_PRIVACY_BANNER_VIEWED=1',
                                        'DNT': '1',
                                        'Sec-GPC': '1'
                                        }

        super(ACMEBrowser, self).__init__()

    def __set_api_endpoint__(self, query: str, start_at: int):
        if start_at < 1:
            raise ValueError(f"The starting Error must be greater than 1.")

        self.alj_endpoint = f"https://www.aljazeera.com/graphql?wp-site=aje&operationName=SearchQuery&variables=%7B%22query%22%3A%22{query}%20{self.category}%22%2C%22start%22%3A{start_at}%2C%22sort%22%3A%22relevance%22%7D&extensions=%7B%7D"

    def __set_video_endpoint__(self, query: str) -> str:
        if self.quantity < 0 or self.offset < 0:
            raise ValueError("The quantity and Offset must be greater than 0.")

        self.alj_video_endpoint = f'https://www.aljazeera.com/graphql?wp-site=aje&operationName=AjeSectionPostsQuery&variables=%7B%22category%22%3A%22{query}%22%2C%22categoryType%22%3A%22where%22%2C%22postTypes%22%3A%5B%22video%22%5D%2C%22quantity%22%3A{self.quantity}%2C%22offset%22%3A{self.offset}%7D&extensions=%7B%7D'

    def __get_api_endpoint__(self) -> str:
        return self.alj_endpoint

    def __get_video_endpoint(self) -> str:
        return self.alj_video_endpoint

    def parse_alj_contents(self) -> List[Dict]:
        results: List = []
        alj_api_responses = self.transform_requests(response=self.fetch_api_request(api_endpoint=self.alj_endpoint, headers=self.aljazeera_headers))
        for news_content in alj_api_responses.get('data').get('searchPosts').get('items'):
            news_item: Dict = {
                'region_name': self.query,
                'url': news_content.get('link', None),
                'news_date': re.match(r"\w{1,4}\s[0-9]{1,2},\s[0-9]{4}", news_content.get('link', None)),
                'category': self.category,
                'title': news_content.get('title', None),
                'image_url': urlsafe_b64encode(str(news_content.get('pagemap').get('cse_image')).encode('utf-8'))
            }
            results.append(news_item)

        return results

    def parse_video_links(self) -> List[Dict]:
        results: List = []
        alj_video_api = self.transform_requests(response=self.fetch_api_request(api_endpoint=self.alj_video_endpoint, headers=self.aljazeera_headers))
        for item in alj_video_api.get('data').get('articles'):
            video_links: Dict = {
                'region_name': self.query,
                'video_url': item.get('link'),
                'video_category': self.category,
                'news_url': item.get('shortUrl')
            }
            results.append(video_links)

        return results

    def parse_news_content(self, url) -> str:
        if not url:
            raise ValueError("Please provide the right URLs.")

        response: bytes = self.fetch_api_request(api_endpoint=url, headers=self.aljazeera_headers)
        soup = BeautifulSoup(response, 'html.parser')
        return '\n'.join([tag.text for tag in soup.find_all('p')])
