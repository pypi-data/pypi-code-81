#!/usr/bin/env python

"""Tests for `datasets` package."""

import unittest
# import sklearn
# from datasets.utils.token_dicts import TokenDicts
import numpy as np
from datasets.utils.tokenizer import BertTokenizer


class TestBertTokenizer(unittest.TestCase):
    """Tests for `datasets` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_bert_tokenizer(self):
        """Test something."""
        # init token_dicts
        tokenizer = BertTokenizer('tests/data/dicts/bert_vocab.txt')
        token_ids, segmen_ids = tokenizer.encode("hi,早上好呀，哈哈！")
        np.testing.assert_array_equal(token_ids, [101, 8913, 117, 3193, 677, 1962, 1435, 8024, 1506, 1506, 8013, 102])
        np.testing.assert_array_equal(segmen_ids, [0] * 12)

        token_ids, segmen_ids = tokenizer.encode("hello world,开始写代码")
        np.testing.assert_array_equal(token_ids, [101, 8701, 8572, 117, 2458, 1993, 1091, 807, 4772, 102])
        np.testing.assert_array_equal(segmen_ids, [0] * 10)

        token_ids, segmen_ids = tokenizer.encode("第一句话", "第二句话")
        np.testing.assert_array_equal(token_ids, [101, 5018, 671, 1368, 6413, 102, 5018, 753, 1368, 6413, 102])
        np.testing.assert_array_equal(segmen_ids, [0] * 6 + [1] * 5)


if __name__ == '__main__':
    unittest.main()
