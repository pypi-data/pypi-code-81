import pytest
from unittest import TestCase
import os
from acme_news.engines.youtube import YoutubeEngine

class TestYoutubeEngine(TestCase):
    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_query(self):
        youtube = YoutubeEngine(search_query='iraq')
        results = youtube.load_results()
        self.assertEqual(80, len(results))
