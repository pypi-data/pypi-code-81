import pytest
from unittest import TestCase
import os
from acme_news.engines.gman import GMANEngine
from typing import Dict, List

class TestBrowser(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_query(self):
        gman = GMANEngine()
        results: List[Dict] = gman.get_gman_reports(search_query="iran", page_size=10)
        self.assertEqual(10, len(results))
