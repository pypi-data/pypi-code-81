#!/usr/bin/env python
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict
import re

class CNNEngine(ACMEBrowser):
    """
    DESCRIPTION
        This class inherit the web browser functionalities from the ACMEBrowser.

    FUNCTIONS
        __init__
        __build_bulk_query__
        __build_url_query__
        __set_category__
        __set_page_size__
        __parse_cnn_api_response__
        __parse_cnn_videos_endpoints__
        get_query
        get_all_queries
        get_article_title
        get_links
        get_all_links
        get_page_content
        get_all_contents
        get_video_links
        get_all_video_links

    USAGE
        Please run the tests using pytest tests
    """
    def __init__(self, url: str = "",
                 news_article: str = "",
                 page_depth: int = 0,
                 category: str = "politics",
                 api_endpoint: bool = False,
                 video: bool = False,
                 size: int = 10):

        self.url: str = url
        self.query: str = ""
        self.use_api_endpoint: bool = api_endpoint
        self.endpoint: str = "https://search.api.cnn.io/content" if self.use_api_endpoint else "https://www.cnn.com/search"
        self.video: bool = video
        self.video_enpoint: str = "https://fave.api.cnn.io/v1/video?id"
        self.vido_required_params: str = "&customer=cnn&edition=domestic&env=prod"
        self.page_depth = page_depth
        self.news_article: str = news_article
        self.size: int = size
        self.category: str = category
        self.cnn_links: List = []
        self.batch_queries: List = []
        self.cnn_driver = None
        self.categories: List[str] = ['us', 'world', 'politics', 'business', 'opinions', 'health', 'entertainment', 'style', 'travel']

        if self.url:
            self.cnn_driver = self.browser(url=self.url)

        elif self.news_article and page_depth > 0 and not self.use_api_endpoint:
            self.batch_queries = self.__build_bulk_query__()

        elif self.news_article and not self.use_api_endpoint:
            self.cnn_driver = self.browser(url=self.__build_url_query__(size=self.size,
                                                                        category=self.category)
                                           )

        super(CNNEngine, self).__init__()

    def __build_bulk_query__(self) -> List[str]:
        if not self.news_article:
            raise ValueError(f"Please provide the right news articles")

        if self.page_depth % 10 != 0:
            raise ValueError("Page depth must be a multply of 10")

        self.batch_queries = [self.__build_url_query__(page=article_page) for article_page in range(0, self.page_depth, 10)]
        return self.batch_queries

    def __build_url_query__(self, size: int = 10, category: str = "politics", page: int = 0) -> str:

        self.__set_category__(category=category)
        self.__set_page_size__(page_size=size)

        if not self.news_article:
            raise ValueError(f"Please provide the right news articles")

        if self.category == 'all':
            self.query = f"{self.endpoint}?size={self.size}&q={self.news_article}"
            return self.query

        if self.category.lower() not in self.categories:
            raise ValueError(f"The following category {self.category} is not the right category.")

        if self.use_api_endpoint and self.video:
            self.query = f"{self.endpoint}?size={self.size}&q={self.news_article}&category={self.category}&type=video"

            if self.page_depth > 0:
                self.query += f"&from={page}&page={round(page / 10) + 1}"

            return self.query

        if self.page_depth == 0:
            self.query = f"{self.endpoint}?size={self.size}&q={self.news_article}&category={self.category}"
            return self.query

        self.query = f"{self.endpoint}?size={self.size}&q={self.news_article}&category={self.category}&from={page}&page={round(page/10) +1}"
        return self.query

    def __set_category__(self, category):
        if not category:
            raise ValueError("Please provide the right category.")

        self.category = category

    def __set_page_size__(self, page_size):
        if not page_size or page_size < 1 or not isinstance(page_size, int):
            raise ValueError("Please provide the right page size")

        self.size = page_size

    def __parse_cnn_api_response__(self, response: bytes) -> List:
        results: Dict = self.transform_requests(response=response)
        if not results:
            return []

        cnn_api_results: List  = []
        for item in results.get('result'):
            current_item: Dict = {
               'region_name' : self.news_article,
                'url': item.get('url'),
                'news_date': item.get('firstPublishDate'),
                'title': item.get('headline'),
                'category': item.get('section'),
                'content': item.get('body'),
                'image_url': item.get('thumbnail')
            }
            cnn_api_results.append(current_item)

        return cnn_api_results

    def __parse_cnn_videos_endpoints__(self, response: Dict) -> List:
        results: List = []
        for item in response.get('result'):
            video_path: str = item.get('path')
            results.append("{}={}{}".format(self.video_enpoint,
                                           video_path[video_path.find(item.get('section')):],
                                           self.vido_required_params))
        return results

    def get_query(self) -> str:
        return self.query

    def get_all_queries(self) -> List[str]:
        return self.batch_queries

    def get_article_title(self) -> str:
        return self.cnn_driver.title

    def get_links(self) -> List[str]:
        return [tag.find_element_by_tag_name('a').get_attribute('href') for tag in self.cnn_driver.find_elements_by_css_selector("h3.cnn-search__result-headline")]

    def get_all_links(self) -> List[str]:
        quries: List[str] = self.__build_bulk_query__()
        for url_query in quries:
            self.cnn_driver = self.browser(url=url_query)
            self.cnn_links.extend(self.get_links())

        return self.cnn_links

    def get_page_content(self, endpoint: str = "") -> List[Dict]:

        if endpoint:
            cnn_api_endpoint = endpoint
        else:
            cnn_api_endpoint = self.__build_url_query__()

        if not self.use_api_endpoint:
            raise NotImplementedError(f"Only available for API endpoint.")

        response: bytes = self.fetch_api_request(api_endpoint=cnn_api_endpoint)
        return self.__parse_cnn_api_response__(response=response)

    def get_all_contents(self) -> List[Dict]:
        cnn_api_endpoints: List[str] = self.__build_bulk_query__()
        results: List = []
        if not self.use_api_endpoint:
            raise NotImplementedError(f"Only available for API endpoint.")

        for query in cnn_api_endpoints:
            results.extend(self.get_page_content(endpoint=query))

        return results

    def get_video_links(self, endpoint: str = "") -> List[str]:
        if not self.endpoint and not self.video:
            raise ValueError("Please enable endpoint and the video args.")

        videos_api_endpoints: str = endpoint if endpoint else self.__build_url_query__()

        response: Dict = self.transform_requests(response=self.fetch_api_request(api_endpoint=videos_api_endpoints))
        response_video_endpoints: List[str] = self.__parse_cnn_videos_endpoints__(response=response)

        results: List = []
        for api_endpoint in response_video_endpoints:
            resp: Dict = self.transform_requests(response=self.fetch_api_request(api_endpoint=api_endpoint))
            video_link = list(filter(lambda video: re.findall(r"mp4$", video.get('fileUri')), resp.get('files')))
            if not video_link:
                video_link = "None"

            video_link = video_link[0].get('fileUri', 'None')

            video_attribute: Dict = {
                'region_name': self.news_article,
                'video_url': video_link,
                'video_category': resp.get('category'),
                'news_url': f"http:{resp.get('clickbackURL')}"
            }
            results.append(video_attribute)

        return results

    def get_all_video_links(self) -> List[str]:

        cnn_api_endpoints: List[str] = self.__build_bulk_query__()
        results: List = []
        if not self.use_api_endpoint:
            raise NotImplementedError(f"Only available for API endpoint.")

        for endpoint_url in cnn_api_endpoints:
            results.extend(self.get_video_links(endpoint=endpoint_url))

        return results


