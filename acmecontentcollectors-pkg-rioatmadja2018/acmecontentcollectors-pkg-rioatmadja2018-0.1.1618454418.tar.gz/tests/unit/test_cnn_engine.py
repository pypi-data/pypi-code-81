#!/usr/bin/env python
from unittest import TestCase
import pytest
import os
from acme_collectors.engines.cnn_engine import CNNENGINE
from typing import List

class TestCNNEngine(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test' )
    def test_cnn_links(self):
        cnn_engine = CNNENGINE(topic='Islamic State')
        links, pages = cnn_engine.get_cnn_links()
        return self.assertListEqual([len(links), len(pages)], [10, 5])


    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test')
    def test_cnn_parse_content(self):
        cnn_engine = CNNENGINE()
        current_article: str = cnn_engine.parse_content(url='https://www.cnn.com/2020/09/02/politics/american-isis-member-kuzu-pleads-guilty/index.html')

        article_title: str = "American ISIS member pleads guilty to supporting terror group"
        return self.assertEqual(article_title in current_article, True) 
