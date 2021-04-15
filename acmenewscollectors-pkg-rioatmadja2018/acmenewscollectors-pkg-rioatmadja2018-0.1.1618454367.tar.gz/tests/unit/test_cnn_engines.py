import pytest
from unittest import TestCase
import os
from acme_news.engines.cnn import CNNEngine
from typing import List, Dict

class TestBrowser(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_query(self):
        cnn = CNNEngine(news_article='iraq')
        self.assertEqual("https://www.cnn.com/search?size=10&q=iraq&category=politics", cnn.get_query())

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_all_queries(self):
        cnn = CNNEngine(news_article='iraq', page_depth=10)
        quries: List[str] = cnn.get_all_queries()
        self.assertEqual(1, len(quries))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_browser(self):
        cnn = CNNEngine(url="https://www.cnn.com/2021/03/19/world/meanwhile-in-america-march-19-intl-latam/index.html")
        return self.assertEqual(cnn.get_article_title(), "The bias facing Black and Asian Americans reflects a broader problem - CNN")


    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_cnn_links(self):
        cnn = CNNEngine(news_article='iraq')
        cnn_links: List[str] = cnn.get_links()
        return self.assertEqual(10, len(cnn_links))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_bulk_cnn_links(self):
        cnn = CNNEngine(news_article='iraq', page_depth=10)
        cnn_links: List[str] = cnn.get_all_links()
        return self.assertEqual(10, len(cnn_links))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_cnn_api_request(self):
        cnn = CNNEngine(news_article='iraq', category='all', api_endpoint=True)
        cnn_links: List[Dict] = cnn.get_page_content()
        return self.assertEqual(10, len(cnn_links))


    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_all_contents(self):
        cnn = CNNEngine(news_article='iraq', category='politics', api_endpoint=True, page_depth=10)
        contents: List[Dict] = cnn.get_all_contents()
        return self.assertEqual(10, len(contents))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_video_links(self):
        cnn = CNNEngine(news_article='iraq',
                        category='politics',
                        api_endpoint=True,
                        video=True)
        contents: List[Dict] = cnn.get_video_links()
        return self.assertEqual(10, len(contents))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_all_video_links(self):
        cnn = CNNEngine(news_article='iraq',
                        category='politics',
                        api_endpoint=True,
                        page_depth=10,
                        video=True)
        contents: List[Dict] = cnn.get_all_video_links()
        return self.assertEqual(10, len(contents))
