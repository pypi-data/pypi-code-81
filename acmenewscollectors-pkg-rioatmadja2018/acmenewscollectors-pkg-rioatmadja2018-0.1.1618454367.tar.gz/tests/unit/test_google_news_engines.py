import pytest
from unittest import TestCase
import os
from acme_news.engines.google_news import GoogleNewsEngine

class TestGoogleNews(TestCase):
    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_query(self):
        gnews = GoogleNewsEngine(search_query='iraq')
        results = gnews.parse_google_news_links()
        print(results)
        return self.assertEqual(100, len(results))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_parse_content(self):
        gnews = GoogleNewsEngine()
        results = gnews.parse_news_contents(url='https://news.google.com/articles/CAIiEDZCK0jVl3DOy5QS58lIgX0qGQgEKhAIACoHCAow4OH9CjCg6_UCMJ-42gU?hl=en-US&gl=US&ceid=US%3Aen')
        return self.assertEqual(2, len(results))
