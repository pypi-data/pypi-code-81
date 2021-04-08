import pytest
from unittest import TestCase
import os
from acme_news.engines.russia_today import RussiaToday
from typing import List, Dict

class TestRussiaToday(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_parse_content(self):
        rt = RussiaToday(query='Iraq')
        results: List[Dict] = rt.parse_rt_contents()
        return self.assertEqual(10, len(results))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_bulk_quries(self):
        rt = RussiaToday(query='Iraq', content_type='Telecast')
        results: List[Dict] = rt.rt_bulk_quries(page=2, page_size=10)
        return self.assertEqual(10, len(results ))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_page_content(self):
        rt = RussiaToday()
        results: Dict = rt.parse_page_content(url="https://www.rt.com/usa/519626-msnbc-joe-vaccine-passports/")
        expected_result: str = "Support vaccine passports or go back to your caves, 'idiots,' MSNBC’s Joe Scarborough tells Republicans and civil liberties fans — RT USA News"
        return self.assertEqual(expected_result, results.get('title'))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_parse_video_link(self):
        rt = RussiaToday()
        results: Dict = rt.parse_video_link(url="https://www.rt.com/shows/sputnik/518599-china-west-iraq-pope/")
        expected_result: str = "The Far East and the Middle East (E376) — RT Sputnik Orbiting the WorldAA"
        return self.assertEqual(expected_result, results.get('title'))
