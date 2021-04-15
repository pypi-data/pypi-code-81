#!/usr/bin/python 
import os 
import pytest 
from typing import Dict,List 
from unittest import TestCase 
from acme_collectors.engines.aljazeera_engine import AljazeeraEngine 
class TestAljazeeraEngines(TestCase):

    @pytest.mark.skipif( os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test')
    def test_valid_urls(self):

        current_topic: str = "islamic state"
        response: List[str] = AljazeeraEngine(topic=current_topic).get_news_links() 
        return self.assertEqual(len(response), 12 )

    @pytest.mark.skipif( os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test')
    def test_parse_contents(self):

        current_topic: str = "islamic state"
        response: Dict = AljazeeraEngine(topic=current_topic).parse_contents() 
        aljazeera_topics: List[str] = list(response.keys())
        return self.assertEqual(len(aljazeera_topics), 12)